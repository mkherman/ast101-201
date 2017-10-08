import os
import argparse
import numpy as np
import natsort as ns
import matplotlib.pyplot as plt
import pandas as pd


parser = argparse.ArgumentParser(description='Calculates exam marks for AST101/201.')

parser.add_argument('-d', '--directory', default=os.getcwd(), type=str,
					help='the directory path to the exam data')
parser.add_argument('-r', '--remark', required=True, type=str,
					help='file name of the remark scantron data')
parser.add_argument('-p', '--portal', required=True, type=str,
					help='file name of the Portal student data')
parser.add_argument('-o', '--output', default='exam_marks.csv', type=str,
					help='desired output file name')
parser.add_argument('-mc', required=True, type=int,
					help='number of multiple choice questions on exam')
parser.add_argument('-sa', required=True, type=int,
					help='number of short answer questions on exam')
parser.add_argument('-tot', '--total', required=True, type=float,
					help='total number of points possible on exam')
parser.add_argument("--plot", action="store_true", default=False,
                    help='include this option to plot results')

args = parser.parse_args()

path = args.directory
remark = os.path.join(path, args.remark)
portal = os.path.join(path, args.portal)
output = os.path.join(path, args.output)
numMC = args.mc
numSA = args.sa
totalpts = args.total
plots = args.plot



# Read in Remark exam data and Portal student info
rdata = pd.read_csv(remark)
pdata = pd.read_csv(portal)

# Merge data
data = pd.merge(rdata,pdata,left_on='Student Number',right_on='Student ID',
		suffixes=('',' portal'),how='left')
data = data.rename(columns={'Total Score':'MC Score'})

# Find the students who messed up their ID and make my life difficult
missed = data.loc[data['Student Number'] != data['Student ID']]

if len(missed) != 0:
	print '\n*** You have %s unmatched students out of %s ***\n' %(len(missed),len(data))
	print 'The following students likely dropped the course or messed up their student number. To fix this:  \
		\n  - Find their name in the Portal .csv file, if they are still enrolled  \
		\n  - Determine their correct student number  \
		\n  - Edit their student number in the Remark .csv file (maybe make a copy first)  \
		\n  - Save everything and rerun this code  \
		\nTrust me, it is safer to do this by eye!\n'
	print missed[['Last Name','First Initial','Student Number']], '\n'

	raise SystemExit(0)

# Correct for blank MC answers
data.replace({'BLANK': 'N'}, regex=True, inplace=True)

# Correct for multiple selected answers in MC questions
MCcols = ['MC'+str(i) for i in range(1,numMC+1)]
data[MCcols] = data[MCcols].replace('.*,.*','M',regex=True)

# Create MC answer string
data['MC Answers'] = data.iloc[:,9:9+numMC].sum(axis=1)

# Calculate SA score
SAhcols = ['SA_Half'+str(i) for i in range(1,numSA+1)]
data[SAhcols] = 0.5 * data[SAhcols]
SAcols = ['SA'+str(i) for i in range(1,numSA+1)] + SAhcols
data['SA Score'] = sum(data[cols] for cols in SAcols)

# Calculate total score
data['Total (%)'] = ((data['MC Score'] + data['SA Score'])/totalpts*100.).round(4)


# Sort data by student username and write all results to output .csv file
data = data.reindex(index=ns.order_by_index(data.index, ns.index_natsorted(data['Username'])))
outcols = ['Username', 'MC Score', 'SA Score', 'Total (%)', 'MC Answers']
data[outcols].to_csv(output, index=False)

print '\nNice, no unmatched students! Your output file has been saved.'
print '\n*** IMPORTANT ***'
print 'Do not forget to change the column names in the output file to '
print 'match the columns specific to the Portal grade center for your course!\n'


if plots:
	# Create total score histogram
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.hist(data['Total (%)'], bins=np.arange(0,100,4), edgecolor='k', color='0.75')
	ax.set_xlim(0,100)
	ax.set_ylim(ymin=0)	
	ax.set_xlabel('Score (%)')
	ax.set_ylabel('Frequency')
	ax.set_title('Total Score')
	fig.savefig(os.path.join(path,'Total_Score.png'))
	plt.close(fig)

	# Create SA score histograms (only works for 4 questions right now)
	if numSA == 4:
		for i in range(1,numSA+1):
			data['SA_Full'+str(i)] = data['SA'+str(i)] + data['SA_Half'+str(i)]

		SApts = (totalpts-numMC)/numSA


		fig = plt.figure()

		ax3 = fig.add_subplot(223)
		ax3.hist(data['SA_Full3'], bins=np.arange(0,SApts+1,0.5), 
			edgecolor='k', color='0.75')
		ax3.set_xlabel('Score')
		ax3.set_ylabel('Frequency')
		ax3.text(ax3.get_xlim()[1]*0.05,ax3.get_ylim()[1]*0.85,'SA Question 3')

		ax4 = fig.add_subplot(224, sharex=ax3, sharey=ax3)
		ax4.hist(data['SA_Full4'], bins=np.arange(0,SApts+1,0.5), 
			edgecolor='k', color='0.75')
		ax4.set_xlabel('Score')
		plt.setp(ax4.get_yticklabels(),visible=False)
		ax4.text(ax4.get_xlim()[1]*0.05,ax4.get_ylim()[1]*0.85,'SA Question 4')

		ax1 = fig.add_subplot(221, sharex=ax3, sharey=ax3)
		ax1.hist(data['SA_Full1'], bins=np.arange(0,SApts+1,0.5), 
			edgecolor='k', color='0.75')
		plt.setp(ax1.get_xticklabels(),visible=False)
		ax1.set_ylabel('Frequency')
		ax1.text(ax1.get_xlim()[1]*0.05,ax1.get_ylim()[1]*0.85,'SA Question 1')

		ax2 = fig.add_subplot(222, sharex=ax3, sharey=ax3)
		ax2.hist(data['SA_Full2'], bins=np.arange(0,SApts+1,0.5), 
			edgecolor='k', color='0.75')
		plt.setp(ax2.get_xticklabels(),visible=False)
		plt.setp(ax2.get_yticklabels(),visible=False)
		ax2.set_xbound(lower=0,upper=SApts+0.5)
		ax2.set_ybound(lower=0)
		ax2.text(ax2.get_xlim()[1]*0.05,ax2.get_ylim()[1]*0.85,'SA Question 2')

		fig.tight_layout()
		fig.savefig(os.path.join(path,'SA_Scores.png'))
		plt.close(fig)

	else:
		print 'No SA Score plot created. Code only written to plot exactly 4 SA questions.'

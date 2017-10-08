AST101/201 Marking Code
========

This code calculates the Midterm/Final Exam marks for students in AST101/201. 
It outputs a CSV file containing student information and their exam results, which can be uploaded to Portal.


Requirements
++++++++++++++

This code uses Python 2.7. You'll need the packages `pandas <https://pandas.pydata.org/pandas-docs/stable/install.html>`_ and `natsort <http://natsort.readthedocs.io/en/master/intro.html#installation>`_, both of which can be installed via pip or conda.

Before you begin, you should have two CSV files ready: 

* the **Remark results** from all of the ScanTron data
* the **student user information** downloaded from the Portal course website, which you can retrieve by going to the Grade Center and choosing 'Work Offline'


Running the code
++++++++++++++

To perform the marking routine, run:

.. code-block:: bash

    python marking.py -d {directory} -r {Remark} -p {Portal} -mc {numMC} -sa {numSA} -tot {totalpts}

where: 

* ``{directory}`` is the directory where the two aforementioned CSV files are located (current directory by default)
* ``{Remark}`` is the name of the Remark file
* ``{Portal}`` is the name of the Portal file
* ``{numMC}`` is the number of multiple choice questions
* ``{numSA}`` is the number of short-answer questions
* ``{totalpts}`` is the total number of points possible on the exam

You can also specify:

* ``-o {output}`` for the desired name of the output CSV file
* ``--plot`` to plot the mark distributions

Note that currently the code is only able to plot the short-answer distributions if there are exactly 4 questions.


Output
++++++++++++++

Generally there will be a handful of students who wrote down their ID numbers incorrectly on their ScanTron sheets. This is a problem, because their marks will not be properly uploaded to Portal, and it's very tricky to fix without human aid! Some students will also have dropped the course after taking the exam, and so will not be listed in Portal.

Therefore, the code prints a list of all the students for whom a matching ID number was not found. You need to find these students in the Portal file, identify their correct ID number, and update this number in the Remark file. If the student dropped the course, remove them from the Remark file. It's a good idea to make a copy of the file before doing this, just in case.

After fixing all of the incorrect ID numbers, run the code again. If all of the students' ID numbers are correct you will receive confirmation that the marking results have been saved.

**BUT WAIT! THERE'S MORE.**

Before you can upload the results to Portal, **you need to edit the column names in the output CSV file** to match the columns you've (hopefully already) created in Portal's Grade Center. The Grade Center columns have specific ID numbers and point allocations described within them which vary between courses and semesters. Just copy and paste the names from Portal into the output CSV file. You should then be able to upload it to Portal without any issues. 




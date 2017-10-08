AST101/201 Marking Code
========

This code calculates the Midterm/Final Exam marks for students in AST101/201. 
It outputs a CSV file containing student information and their exam results so the file can easily be uploaded to Portal.


Requirements
++++++++++++++

This code uses Python 2.7. You'll also need the packages pandas `pandas <https://pandas.pydata.org/pandas-docs/stable/install.html>`_ and `natsort <http://natsort.readthedocs.io/en/master/intro.html#installation>`_. Both of these can be installed via pip or conda.

Before you begin, you should have two .csv files ready: 
* the **Remark results** from all of the ScanTron data
* the **student user information** downloaded from the Portal course website, which you can retrieve by going to the Grade Center and choosing 'Work Offline'


Running the code
++++++++++++++

To perform the marking routine, run:

.. code-block:: bash

    python marking.py -d {directory} -r {Remark} -p {Portal} -mc {numMC} -sa {numSA} -tot {totalpts}

where 
* ``{directory}`` is the directory where the two aforementioned CSV files are located (current directory by default)
* ``{Remark}`` is the name of the Remark file
* ``{Portal}`` is the name of the Portal file
* ``{numMC}`` is the number of multiple choice questions
* ``{numSA}`` is the number of short-answer quetions
* ``{totalpts}`` is the total number of points possible on the exam

You can also specify:
* ``-o {output}`` for the desired name of the output CSV file
* ``--plot`` to plot the mark distributions


Output
++++++++++++++

Generally there will be a handful of students who wrote down their ID numbers incorrectly on their ScanTron sheets. This is a problem, because their marks will not be properly uploaded to Portal. Unfortunately, this is very tricky to fix without human aid.

Therefore, the code prints a list of all the students for whom a matching ID number was not found. You need to find these students in the Portal file, identify their correct ID number, and update this number in the Remark file. It's a good idea to make a copy of the Remark file before doing this, just in case!

After fixing all of the incorrect ID numbers, run the code again. If all of the students' ID numbers perfectly match between the two files you should receive confirmation that the marking results have been saved.

**BUT WAIT! THERE'S MORE.**

Before you can upload the results to Portal, *you need to edit the column names in the output CSV file* to match the columns you've (hopefully already) created in Portal's Grade Center. They have specific ID numbers and point allocations described within them which vary between courses and semesters. Just copy and paste the names from Portal into the output CSV file. Now you should be able to upload it to Portal without any issues. 




# plotter_p2.py
# Andrea

# DO NOT MODIFY THIS FILE

import sys, os
import numpy as np
import matplotlib.pyplot as plt
import hashlib

def file_hash(fname):
    with open(fname,"rb") as f:
        return hashlib.sha256(f.read()).hexdigest();

input_file = 'input_p2.txt'

description="""This plotter script reads time series values for the number of tweets
per hour.  Time series are read from the file {}.

Each line of the file consists of three integers separated by spaces. The first
integer represents the number of hours since the earliest observed tweet in all
the data (i.e., tweets occurring in that first hour will have a time of 0).
The second number represents the number of tweets occurring in that hour in the
Obama corpus.  The third number represents the number of tweets occurring in
that hour in the Romney corpus.

For example:
    0 9 2
    1 8 0
    2 5 11
    3 28 88
    . . .
    72 0 0
    73 1 0
    . . .
means there are 9 tweets in the Obama corpus in hour zero and two in Romney
corpus, and so forth. 

Note the following:

  * The number of hours continues well beyond 24, as the data cover multiple
    days.
  * Lines must be recorded in order by number of hours, so that the time
    series is correctly represented chronologically.
  * Zero counts need to be included for times when there are no counts, to
    "line" up the two time series.

Consult the course introductory reading if you need help preparing Python code
to write this file.
""".format(input_file)


import argparse
from argparse import RawTextHelpFormatter
parser = argparse.ArgumentParser(
    description=description,
    formatter_class=RawTextHelpFormatter
)
results = parser.parse_args()

try:
    D = np.loadtxt(input_file)
    a = D[:,0]
    b = D[:,1]
    c = D[:,2]
except:
    sys.exit("""
Something is your wrong with your input file. (Is it named and formatted
correctly? Have you checked the help message?) 
Exiting...
""".strip())

# hash:
input_hash = file_hash(input_file)
scrpt_hash = file_hash(sys.argv[0])

# plot:
plt.plot(a,b, color='C0', label='Obama')
plt.plot(a,c, color='C3', label='Romney')

plt.xlabel(r"Time [hours]")
plt.ylabel("Number of tweets")
plt.legend(loc='upper left')
plt.xlim([-24, 408])
plt.ylim([25, 225])
plt.title("{}-I\n{}-P".format(input_hash, scrpt_hash), 
          loc='left', fontsize='small')

plt.tight_layout()
plt.savefig("plotter_p2.pdf")
plt.savefig("plotter_p2.svg")
print("File created: plotter_p2.pdf at location {}".format(os.getcwd()))


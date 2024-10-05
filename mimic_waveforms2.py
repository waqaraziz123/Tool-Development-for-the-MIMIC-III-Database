# mimic_waveforms2.py
"""
This code will generate a similar csv file as mimic_waveforms1.csv but without a frequency resolution column (as it is the same for all the recordings, i.e., 125 Hz) 

Access to MIMIC-III Clinical Database: https://physionet.org/content/mimiciii/1.4/

Access to MIMIC-III Waveform Database Matched Subset: https://physionet.org/content/mimic3wdb-matched/1.0/

Inputs:

-- mimic_waveforms1.csv
   
Outputs:

-- mimic_waveforms2.csv 
    This will output the contents of matched waveforms (i.e., subject_id, header file name, time stamp, signal duration, and signal name)
    for all subjects present in the MIMIC-III matched waveform database.
   
How to run it:

python mimic_waveforms2.py | out-file mimic_waveforms2.csv -encoding ASCII

"""

import __main__ as mn
from matplotlib.pyplot import ion
if not hasattr(mn,'__file__'): # running interactively
  ion()
  for _clrk in list(vars().keys()):
    if _clrk not in _svdir:
      vars().__delitem__(_clrk)

import numpy as np
import time
import sys
import re
import pdb

if True:
  filename = 'mimic_waveform1.csv'
  readopt = "r"

  with open(filename,readopt,newline=None) as infile:
    for line in infile:
      #str = line.decode('utf-8')
      str = line
      sp = re.split('[ ,\n\r]+',str)
      #print(len(sp))
      for jj in range(len(sp)-3):
        print(sp[jj],',',end='')
      print(sp[-3])

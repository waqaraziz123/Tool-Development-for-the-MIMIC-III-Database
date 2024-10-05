

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
  #filename = 'waveforms.csv'
  filename = 'waveform_sample.csv'
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

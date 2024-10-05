
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

NN = 3670021

if True:
  filename = 'waveforms2.csv'
  readopt = "r"
  patienta = np.zeros(NN,dtype=int)
  name0a   = np.zeros(NN,dtype=int)
  name1a   = np.zeros(NN,dtype=int)
  timea    = np.zeros(NN,dtype=float)
  lena     = np.zeros(NN,dtype=int)
  typea    = np.zeros(NN,dtype=int)
  with open(filename,readopt,newline=None) as infile:
    ii=-1
    for line in infile:
      ii += 1
      if ii%100000==0:
         print(ii)
      #str = line.decode('utf-8')
      str = line
      sp = re.split('[ ,\n\r]+',str)
      fl = re.split('_',sp[1])
      t1 = sp[0]
      patienta[ii] = int(t1[1:])
      name0a[ii]   = int(fl[0])
      name1a[ii]   = int(fl[1])
      timea[ii] = float(sp[2])
      lena[ii] = int(sp[3])
      ptype = sp[4]
      if ptype=='ABP':
        typea[ii]=1
  np.save('wpatient_abp',patienta)
  np.save('wname0_abp',name0a)
  np.save('wname1_abp',name1a)
  np.save('wtime_abp',timea)
  np.save('wlen_abp',lena)
  np.save('wtype_abp',typea)

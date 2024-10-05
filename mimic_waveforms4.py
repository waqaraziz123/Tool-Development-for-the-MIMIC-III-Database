
import __main__ as mn
from matplotlib.pyplot import ion
if not hasattr(mn,'__file__'):
  ion()
  for _clrk in list(vars().keys()):
    if _clrk not in _svdir:
      vars().__delitem__(_clrk)

import numpy as np
import time
import sys
import re
import pdb

patienta = np.load('wpatient_abp.npy')
name0a   = np.load('wname0_abp.npy')
name1a   = np.load('wname1_abp.npy')
timea    = np.load('wtime_abp.npy')
lena     = np.load('wlen_abp.npy')
typea    = np.load('wtype_abp.npy')

readopt = "r"

if True:
  staypatient = dict()
  ii = 0
  with open('ids.csv',readopt,newline=None) as infile:
    for line in infile:
      ii += 1
      if ii<2:
        continue
      # Extract the line and split it into the components
      str1 = line
      sp = re.split('[,\n\r]',str1)
      icustay =int(sp[0])
      subjectid = int(sp[1])
      staypatient[icustay] = subjectid

if True:
  filename = 'clinicalvitals_1h.txt'

  with open(filename,readopt,newline=None) as infile:
    ii = 0
    jj = 0
    for line in infile:
      ii += 1
      if ii<2:
        # The first line is just headings for the columns
        print(line.rstrip(),end='')
        print(',filename,offset')
        continue
      # Extract the line and split it into the components
      str1 = line
      sp = re.split('[,\n\r]',str1)
      icustay =int(sp[0])
      predicttime = int(sp[1])
      subjectid = staypatient[icustay]
      f1 = np.flatnonzero(np.logical_and(
        subjectid==patienta,np.logical_and(
          typea==1,np.logical_and(
            predicttime>timea,predicttime<=timea + lena/125.))))
      if f1.size==1:
        subjectidstr = 'p'+str(f"{subjectid:06}")
        print(line.rstrip(),','+subjectidstr[0:3]+'/'+subjectidstr+'/'
              +str(f'{int(name0a[f1]):7}')
              +'_'+str(f'{int(name1a[f1]):04}')+'.hea,',
              int(np.round(predicttime-timea[f1])))
      elif f1.size==0:
        a=1
        #print(line,',None,0')
      #print(ii,f1.size)
      if f1.size>1:
        print('size error: ',ii,',',f1.size,file=sys.stderr)
  print(ii)

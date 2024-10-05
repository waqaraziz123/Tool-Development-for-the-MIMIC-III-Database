

import __main__ as mn
if not hasattr(mn,'__file__'):
  for _clrk in list(vars().keys()):
    if _clrk not in _svdir:
      vars().__delitem__(_clrk)

import numpy as np
import time
import sys
import re
import pdb

if True:
  N = 629321   # number of entries in the numerics database
  N = 22055    # number of entries in the numerics2 database
  N = 22247	   # number of enteries in numerics2_new.csv file
  epoch      = np.zeros(N,dtype=float)
  samples    = np.zeros(N,dtype=float)
  intervals  = np.zeros(N,dtype=float)
  filenames  = np.empty(N,dtype='<U26')
  datfiles   = np.empty(N,dtype='<U13')
  invert     = dict() # allows us to find line numbers that match a patient id
  with open('numerics2_all.csv','r',newline=None) as infile:
    ii = -1
    for line in infile:
      ii += 1
      sp = re.split('[,\n\r]',line)
      filename1 = sp[0]
      subjectid = filename1[0:7]
      try:
        lns = invert[subjectid]
      except:
        lns = list()
      lns.append(ii)
      invert[subjectid] = lns
      epoch[ii]      = float(sp[1])
      intervals[ii]  = float(sp[2])
      samples[ii]    = float(sp[3])
      filenames[ii]  = filename1
      datfiles[ii]   = sp[4]

  stoptimes = epoch + samples*intervals


if True:
  # Read in the translation between icustays and patient IDs
  staypatient = dict()
  ii = 0
  with open('ids.csv','r',newline=None) as infile:
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

  with open(filename,'r',newline=None) as infile:
    ii = 0
    for line in infile:
      ii += 1
      if ii<2:
        # The first line is just headings for the columns
        print(line.rstrip(),end='')
        strz = (',filename1,offset1,interval1,dat1,'
               'filename2,offset2,interval2,dat2' )
        print(strz)
        continue
      # Extract the line and split it into the components
      str1 = line
      sp = re.split('[,\n\r]',str1)
      icustay =int(sp[0])
      predicttime = int(sp[1])
      #subjectid = staypatient[icustay]
      #subjectid = 'p'+str(f"{staypatient[icustay]:06}")
      subjectid = 'p'+str(staypatient[icustay]).zfill(6)

      try:
        lns = np.array(invert[subjectid])
        lens = lns.size
      except:
        lens = 0

      if lens==0:
        #print(line.rstrip(),',None,0')
        continue

      startb = epoch[lns]
      stopb = stoptimes[lns]
      intervalb = intervals[lns]

      f1 = np.flatnonzero(np.logical_and(
            predicttime>startb,predicttime<=stopb))
      if f1.size<=0:
        #print(line.rstrip(),',None,0')
        continue
      startc = startb[f1]
      offsetc = np.asarray(np.round((predicttime-startb[f1])/intervalb[f1]),
                           dtype=int)
      intervalc = intervalb[f1]
      lnsf1 = lns[f1]
      allfilenames = filenames[lnsf1]
      alldats = datfiles[lnsf1]
      uu = np.unique(allfilenames)
      ndx0 = np.flatnonzero(uu[0]==allfilenames)
      offset0 = offsetc[ndx0[0]]
      interval0 = intervalc[ndx0[0]]
      dat0 = alldats[ndx0[0]]
      print(line.rstrip(),','+subjectid[1:3]+'/'+subjectid+'/',
            uu[0],',',offset0,',',interval0,',',dat0,sep='',end='')
      if uu.size>1:
        ndx1 = np.flatnonzero(uu[1]==allfilenames)
        offset1 = offsetc[ndx1[0]]
        interval1 = intervalc[ndx1[0]]
        dat1 = alldats[ndx1[0]]
        print(',',subjectid[1:3],'/',subjectid,'/',
              uu[0],',',offset1,',',interval1,',',dat1,sep='')
      else:
        print(',None,0,0,None')

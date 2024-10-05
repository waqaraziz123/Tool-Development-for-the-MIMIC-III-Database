# mimic_waveforms1.py
"""
This code can search the entire MIMIC-III Waveform Database Matched Subset (waveform records).

Access to MIMIC-III Clinical Database: https://physionet.org/content/mimiciii/1.4/

Access to MIMIC-III Waveform Database Matched Subset: https://physionet.org/content/mimic3wdb-matched/1.0/

Inputs:

-- This code assumes that you have downloaded the MIMIC-III Waveform Database Matched Subset on your local machine to scroll through the header files
   to extract the required information about data files and offset values.
   
Outputs:

-- mimic_waveforms1.csv
   This will output the contents of matched waveforms (i.e., subject_id, header file name, time stamp, signal duration, signal name, and frequency resolution)
   for all subjects present in the MIMIC-III matched waveform database.
   
How to run it:

python mimic_waveforms1.py | out-file mimic_waveforms1.csv -encoding ASCII

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
import os
import re
import sys
import calendar

import pdb
from line_profiler import LineProfiler
lp = LineProfiler()

def tstr(strr,seconds):
  tt1 = time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(seconds))
  print(strr+' = '+tt1+' , ',seconds,file=sys.stderr)


if True:
  root1 = 'Z:/test'
  readopt = "r"
  ii=0
  for dirName, subdirList, fileList in sorted(os.walk(root1)):
      head,tail = os.path.split(dirName)
      if tail[0]=='p' and len(tail)==7:
          RECORDname = dirName+'/RECORDS'
          with open(RECORDname,readopt,newline=None) as patientfile:
              for paline in patientfile:
                  str = paline
                  if str[0:7] == tail and not str[-2]=='n':
                      admissionname = str[:-1]
                      with open(dirName+'/'+admissionname + '.hea',
                      readopt,newline=None) as admissionfile:
                          adii=0
                          samplecount = 0
                          for adline in admissionfile:
                              adii += 1
                              adsp = re.split('\s+',adline)
                              if adii==1:
                                  adsamplerate=float(adsp[2])
                                  adsamples =int(adsp[3])
                                  tmsp = re.split('\.',adsp[4])
                                  adtime1 = time.strptime(adsp[5]+'-'+tmsp[0]+' UTC',
                                          '%d/%m/%Y-%H:%M:%S %Z')
                                  adtimev = float(calendar.timegm(adtime1))
                                  adtimechk = time.gmtime(adtimev)
                                  if not adtimechk==adtime1:
                                      print('time check error ')
                                      crashout0
                                  if len(tmsp)>1:
                                      adtimev = adtimev+float('.'+tmsp[1])
                                      bltimev = adtimev
                              elif adii>2:
                                  if not adline[0]=='#':
                                      blocksamples = int(adsp[1])
                                      bltimev += blocksamples/adsamplerate
                                      if not adline[0]=='~':
                                          blockname = adsp[0]
                                          
                                          #bltimestruct = time.gmtime(bltimev)
                                          #blhour = bltimestruct.tm_hour
                                          #blmin = bltimestruct.tm_min
                                          #blsec = bltimestruct.tm_sec
                                          #blseconds = 3600*blhour+60*blmin+blsec
                                          try:
                                              with open(dirName+'/'+blockname + '.hea',
                                                        readopt,newline=None) as blockfile:
                                                  blii = 0
                                                  for blline in blockfile:
                                                      blii += 1
                                                      blsp = re.split('\s+',blline)
                                                      if blii==1:
                                                          blsamplerate=float(blsp[2])
                                                          if not blsamplerate==adsamplerate:
                                                              print('sample rate error, ',
                                                                    dirName,',',blockname,file=sys.stderr)
                                                          #bltmsp  = re.split(':',blsp[4])
                                                          #if len(bltmsp)==3:
                                                              #blhour2 = int(bltmsp[0])
                                                              #blmin2  = int(bltmsp[1])
                                                              #blsec2  = float(bltmsp[2])
                                                          #else:
                                                              #blhour2 = 0
                                                              #blmin2  = int(bltmsp[0])
                                                              #blsec2  = float(bltmsp[1])
                                                          #blseconds2= 3600*blhour2+60*blmin2+blsec2
                                                          #if blseconds2-blseconds<-60:
                                                              #bltimev += 60*60*24 # sort this out
                                                          #tt1 = time.strftime('%Y-%m-%d UTC',
                                                                              #time.gmtime(bltimev))
                                                          #tt2 = time.strptime(tt1,'%Y-%m-%d %Z')
                                                          #tt3 = float(calendar.timegm(tt2))
                                                          #bltimev = tt3 + blseconds2
                                                          if False:
                                                              print('block time error',tail,',',
                                                                    admissionname,',',
                                                                    blockname,',',blline,',',
                                                                    blhour,':',blmin,':',blsec,',',
                                                                    blhour2,':',blmin2,':',blsec2,',',
                                                                    file=sys.stderr)
                                                              print('tt1=',tt1,file=sys.stderr)
                                                              print('tt3=',tt3,file=sys.stderr)
                                                              print('adtimev=',adtimev,file=sys.stderr)
                                                              print('blttimev=',bltimev,file=sys.stderr)
                                                              print('blocksamples=',blocksamples,
                                                                    file=sys.stderr)
                                                              crashout1
                                                          else:
                                                              wavtype = blsp[-2]
                                                              print(tail,',',blockname,',',
                                                                    samplecount,',',blocksamples,
                                                                    ',',wavtype,',',adsamplerate)
                                                              
                                          except:
                                              print(dirName+'/'+blockname + '.hea not found',
                                                    file=sys.stderr)
                                  samplecount += bltimev
                          if False:
                              print('sample count error: ', dirName,',',admissionname,',',
                                    samplecount,',',adsamples,',',
                                    samplecount-adsamples,file=sys.stderr)
                              

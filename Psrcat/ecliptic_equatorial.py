#!/Users/persusx/anaconda3/bin/python

import math

import numpy as np

def deg2HMS(ra='', dec='', round=False):
  RA, DEC, rs, ds = '', '', '', ''
  if dec:
    if str(dec)[0] == '-':
      ds, dec = '-', abs(dec)
    deg = int(dec)
    decM = abs(int((dec-deg)*60))
    if round:
      decS = int((abs((dec-deg)*60)-decM)*60)
    else:
      decS = (abs((dec-deg)*60)-decM)*60
    DEC = '{0}{1} {2} {3}'.format(ds, deg, decM, decS)
  
  if ra:
    if str(ra)[0] == '-':
      rs, ra = '-', abs(ra)
    raH = int(ra/15)
    raM = int(((ra/15)-raH)*60)
    if round:
      raS = int(((((ra/15)-raH)*60)-raM)*60)
    else:
      raS = ((((ra/15)-raH)*60)-raM)*60
    RA = '{0}{1} {2} {3}'.format(rs, raH, raM, raS)
  
  if ra and dec:
    return (RA, DEC)
  else:
    return RA or DEC

def decdeg2dms(dd):
    negative = dd < 0
    dd = abs(dd)
    minutes,seconds = divmod(dd*3600,60)
    degrees,minutes = divmod(minutes,60)
    if negative:
        if degrees > 0:
            degrees = -degrees
        elif minutes > 0:
            minutes = -minutes
        else:
            seconds = -seconds
    return (degrees,minutes,seconds)


def decdeg2hms(dd):
    negative = dd < 0
    dd = abs(dd)
    minutes,seconds = divmod(dd*15*60,60)
    hour,minutes = divmod(minutes,60)
    if negative:
        if hour > 0:
            hour = -hour
        elif minutes > 0:
            minutes = -minutes
        else:
            seconds = -seconds
    return (hour,minutes,seconds)


varep = math.radians(23+26/60+20.512/3600)

print(decdeg2hms(37.574),decdeg2dms(54.067))

lam = math.radians(37.574) #change deg to rad
beta = math.radians(54.067)

sindelt = math.sin(varep)*math.sin(lam)* \
    math.cos(beta)+math.cos(varep)*math.sin(beta)
delt = math.asin(sindelt)

cosalp = math.cos(lam)*math.cos(beta)/math.cos(delt)


alpha = math.acos(cosalp)

delt = decdeg2dms(math.degrees(delt))
alpha = decdeg2dms(math.degrees(alpha))
print(delt,alpha)











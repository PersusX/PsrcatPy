#!/Users/persusx/anaconda3/bin/python

import math
import numpy as np
from Psrcat import psrcat


def HMS2deg(ra='',dec='',rou=True):
    '''convert Hms or Dms to deg'''
    if dec:
        num = list(dec).count(':') ## the number of ":"
        if num ==0:
            decdeg = int(dec)
        elif num ==1:
            decdeg = int(dec.split(":",1)[0]) + round(float(dec.split(":",1)[1]),1)/60
        elif num ==2:
            decdeg = int(dec.split(":",2)[0]) + int(dec.split(":",2)[1])/60+round(float(dec.split(":",2)[2]),1)/3600

    if ra:
        num = list(ra).count(':') ## the number of ":"
        #print("ra",ra)
        if num ==0:
            radeg = int(ra)*15
        elif num ==1:
            radeg = int(ra.split(":",1)[0])*15 + round(float(ra.split(":",1)[1]),2)/60*15
        elif num ==2:
            radeg = int(ra.split(":",2)[0])*15 + int(ra.split(":",2)[1])/60*15+round(float(ra.split(":",2)[1]),1)/3600*15

    if ra and dec:
        return (radeg, decdeg)
    else:
        return radeg or decdeg



def deg2HMS(ra='', dec='', rou=True):
    '''convert deg to ra's HMS or dec's DHS'''
    RA, DEC, rs, ds = '', '', '', ''
    if dec:
        if str(dec)[0] == '-':
            ds, dec = '-', abs(dec)
        deg = int(dec)
        decM = abs(int((dec-deg)*60))
        
        if rou:
            decS = round((abs((dec-deg)*60)-decM)*60,1)
        else:
            decS = (abs((dec-deg)*60)-decM)*60
        
        if deg ==0:
            deg ="00"
        elif deg <10:
            deg = "0%s"%deg
        
        if decM ==0:
            decM ="00"
        elif decM <10:
            decM = "0%s"%decM
            
        if decS ==0:
            decS ="00.0"
        elif decS <10:
            decS = "0%s"%decS
            
        DEC = '{0}{1}:{2}:{3}'.format(ds, deg, decM, decS)
  
    if ra:
        if str(ra)[0] == '-':
            rs, ra = '-', abs(ra)
        raH = int(ra/15)
        raM = int(((ra/15)-raH)*60)
        if rou:
            raS = round(((((ra/15)-raH)*60)-raM)*60,1)
        else:
            raS = ((((ra/15)-raH)*60)-raM)*60
            
        if raH ==0:
            raH = "00"
        elif raH <10:
            raH = "0%s"%raH
            
        if raM ==0:
            raM = "00"
        elif raM <10:
            raM = "0%s"%raM
            
        if raS ==0:
            raS = "00.0"
        elif raS <10:
            raS = "0%s"%raS
        
        RA = '{0}{1}:{2}:{3}'.format(rs, raH, raM, raS)
  
    if ra and dec:
        return (RA, DEC)
    else:
        return RA or DEC

#def HMS2deg(ra='', dec='', rou=True):

def convertEquatorial(el,eb):
    '''convert Ecliptic(el eb) to Equatorial raj decj'''
    #el Ecliptic longitude (degrees)
    #eb Ecliptic latitude (degrees)
    
    M_PI = math.pi
    sin = math.sin
    cos = math.cos
    asin = math.asin
    tan = math.tan
    atan2 = math.atan2
    
    ce = 0.91748213149438 # Cos epsilon
    se = 0.39777699580108 # Sine epsilon
    dr = M_PI/180.0
    
    sdec = sin(eb*dr)*ce + cos(eb*dr)*se*sin(el*dr)
    dec = asin(sdec) # in radians
    cos_ra = (cos(el*dr)*cos(eb*dr)/cos(dec))
    sin_ra = (sin(dec)*ce - sin(eb*dr))/(cos(dec)*se)
    ra = atan2(sin_ra,cos_ra)  # in radians
    
    #Get RA into range 0 to 360
    if ra < 0.0:
        ra = 2*M_PI+ra
    elif ra > 2*M_PI:
        ra = ra - 2*M_PI

    raj = math.degrees(ra) # convert to degrees
    decj = math.degrees(dec) #convert to degree

    ra = deg2HMS(ra=raj)
    dec = deg2HMS(dec=decj)

    return ra,dec




def convertEcliptic(raj,decj):
    '''convert raj deci to elog elat'''
    #rai in rad
    #decj in rad

    M_PI = math.pi
    sin = math.sin
    cos = math.cos
    asin = math.asin
    tan = math.tan
    atan2 = math.atan2
    
    
    deg2rad = M_PI/180.0
    epsilon = 23.439292*deg2rad
    #/*  epsilon = 23.441884*deg2rad;*/

    sinb = sin(decj)*cos(epsilon)-cos(decj)*sin(epsilon)*sin(raj)
    beta = asin(sinb)
    y = sin(raj)*cos(epsilon)+tan(decj)*sin(epsilon)
    x = cos(raj)
  
    lambdap = atan2(y,x)
    if lambdap<0:
        lambdaa = lambdap+2*M_PI
    else:
        lambdaa = lambdap

    elong = round(math.degrees(lambdaa),3) # convert to degree
    elat  = round(math.degrees(beta),3)

    return elong,elat

def convertGalactic(raj,decj):
    '''convert raj decj to gl gb'''
    # raj in rad
    # decj in rad
    M_PI = math.pi
    sin = math.sin
    cos = math.cos
    asin = math.asin
    tan = math.tan
    atan2 = math.atan2


    deg2rad = M_PI/180.0
    gpoleRAJ = 192.85*deg2rad
    gpoleDECJ = 27.116*deg2rad
    rot = [0.0]*9
    rot = np.array(rot).reshape(3,3)

    #/* Note: Galactic coordinates are defined from B1950 system - e.g. must transform from J2000.0 equatorial coordinates to IAU 1958 Galactic coords */
  
    #/* Convert to rectangular coordinates */
    rx = cos(raj)*cos(decj)
    ry = sin(raj)*cos(decj)
    rz = sin(decj)
    
    #/* Now rotate the coordinate axes to correct for the effects of precession */
    #/* These values contain the conversion between J2000 and B1950 and from B1950 to Galactic */
    rot[0][0] = -0.054875539726
    rot[0][1] = -0.873437108010
    rot[0][2] = -0.483834985808
    rot[1][0] =  0.494109453312
    rot[1][1] = -0.444829589425
    rot[1][2] =  0.746982251810
    rot[2][0] = -0.867666135858
    rot[2][1] = -0.198076386122
    rot[2][2] =  0.455983795705
    
    rx2 = rot[0][0]*rx + rot[0][1]*ry + rot[0][2]*rz
    ry2 = rot[1][0]*rx + rot[1][1]*ry + rot[1][2]*rz
    rz2 = rot[2][0]*rx + rot[2][1]*ry + rot[2][2]*rz

    #/* Convert the rectangular coordinates back to spherical coordinates */
    
    gb = asin(rz2)
    gl = atan2(ry2,rx2)
    if gl < 0:
        gl += 2.0*M_PI
    gl = round(math.degrees(gl),3)
    gb = round(math.degrees(gb),3)
        
    return gl,gb




#el,eb = convertEcliptic(1.2,0.5)
#gl,gb = convertGalactic(1.2,0.5)
#print(el,eb)
#print(gl,gb)

psr = psrcat.psrcat()

Raj = psr.get_para("RAJ")
Decj = psr.get_para("DECJ")
elon = psr.get_para("ELONG")
elat = psr.get_para("ELAT")

P1err = psr.get_para_err("P1")
print("number of PXerr:",len(P1err),P1err)
'''
for i in range(len(Raj)):
    #print(Rajerr[i])
    if Raj[i] == "*":
        raii,decii = convertEquatorial(float(elon[i]),float(elat[i]))
        Raj[i] = raii
    if elon[i] == "*":
        radeg,decdeg = HMS2deg(ra=Raj[i],dec=Decj[i])
        #print("radeg decdeg:",radeg,decdeg,"hms",Raj[i],Decj[i])
        rarad = math.radians(round(radeg,3))
        derad = math.radians(round(decdeg,3))
        elonii,elatii = convertEcliptic(rarad,derad)
        #print("elong,elat",elonii,elatii)
    elon[i]=elonii
'''
#DIST = psr.get_dist()


#for i in DIST:
 #   print("DIST",i)
#print("num",len(DIST))
#for i in range(len(Raj)):
 #   print(Raj[i],elon[i])

#ra,dec = convertEquatorial(9.07039380,6.3091085)
#print(ra,dec)


def find_galcoord_ecliptic(el,eb,pmel,pmelerr,pmeb,pmeberr,dist):

    # angles in mas/yr to kms/s (along with distances in kpc)
    dang2vel = 4.7405;
    # Oort's consts */
    a=14.5
    b=-12.0
    r0=8.5
    #v0gal,vsun[4];
    # Solar velocity */
    vsun=[9.2,10.5,6.9]
    #/* Galactic rotation velocty at the Earth */
    v0gal = 225.0 # /* Using flat rotation curve */

    l2000,b2000,cel2gal= ec2gal_ecliptic(el,eb)
    cel= [pmel,pmeb]
    #/* Calculate the position in galactic cartesian coordinates */
    #/* x increasing towards the galactic centre */
    cosb = cos(b2000)
    galcart = [cos(l2000)*cosb,sin(l2000)*cosb,sin(b2000)]

    for i in range(3):
        galcart[i]=galcart[i]*dist

    #/* Calculate the projected galactocentric distance to the source */
    gcr=math.sqrt(math.pow(r0-galcart[0],2)+math.pow(galcart[1],2))
    #/* Calculate the proper motions in galactic coords */
    gal = matx2v_ecliptic(cel2gal,cel)

    #/* Form the covarience matrix */
    covmat = [0]*4
    covmat = np.array(covmat).reshape(2,2)
    covmat[0][0] = pmelerr*pmelerr
    covmat[1][1] = pmeberr*pmeberr
    covmat[0][1] = covar*pmelerr*pmeberr
    covmat[1][0] = covar*pmelerr*pmeberr
    
    #/* Postmultiply by the conversion matrix */
    covmatgal =  multiply_ecliptic(covmat,cel2gal)
 
    #/* Premultiply by the transpose of the conversion matrix */
    ddtemp = cel2gal[0][1]
    cel2gal[0][1] = cel2gal[1][0]
    cel2gal[1][0]=ddtemp
    covmatgal =  multiply_ecliptic(cel2gal,covmatgal)

    pmlerr = math.sqrt(math.fabs(covmatgal[0][0]))
    pmberr = math.sqrt(math.fabs(covmatgal[1][1]))
    covargal = covmatgal[0][1]/math.fabs(pmlerr)/math.fabs(pmeberr)


    #/* Calculate orthogonal vectors */
    
    p = [0]*3
    p[1] = -sin(l2000)
    p[2] =  cos(l2000)
    p[3] =  0.0

    q = [0]*3
    q[1] = -sin(b2000)*cos(l2000)
    q[2] = -sin(b2000)*sin(l2000)
    q[3] =  cos(b2000)

    r = [0]*3
    r[1] =  cos(b2000)*cos(l2000)
    r[2] =  cos(b2000)*sin(l2000)
    r[3] =  sin(b2000)

    #/* Form dot product with the sun's velocity vector */
    vsl = -product_ecliptic(p,vsun)/dist/dang2vel
    vsb = -product_ecliptic(q,vsun)/dist/dang2vel

    #/* Find the proper motions expected from galactic rotation using rotation */
    #/* curve model */
    thetagal = math.atan2(galcart[1],r0-galcart[0])
    vrgal = v0gal # /* Use flat rotation curve */
    vgal = [0]*3
    vgal[0] = vrgal*sin(thetagal)
    vgal[1] = vrgal*cos(thetagal)-v0gal
    vgal[2] = 0.0

    pmlrot=product_ecliptic(p,vgal)/dist/dang2vel
    pmbrot=product_ecliptic(q,vgal)/dist/dang2vel


    #/* Take the galactiv rotation and solar motion off the galactic pm */
    pmb = gal[1];
    pml = gal[0];
    pmb = pmb-pmbrot-vsb
    pml = pml-pmlrot-vsl

    mul=pml
    mulerr = pmlerr
    mub = pmb
    muberr = pmberr
    
    return mul,mulerr,mub,muberr


#/* Derived from SLA_EQGAL */
def  ec2gal_ecliptic(dr,dd):

    #/* Postmultiply equatorial to galactic rotation matrix with */
    #/* ecliptic to equatorial rotation matrix */
    ce = 0.91748213149438 #/* Cos epsilon  */
    se = 0.39777699580108 #/* Sine epsilon */
    a = -0.054875539726
    b = -0.873437108010
    c = -0.483834985808
    d = +0.494109453312
    e = -0.444829589425
    f = +0.746982251810
    g = -0.867666135858
    h = -0.198076386122
    i = +0.455983795705
    
    rmat = [0]*9
    rmat = np.array(rmat).reshape(3,3)
    
    rmat[0][0] = a
    rmat[0][1] = b*ce+c*se
    rmat[0][2] = -b*se+c*ce

    rmat[1][0] = d;
    rmat[1][1] = e*ce+f*se
    rmat[1][2] = -e*se+f*ce
  
    rmat[2][0] = g
    rmat[2][1] = h*ce+i*se
    rmat[2][2] = -h*se+i*ce
    cos = math.cos # cite cos def
    sin = math.sin # cite sin def
    cosb=cos(dd)
    v1 = [cos(dr)*cosb,sin(dr)*cosb,sin(dd)]
    p = [-sin(dd)*cos(dr),-sin(dd)*sin(dr),cos(dd)]
    
    #/* Ecliptic to galactic */
    v1,v2 = transform_ecliptic(rmat,v1,v2)
    p,tp = transform_ecliptic(rmat,p,tp)
    q,tq = transform_ecliptic(rmat,q,tq)

    #/* Cartesian to spherical */
    dl,db = dir2sph_ecliptic(v2,dl,db)
    
    #/* Express in conventional ranges */
    dl = f_mod_ecliptic(dl,2.0*M_PI)
    if (dl < 0):
        dl = dl+M_PI*2.0

    db = f_mod_ecliptic(db,2.0*M_PI);
    if (db < 0):
        db = db+M_PI*2.0
    
    #/* Form the p vector in galactic reference frame */
    pg = [-sin(dl),cos(dl),0.0]
   
    #/* Form the proper motion rotation matrix */
    rotmat = [0]*4
    rotmat = np.array(rotmat).reshape(2,2)
    rotmat[0][0] = product_ecliptic(pg,tp)
    rotmat[1][1] = rotmat[1][1]
    rotmat[0][1] = product_ecliptic(pg,tq)
    rotmat[1][0] = -rotmat[1][2]
    
    return dl,db,rotmat
   
   
#/* Performs the 3-D forward unitary transformation: */
def transform_ecliptic(dm,va,vb):
    
    #double w,vw[4]
    #dm = [0]*9
    for j in range(3):
        w=0.0
        for i in range(3):
            w=w+dm[j][i]*va[i]
            vw[j]=w
  
    for j in range(3):
        vb[j] = vw[j]
    
    return va,vb
    
#/* Direction cosines to spherical coordinates (double precision) */
def dir2sph_ecliptic(v,a,b):
    
    x=v[0]
    y=v[1];
    z=v[2];
    r=math.sqrt(x*x+y*y)
    if (r==0):
        a=0.0
    else:
        a = math.atan2(y,x);

    if (z==0):
        b = 0.0;
    else:
        b = math.atan2(z,r);
    return a,b

def f_mod_ecliptic(a,p):
    return a - (int(a / p) * p)
    
#/*  Scalar product of two 3-vectors  (double precision) */
def product_ecliptic(va,vb):
    return va[0]*vb[0]+va[1]*vb[1]+va[2]*vb[2]

#/* Fortran sign */
def f_sign_ecliptic(a,b):
    if b >=0:
        return math.fabs(a)
    else:
        return -math.fabs(a)

def matx2v_ecliptic(mat,v):
    r = [0]*2
    r[0] = mat[0][0]*v[0]+mat[0][1]*v[1]
    r[1] = mat[1][0]*v[0]+mat[1][1]*v[1]
    return r

def multiply_ecliptic(a,b,c):
    wm = [0]*4
    wm = np.array(wm).reshape(2,2)
    for i in range(2):
        for j in range(2):
            w = 0.0
            for k in range(2):
                w = w + a[i][k]*b[k][j]
            wm[i][j] = w
    for j in range(2):
        for i in range(2):
            c[i][j]=wm[i][j]
            
    return c


#!/Users/persusx/anaconda3/bin/python
# version 1.1
# this sopftware is to get the value and parameter of psrcat.db
# Contact PersusXie@outlook.com if in doubt

import math
import numpy as np
import Psrcat.Coordinate as Co
import astropy.units as aunits
from astropy import units as u
from scipy.optimize import newton
from astropy.constants import c, GM_sun
from astropy.coordinates import SkyCoord, ICRS, Galactic, BarycentricMeanEcliptic

class psrcat():

    def __init__(self):
        
        self.f = open("../Psrcat/psrcat.db","r")   #设置文件对象
        data = []
    
        line = self.f.readline()
        line = line[:-1]
        while line:             #直到读取完文件
            line = self.f.readline()  #读取一行文件，包括换行符
            line = line[:-1]     #去掉换行符，也可以不去
            if line == '':   ##判断去除空行
                print("please have fun")
                #data.append(line)
            elif line[0] != "#": ## 判断去除解释行
                #print(line)
                data.append(line)
        self.f.close() #关闭文件

        self.Psrcard = [] ## 创建PSR信息卡集合
        card = {}
        for i in range(len(data)):
            #card = {} ## 生成每个PSR的信息卡
            if data[i][0] != "@":
                key,value = self.get_item(data[i])
                card[key]=value
            else:
                self.Psrcard.append(card)
                card = {}
        #Jname = self.get_Jname()
        #print(Jname)
        #Bname = self.get_Bname()
        #print()
        #for i in range(len(Jname)):
         #   print(Bname[i],Jname[i])


    def get_Jname(self):
        """
        psrD为psr卡片信息卡集合
        获取脉冲星的Jname
        """
        psrD=self.Psrcard
        num = len(psrD)
        Jname = []
        for i in range(num):
            factor0 = psrD[i].__contains__("PSRJ")
            factor1 = psrD[i].__contains__("PSRB")
            if factor0 == True:
                Jname.append(psrD[i]["PSRJ"][0])
            elif factor1 == True:
                Jname.append(psrD[i]["PSRB"][0])
            else:
                print("these is someting wrong")
        return Jname


    def get_Bname(self):
        """
        psrD为psr卡片信息卡集合
        获取脉冲星的Bname
        """
        psrD = self.Psrcard
        num = len(psrD)
        Bname = []
        for i in range(num):
            factor1 = psrD[i].__contains__("PSRJ")
            factor0 = psrD[i].__contains__("PSRB")
            if factor0 == True:
                Bname.append(psrD[i]["PSRB"][0])
            elif factor1 == True:
                Bname.append(psrD[i]["PSRJ"][0])
            else:
                print("these is someting wrong")
        return Bname

        
    def get_para(self,para):
        """
        psrD为psr卡片信息卡集合
        获取脉冲星的参数
        """
        psrD = self.Psrcard
        num = len(psrD)
        para1 = para.upper()
        data = []
        for i in range(num):
            factor1 = psrD[i].__contains__(para1)
            if factor1 == True:
                data.append(psrD[i][para1][0])
            elif factor1 == False:
                data.append("*")
        return data

    def get_err(self,para):
        # test for the cases where the error */
        # represents the absolute value i.e. */
        # if negative or if there is a */
        # decimal point in string */
        psrD = self.Psrcard
        num = len(psrD)
        para1 = para.upper()
        err_int = []
        for i in range(num):
            factor1 = psrD[i].__contains__(para1)
            if factor1 == True:
                try:
                    #print(psrD[i][para1][1])
                    int(psrD[i][para1][1])
                    err_int.append(psrD[i][para1][1])
                except ValueError:
                    err_int.append("*")
                except IndexError:
                    err_int.append("*")
            elif factor1 == False:
                err_int.append("*")
        return err_int
    
    
    def get_mag(self,para):
        ''' Gets the magnitude of the error'''
        psrD = self.Psrcard
        Para = self.get_para(para) # get data of the para
        err_data = self.get_err(para) # get int err
        num = len(Para) # the number of pulsar
        mag = []
        for i in range(num):
            if Para[i] == "*":
                mag.append("*")
            elif err_data[i] == "*":
                mag.append("*")
            else:
                paralist = list(Para[i])
                if 'E' in paralist and '.'  in paralist:
                    magi1 =10**int(Para[i].split("E")[1])
                    num1 = len(paralist)
                    num2 = paralist.index('.')
                    num3 = paralist.index('E')
                    magi2 = 10**-(num1-num2-(num1-num3)-1)
                    magi = magi1*magi2
                    mag.append(magi)
                elif 'e' in paralist and '.'  in paralist:
                    magi1 =10**int(Para[i].split("E")[1])
                    num1 = len(paralist)
                    num2 = paralist.index('.')
                    num3 = paralist.index('E')
                    magi2 = 10**-(num1-num2-(num1-num3)-1)
                    magi = magi1*magi2
                    mag.append(magi)
                elif '.'  in paralist:
                    num1 = len(paralist)
                    num2 = paralist.index('.')
                    magi = 10**-(num1-num2-1)
                    mag.append(magi)
                elif 'E' in paralist:
                    magi =10**int(Para[i].split("E")[1])
                    mag.append(magi)
                elif 'e' in paralist:
                    magi =10**int(Para[i].split("e")[1])
                    mag.append(magi)
                else:
                    mag.append(1)
                    #print("there is something error:",i)
                    #print(psrD[i])
        return mag
    
    def get_para_err(self,para):
        err_data = self.get_err(para)
        err_mag = self.get_mag(para)
        err = []
        for i in range(len(err_mag)):
            if err_data[i] !="*" and err_mag[i] !="*":
                #print("wuhu",err_data[i],err_mag[i],type(err_data[i]))
                err_i = float(err_data[i])*float(err_mag[i])
                err.append(err_i)
            else:
                err.append("*")
        #print(len(err),len(err_mag))
        return err




    def get_raj(self):
        '''get raj '''
        Raj = self.get_para("RAJ")
        Decj = self.get_para("DECJ")
        elon = self.get_para("ELONG")
        elat = self.get_para("ELAT")
        
        # get sky coordinates from elong elat
        for i in range(len(Raj)):
            if Raj[i] == "*":
                if elon[i] != "*":
                #raii,decii = Co.convertEquatorial(float(elon[i]),float(elat[i]))
                    scii = BarycentricMeanEcliptic(float(elon[i])*aunits.deg,
                                    float(elat[i])*aunits.deg
                                     ).transform_to(ICRS())
                    RaJDnew = scii.ra.to('hourangle').to_string(sep=':', pad=True)
                    Raj[i] = RaJDnew
        return Raj
        
    def get_decj(self):
        '''get decj '''
        Raj = self.get_para("RAJ")
        Decj = self.get_para("DECJ")
        elon = self.get_para("ELONG")
        elat = self.get_para("ELAT")
        # get sky coordinates from elong elat
        for i in range(len(Decj)):
            if Decj[i] == "*":
                if elon[i] !="*":
                    #raii,decii = Co.convertEquatorial(float(elon[i]),float(elat[i]))
                    scii = BarycentricMeanEcliptic(float(elon[i])*aunits.deg,
                                    float(elat[i])*aunits.deg
                                     ).transform_to(ICRS())
                    DecJDnew = scii.dec.to_string(sep=':', pad=True, alwayssign=True)
                    Decj[i] = DecJDnew

        return Decj

    def get_rajd(self):
        '''
          get RAJD
          get Right ascension (J2000) (degrees)
          '''
        raj = self.get_raj()
        decj = self.get_decj()
        rajd = []
        for i in range(len(raj)):
            if raj[i] !="*":
                radec = raj[i]+' '+decj[i]
                scii = SkyCoord(radec, unit=(u.hourangle, u.deg))
                rajdii = round(scii.ra.degree,8)
                rajd.append(str(rajdii))
            else:
                rajd.append("*")
        return rajd
        
    def get_decjd(self):
        '''
          get DECJD
          get Declination (J2000) (degrees)
          '''
        raj = self.get_raj()
        decj = self.get_decj()
        decjd = []
        for i in range(len(raj)):
            if raj[i] !="*":
                radec = raj[i]+' '+decj[i]
                scii = SkyCoord(radec, unit=(u.hourangle, u.deg))
                decjdii = round(scii.dec.degree,8)
                decjd.append(str(decjdii))
            else:
                decjd.append("*")
        return decjd


        
    def get_elong(self):
        '''get decj '''
        RAJD = self.get_rajd()
        DECJD = self.get_decjd()
        elon = self.get_para("ELONG")
        elat = self.get_para("ELAT")
        for i in range(len(elon)):
            if elon[i] == "*":
                if RAJD[i] !="*" and DECJD[i] !="*":
                #radeg,decdeg = Co.HMS2deg(ra=Raj[i],dec=Decj[i])
                #print("radeg decdeg:",radeg,decdeg,"hms",Raj[i],Decj[i])
                #rarad = math.radians(round(radeg,3))
                #derad = math.radians(round(decdeg,3))
                #elonii,elatii = Co.convertEcliptic(rarad,derad)
                #print("elong,elat",elonii,elatii)
                    sc = SkyCoord(float(RAJD[i])*aunits.deg,
                                float(DECJD[i])*aunits.deg)
                    elon[i] = str(round(sc.barycentricmeanecliptic.lon.value,3))
                #elon[i]=str(elonii)
                

        return elon
        
    def get_elat(self):
        '''get decj '''
        RAJD = self.get_rajd()
        DECJD = self.get_decjd()
        elon = self.get_para("ELONG")
        elat = self.get_para("ELAT")
        for i in range(len(elat)):
            if elat[i] == "*":
                if RAJD[i] !="*" and DECJD[i] !="*":
                #radeg,decdeg = Co.HMS2deg(ra=Raj[i],dec=Decj[i])
                #print("radeg decdeg:",radeg,decdeg,"hms",Raj[i],Decj[i])
                #rarad = math.radians(round(radeg,3))
                #derad = math.radians(round(decdeg,3))
                #elonii,elatii = Co.convertEcliptic(rarad,derad)
                #print("elong,elat",elonii,elatii)
                    sc = SkyCoord(float(RAJD[i])*aunits.deg,
                                float(DECJD[i])*aunits.deg)
                    elat[i] = str(round(sc.barycentricmeanecliptic.lat.value,3))
                #elat[i]=str(elatii)

        return elat

    def get_dist(self):
        # Calculate dist
        # -- if dist_a exists then use dist_a
        # -- if PX exists then use 1/PX if PX is >3 sigma significance (updated June 3rd 2012: GH)
        # -- if dist_amn and dist_amx exist and dist_dm lies within boundary
        #   then use dist_dm else use the closest limit to dist_dm
        # - if dist_dm is not defined then use (dism_amn + dist_amx)/2
        # -- otherwise use dist_dm
        oneAU = 149597870.  # AU in km (from psrcat.h)
        onePC = 30.857e12   # 1 pc in km (from psrcat.h)
        psrD = self.Psrcard
        print("num1",len(psrD))
        DIST_DM = self.get_para("DIST_DM")
        DIST_A = self.get_para("DIST_A")
        DIST_AMN = self.get_para("DIST_AMN")
        DIST_AMX = self.get_para("DIST_AMX")
        num = len(psrD)
        PX = self.get_para("PX")
        PXerr = self.get_para_err("PX")
        for i in range(len(PXerr)):
            if PXerr[i] != "*":
                PXerr[i]=round(PXerr[i],4)
            
        
        DIST= []
        for i in range(num):
            fa0 = psrD[i].__contains__("DIST_A")
            fa1 = psrD[i].__contains__("PX")
            fa2 = psrD[i].__contains__("DIST_AMN")
            fa3 = psrD[i].__contains__("DIST_AMX")
            fa4 = psrD[i].__contains__("DIST_DM")
            if fa0 == True:
                DIST.append(DIST_A[i])
            elif fa1 == True:
                PXsigma = float(PX[i])/PXerr[i]
                if PXsigma >3:
                    DIST.append(str(round((oneAU/onePC)*(60.*60.*180)/(float(PX[i])*np.pi),3)))
                elif fa2 ==True and fa3==True:
                    if fa4 ==False:
                        DIST.append(str(round((float(DIST_AMN[i])+float(DIST_AMX[i]))/2,3)))
                    elif float(DIST_DM[i]) <= float(DIST_AMN[i]):
                        DIST.append(DIST_AMN[i])
                    elif float(DIST_DM[i])>=float(DIST_AMX[i]):
                        DIST.append(DIST_AMX[i])
                    elif fa4 ==True:
                        DIST.append(DIST_DM[i])
                    else:
                        print("something error1",i,psrD[i])
                elif fa4 ==True:
                    DIST.append(DIST_DM[i])
                else:
                    print("something error2")
            elif fa2 ==True and fa3==True:
                if fa4 ==False:
                    DIST.append(str(round((float(DIST_AMN[i])+float(DIST_AMX[i]))/2,3)))
                elif float(DIST_DM[i]) < float(DIST_AMN[i]):
                    DIST.append(DIST_AMN[i])
                elif float(DIST_DM[i])>float(DIST_AMX[i]):
                    DIST.append(DIST_AMX[i])
                else:
                    DIST.append(DIST_DM[i])
            elif fa4 ==True:
                DIST.append(DIST_DM[i])
            elif fa4 ==False:
                if fa2 ==True and float(DIST_DM[i]) < float(DIST_AMN[i]):
                    DIST.append(DIST_AMN[i])
                elif fa3 == True and float(DIST_DM[i])>float(DIST_AMX[i]):
                    DIST.append(DIST_AMX[i])
                else:
                    DIST.append("*")
            else:
                print("something wrong3")
                DIST.append("*")
        return DIST

    def get_gl(self):
        '''get galactic longitude '''
        RAJD = self.get_rajd()
        DECJD = self.get_decjd()
        DIST = self.get_dist()
        gl = []
        for i in range(len(RAJD)):
            if RAJD[i] !="*":
                if DIST[i] != "*":
                    sc = SkyCoord(float(RAJD[i])*aunits.deg, float(DECJD[i])*aunits.deg,
                        float(DIST[i])*aunits.kpc)
                else:
                    sc = SkyCoord(float(RAJD[i])*aunits.deg, float(DECJD[i])*aunits.deg)
                gl.append(str(sc.galactic.l.value))
            else:
                gl.append("*")
        #elon = self.get_para("ELONG")
        #elat = self.get_para("ELAT")
        #for i in range(len(Decj)):
         #   if Decj[i] == "*":
          #      raii,decii = Co.convertEquatorial(float(elon[i]),float(elat[i]))
           #     Raj[i] = raii
            #    Decj[i] = decii
        #gl = []
        #for j in range(len(Decj)):
         #   radeg,decdeg = Co.HMS2deg(ra=Raj[j],dec=Decj[j])
            #print("radeg decdeg:",radeg,decdeg,"hms",Raj[i],Decj[i])
          #  rarad = math.radians(round(radeg,3))
           # derad = math.radians(round(decdeg,3))
            #gljj,gbjj = Co.convertGalactic(rarad,derad)
            #gl.append(str(gljj))
            
        return gl

    def get_gb(self):
        '''get galactic latitude '''
        RAJD = self.get_rajd()
        DECJD = self.get_decjd()
        DIST = self.get_dist()
        gb = []
        for i in range(len(RAJD)):
            if RAJD[i] !="*":
                if DIST[i] != "*":
                    sc = SkyCoord(float(RAJD[i])*aunits.deg, float(DECJD[i])*aunits.deg,
                        float(DIST[i])*aunits.kpc)
                else:
                    sc = SkyCoord(float(RAJD[i])*aunits.deg, float(DECJD[i])*aunits.deg)
                gb.append(str(sc.galactic.b.value))
            else:
                gb.append("*")
        #Raj = self.get_para("RAJ")
        #Decj = self.get_para("DECJ")
        #elon = self.get_para("ELONG")
        #elat = self.get_para("ELAT")
        #for i in range(len(Decj)):
         #   if Decj[i] == "*":
          #      raii,decii = Co.convertEquatorial(float(elon[i]),float(elat[i]))
           #     Raj[i] = raii
            #    Decj[i] = decii
        #gb = []
        #for j in range(len(Decj)):
         #   radeg,decdeg = Co.HMS2deg(ra=Raj[j],dec=Decj[j])
            #print("radeg decdeg:",radeg,decdeg,"hms",Raj[i],Decj[i])
          #  rarad = math.radians(round(radeg,3))
           # derad = math.radians(round(decdeg,3))
            #gljj,gbjj = Co.convertGalactic(rarad,derad)
            #gb.append(str(gbjj))
            
        return gb

    def get_DMsinb(self):
        '''
        ‘Vertical’ component of DM: DM sin GB (cm−3 pc)
          '''
        DM = self.get_para("DM")
        gb = self.get_gb()
        DMsinb = []
        print("wohu")
        for i in range(len(DM)):
            if DM[i] != "*":
                if gb[i] != "*":
                    DMsini = float(DM[i])*np.sin(np.deg2rad(float(gb[i])))
                    DMsinb.append(str(DMsini))
                else:
                    DMsinb.append("*")
            else:
                DMsinb.append("*")
        return DMsinb

    def get_pmra(self):
        '''get PMRA
            if PMDEC and PMRA do not exit
            and PMELAT and PMELONG exit
            calculate PMDEC and PMRA
          '''
        pmra = self.get_para("PMRA")
        pmdec = self.get_para("PMDEC")
        elon = self.get_elong()
        elat = self.get_elat()
        pmelong = self.get_para("PMELONG")
        pmelat = self.get_para("PMELAT")
        
        for i in range(len(pmra)):
            if pmra[i] =="*":
                if pmelong[i] !="*" and pmelat[i] != "*":
                    sc =  BarycentricMeanEcliptic(
                            float(elon[i])*aunits.deg,
                            float(elat[i])*aunits.deg,
                            pm_lon_coslat=float(pmelong[i])*aunits.mas/aunits.yr,
                            pm_lat=float(pmelat[i])*aunits.mas/aunits.yr
                            ).transform_to(ICRS())
                    PMRAnew = sc.pm_ra_cosdec.value
                    PMDECnew = sc.pm_dec.value
                    pmra[i] = str(round(PMRAnew,4))
                    pmdec[i] = PMDECnew
                    
        return pmra
                
    def get_pmdec(self):
        '''get PMDEC
            if PMDEC and PMRA do not exit
            and PMELAT and PMELONG exit
            calculate PMDEC and PMRA
          '''
        pmra = self.get_para("PMRA")
        pmdec = self.get_para("PMDEC")
        elon = self.get_elong()
        elat = self.get_elat()
        pmelong = self.get_para("PMELONG")
        pmelat = self.get_para("PMELAT")
        
        pmdec_new = []
        for i in range(len(pmdec)):
            if pmdec[i] =="*":
                if pmelong[i] !="*" and pmelat[i] != "*":
                    sc =  BarycentricMeanEcliptic(
                        float(elon[i])*aunits.deg,
                        float(elat[i])*aunits.deg,
                        pm_lon_coslat=float(pmelong[i])*aunits.mas/aunits.yr,
                        pm_lat=float(pmelat[i])*aunits.mas/aunits.yr
                        ).transform_to(ICRS())
                    #PMRAnew = sc.pm_ra_cosdec.value
                    PMDECnew = str(round(sc.pm_dec.value,4))
                    #pmra[i] = PMRAnew
                    pmdec[i] = PMDECnew
                    #print("new pmra:",pmra[i],pmdec[i])
                    #pmdec_new.append(PMDECnew)
                #else:
                    #print("ohioh")
                 #   pmdec_new.append(pmdec[i])
            #else:
             #   pmdec_new.append(pmdec[i])
        #print(pmdec_new[:10])
        return pmdec
        
    def get_posepoch(self):
        '''get POSEPOCH
          if POSEPOCH is not exit
          take PEPOCH as POSEPOCH
          '''
        posepoch = self.get_para("POSEPOCH")
        pepoch = self.get_para("PEPOCH")
        for i in range(len(posepoch)):
            if posepoch[i] == "*":
                if pepoch[i] != "*":
                    posepoch[i] = pepoch[i]
        return posepoch
    

    def get_p0(self):
        '''get P0
          if P0 is not exit
          P0 = 1/F0
          '''
        P0 = self.get_para("P0")
        F0 = self.get_para("F0")
        
        for i in range(len(P0)):
            if P0[i] =="*":
                if F0[i] !="*":
                    P0[i] = str(1./float(F0[i]))
        return P0


    def get_f0(self):
        '''get F0
          if F0 is not exit
          P0 = 1/P0
          '''
        P0 = self.get_para("P0")
        F0 = self.get_para("F0")
        
        for i in range(len(P0)):
            if F0[i] =="*":
                if P0[i] !="*":
                    F0[i] = str(1./float(P0[i]))
        return F0
    
    def get_p1(self):
        '''
          get P1
          If P1 is not exit
          P1 = -(P0**2)*F1
          '''
        P0 = self.get_p0()
        P1 = self.get_para("P1")
        F1 = self.get_para("F1")
        for i in range(len(P1)):
            if P1[i] == "*":
                if F1[i] !="*":
                    P1[i]= str(-(float(P0[i])**2)*float(F1[i]))
        return P1
        
    def get_f1(self):
        '''
          get F1
          If F1 is not exit
          F1 = -(F0**2)*P1
          '''
        F0 = self.get_f0()
        P1 = self.get_para("P1")
        F1 = self.get_para("F1")
        for i in range(len(F1)):
            if F1[i] == "*":
                if P1[i] !="*":
                    F1[i]= str(-(float(F0[i])**2)*float(P1[i]))
        return F1

    def get_units(self):
        '''
          get Units
          if Units is not exit
          Units is TDB
          '''
        Units = self.get_para("Units")
        for i in range(len(Units)):
            if Units[i] == "*":
                Units[i] = "TDB"
        return Units
    
    def get_pb(self):
        '''
         get PB
         if PB is not exit
         PB = 1./(FB0*86400.)
         '''
        FB0 = self.get_para("FB0")
        PB = self.get_para("PB")
        for i in range(len(PB)):
            if PB[i] =="*":
                if FB0[i] !="*":
                    PB[i] = str(1./(float(FB0[i])*86400.))
        return PB
        
    def get_om(self):
        '''
          get OM
          '''
        EPS1 = self.get_para("EPS1")
        EPS2 = self.get_para("EPS2")
        OM  = self.get_para("OM")
        for i in range(len(OM)):
            if OM[i] =="*":
                if EPS1[i] != "*" and EPS2[i] != "*":
                    OMi = np.arctan2(float(EPS1[i]),float(EPS2[i]))*180.0/math.pi
                    OM[i] = str(np.mod(OMi+360., 360.))
        return OM
        
    def get_ecc(self):
        '''
          get ECC
          '''
        EPS1 = self.get_para("EPS1")
        EPS2 = self.get_para("EPS2")
        ECC = self.get_para("ECC")
        for i in range(len(ECC)):
            if ECC[i] =="*":
                if EPS1[i] != "*" and EPS2[i] != "*":
                    ECCi = np.sqrt(float(EPS1[i])**2+float(EPS2[i])**2)
                    if ECCi >0:
                        ECC[i] = str(ECCi)
        return ECC
                
    def solfunc(self,m2, sini, mf, m1):
        return (m1 + m2)**2 - (m2*sini)**3/mf

    def get_minmass(self):
    
        SINI_MIN = 1.0  # inclination for minimum mass
        SINI_MED = 0.866025403  # inclination of 60deg for median mass
        SINI_90 = 0.438371146   # inclination for 90% UL mass
        MASS_PSR = 1.35  # canonical pulsar mass (solar masses)
        Msun = GM_sun.value
        A1 = self.get_para("A1")
        PB = self.get_pb()
        for i in range(len(PB)):
            if PB[i] != "*":
                PB[i] = float(PB[i])*86400. # convert to sec
            if A1[i] != "*":
                A1[i] = float(A1[i])*c.value # convert to m
        MASSFN = []
        for i in range(len(A1)):
            if PB[i] != "*" and A1[i] != "*":
                MASSFNi = (4.*np.pi**2/Msun)*A1[i]**3/(PB[i]**2)
                MASSFN.append(MASSFNi)
            else:
                MASSFN.append("*")
        MINMASS = []
        for i in range(len(MASSFN)):
            if MASSFN[i] !="*":
                try:
                    MINMASSi = newton(self.solfunc, MASS_PSR,
                                        args=(SINI_MIN, MASSFN[i], MASS_PSR),
                                        maxiter=1000)
                    MINMASS.append(str(MINMASSi))
                except RuntimeError:
                    MINMASS.append("*")
            else:
                MINMASS.append("*")
        return MINMASS
                
    def get_medmass(self):
    
        SINI_MIN = 1.0  # inclination for minimum mass
        SINI_MED = 0.866025403  # inclination of 60deg for median mass
        SINI_90 = 0.438371146   # inclination for 90% UL mass
        MASS_PSR = 1.35  # canonical pulsar mass (solar masses)
        Msun = GM_sun.value
        A1 = self.get_para("A1")
        PB = self.get_pb()
        for i in range(len(PB)):
            if PB[i] != "*":
                PB[i] = float(PB[i])*86400. # convert to sec
            if A1[i] != "*":
                A1[i] = float(A1[i])*c.value # convert to m
        MASSFN = []
        for i in range(len(A1)):
            if PB[i] != "*" and A1[i] != "*":
                MASSFNi = (4.*np.pi**2/Msun)*A1[i]**3/(PB[i]**2)
                MASSFN.append(MASSFNi)
            else:
                MASSFN.append("*")
        MEDMASS = []
        for i in range(len(MASSFN)):
            if MASSFN[i] !="*":
                try:
                    MEDMASSi = newton(self.solfunc, MASS_PSR,
                                        args=(SINI_MED, MASSFN[i], MASS_PSR),
                                        maxiter=1000)
                    MEDMASS.append(str(MEDMASSi))
                except RuntimeError:
                    MEDMASS.append("*")
            else:
                MEDMASS.append("*")
        return MEDMASS

    def get_date(self):
        '''
          get Date of psr discovery publication
          '''
        psrD = self.Psrcard
        num = len(psrD)
        Date = []
        for i in range(num):
            factor1 = psrD[i].__contains__("PSRB")
            if factor1 == True:
                if len(list(psrD[i]["PSRB"])) >1:
                    da = list(psrD[i]["PSRB"][1])
                    da1= []
                    numi = ""
                    for i in range(len(da)):
                        if da[i].isdigit() ==True:
                            numi = numi+da[i]
                    da2 =  int(numi)
                    if  da2 < 68:
                        da2 = da2+2000
                    else:
                        da2 = da2+1900
                    Date.append(str(da2))
                else:
                    Date.append("*")
            else:
                if len(list(psrD[i]["PSRJ"])) >1:
                    da = list(psrD[i]["PSRJ"][1])
                    da1= []
                    numi = ""
                    for i in range(len(da)):
                        if da[i].isdigit() ==True:
                            numi = numi+da[i]
                    da2 =  int(numi)
                    if  da2 < 68:
                        da2 = da2+2000
                    else:
                        da2 = da2+1900
                    Date.append(str(da2))
                else:
                    Date.append("*")
        return Date

    def get_xx(self):
        '''
          get galactic XX
          '''
        DIST = self.get_dist()
        gl = self.get_gl()
        gb = self.get_gb()
        XX = []
        for i in range(len(DIST)):
            if DIST[i] !="*" and gl[i] !="*":
                gl_ra = math.radians(float(gl[i]))
                gb_ra = math.radians(float(gb[i]))
                xxi = round(float(DIST[i])*math.cos(gb_ra)*math.sin(gl_ra),3)
                XX.append(str(xxi))
            else:
                XX.append("*")
        return XX
        
    def get_yy(self):
        '''
          get galactic YY
          '''
        DIST = self.get_dist()
        gl = self.get_gl()
        gb = self.get_gb()
        YY = []
        for i in range(len(DIST)):
            if DIST[i] !="*" and gl[i] !="*":
                gl_ra = math.radians(float(gl[i]))
                gb_ra = math.radians(float(gb[i]))
                yyi = round(float(DIST[i])*math.cos(gb_ra)*math.cos(gl_ra+math.pi)+8.3,3)
                YY.append(str(yyi))
            else:
                YY.append("*")
        return YY
        
    def get_zz(self):
        '''
          get galactic ZZ
          '''
        DIST = self.get_dist()
        gl = self.get_gl()
        gb = self.get_gb()
        ZZ = []
        for i in range(len(DIST)):
            if DIST[i] !="*" and gl[i] !="*":
                gl_ra = math.radians(float(gl[i]))
                gb_ra = math.radians(float(gb[i]))
                zzi = round(float(DIST[i])*math.sin(gb_ra),3)
                ZZ.append(str(zzi))
            else:
                ZZ.append("*")
        return ZZ
        
    def get_rlum(self):
        '''
          Radio luminosity at 400 MHz (mJy kpc2)
          '''
        S400 = self.get_para("S400")
        DIST = self.get_dist()
        R_Lum = []
        for i in range(len(S400)):
            if S400[i] != "*" and DIST[i] != "*":
                R_Lum.append(str(float(S400[i])*float(DIST[i])**2))
            else:
                R_Lum.append("*")
        return R_Lum
        
    def get_rlum1400(self):
        '''
          Radio luminosity at 1400 MHz (mJy kpc2)
          '''
        S1400 = self.get_para("S1400")
        DIST = self.get_dist()
        R_Lum1400 = []
        for i in range(len(S1400)):
            if S1400[i] != "*" and DIST[i] != "*":
                R_Lum1400.append(str(float(S1400[i])*float(DIST[i])**2))
            else:
                R_Lum1400.append("*")
        return R_Lum1400
    
    def get_cage(self):
        '''
          get  Spin down age (yr)  of Psr : tau = P/(2*Pdot)
          '''
        braking_idx=3.0
        P0 = self.get_p0()
        P1 = self.get_p1()
        Age=[]
        for i in range(len(P0)):
            if P0[i] !="*" and P1[i] !="*":
                if  float(P1[i]) !=0.0:
                    agei = float(P0[i]) / (float(P1[i])*(braking_idx-1.0)) / (365.25*86400.0)
                    if agei >0:
                        Age.append(str(agei))
                    else:
                        Age.append("*")
                else:
                    Age.append("*")
            else:
                Age.append("*")
        return Age
                
    def get_bsurf(self):
        '''
          get Surface magnetic flux density (Gauss) : B = 3.2*10e19 *(P*Pdot)**(1/2)
          '''
        P0 = self.get_p0()
        P1 = self.get_p1()
        BSurf = []
        for i in range(len(P0)):
            if P0[i] !="*" and P1[i] !="*":
                if  float(P1[i]) >0.0:
                    #print(P0[i],P1[i])
                    bsurfi = 3.2e19*np.sqrt(float(P0[i])*float(P1[i]))
                    BSurf.append(str(bsurfi))
                else:
                    BSurf.append("*")
            else:
                BSurf.append("*")
        return BSurf

    def get_edot(self):
        '''
          get  Spin down energy loss rate (ergs/s)
          '''
        P0 = self.get_p0()
        P1 = self.get_p1()
        Edot = []
        for i in range(len(P0)):
            if P0[i] !="*" and P1[i] !="*":
                if  float(P1[i]) >0.0:
                    edoti = 4.0 * np.pi**2 * 1e45 * float(P1[i]) / float(P0[i])**3
                    Edot.append(str(edoti))
                else:
                    Edot.append("*")
            else:
                Edot.append("*")
        return Edot

    def get_edot2(self):
        '''
          get Energy flux at the Sun (ergs/kpc2/s)
          '''
        P0 = self.get_p0()
        P1 = self.get_p1()
        Edot2 = []
        DIST = self.get_dist()
        for i in range(len(P0)):
            if P0[i] !="*" and P1[i] !="*" and DIST[i] !="*":
                if  float(P1[i]) >0.0:
                    edot2i = 4.0*np.pi**2*1e45*((float(P1[i])/float(P0[i])**3)/float(DIST[i])**2)
                    Edot2.append(str(edot2i))
                else:
                    Edot2.append("*")
            else:
                Edot2.append("*")
        return Edot2

    def get_pmtot(self):
        '''
          get Total proper motion (mas/yr)
          '''
        PMRA = self.get_pmra()
        PMDEC = self.get_pmdec()
        PMTot = []
        for i in range(len(PMRA)):
            if PMRA[i] !="*" and PMDEC[i] != "*":
                pmtoti = np.sqrt(float(PMRA[i])**2+float(PMDEC[i])**2)
                PMTot.append(str(pmtoti))
            else:
                PMTot.append("*")
        return PMTot
        
    def get_vtrans(self):
        '''
          get Transverse velocity - based on DIST (km/s)
          '''
        PMTOT = self.get_pmtot()
        DIST = self.get_dist()
        VTrans = []
        for i in range(len(PMTOT)):
            if PMTOT[i] != "*" and DIST[i] !="*":
                vtransi = (float(PMTOT[i]) * np.pi / (1000.0*3600.0*180.0*365.25 *
                                86400.0))*3.086e16*float(DIST[i])
                VTrans.append(str(vtransi))
            else:
                VTrans.append("*")
        return VTrans

    def get_p1_i(self):
        '''
          get Period derivative corrected for Shklovskii (proper motion) effect
          '''
        P0 = self.get_p0()
        P1 = self.get_p1()
        DIST = self.get_dist()
        VTrans = self.get_vtrans()
        P1_i = []
        for i in range(len(P1)):
            if P0[i] !="*" and P1[i] !="*" and DIST[i]!="*" and VTrans[i] !="*":
                p1ii = ((float(P1[i])/1.0e-15) -
                            float(VTrans[i])**2 * 1.0e10 * float(P0[i]) /
                            (float(DIST[i]) * 3.086e6)/2.9979e10) * 1.0e-15
                P1_i.append(str(p1ii))

            else:
                P1_i.append("*")
        return P1_i

    def get_age_i(self):
        '''
          get  Spin down age from P1_i (yr)
          '''
        braking_idx=3.0
        P0 = self.get_p0()
        P1 = self.get_p1_i()
        Agei=[]
        for i in range(len(P0)):
            if P0[i] !="*" and P1[i] !="*":
                if  float(P1[i]) !=0.0:
                    agei = float(P0[i]) / (float(P1[i])*(braking_idx-1.0)) / (365.25*86400.0)
                    if agei >0:
                        Agei.append(str(agei))
                    else:
                        Agei.append("*")
                else:
                    Agei.append("*")
            else:
                Agei.append("*")
        return Agei

    def get_bsurf_i(self):
        '''
          get Surface magnetic dipole from P1_i (gauss) : B = 3.2*10e19 *(P*P1idot)**(1/2)
          '''
        P0 = self.get_p0()
        P1 = self.get_p1_i()
        BSurfi = []
        for i in range(len(P0)):
            if P0[i] !="*" and P1[i] !="*":
                if  float(P1[i]) >0.0:
                    #print(P0[i],P1[i])
                    bsurfi = 3.2e19*np.sqrt(float(P0[i])*float(P1[i]))
                    BSurfi.append(str(bsurfi))
                else:
                    BSurfi.append("*")
            else:
                BSurfi.append("*")
        return BSurfi

    def get_b_lc(self):
        '''
          get  Magnetic field at light cylinder
          '''
        P0 = self.get_p0()
        P1 = self.get_p1()
        B_LC= []
        for i in range(len(P0)):
            if P1[i] !="*" and P0[i] !="*":
                if float(P1[i]) >0. :
                    blci = 3.0e8*np.sqrt(float(P1[i]))*np.abs(float(P0[i]))**(-5./2.)
                    B_LC.append(str(blci))
                else:
                    B_LC.append("*")
            else:
                B_LC.append("*")
        return B_LC
        
        

    def get_item(self,item):
        """
        对一行转换为字典需要的key:value
        vlaue 为一个列表
        """
        #print(item)
        item = item.split()
        key = item[0]
        value = item[1:]
        return key,value
    
    

    #print(data[0].split())

    #print(Psrcard[0])

    



    #print(list)


if __name__ == '__main__':

    psrcat()

"""
def get_P0():


def get_P1():

"""

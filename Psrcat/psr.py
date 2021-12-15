#!/Users/persusx/anaconda3/bin/python
# version 1.1
# this sopftware is to get the value and parameter of psrcat.db
# Contact PersusXie@outlook.com if in doubt

import math
import numpy as np



def get_Jname(psrD):
    """
    psrD为psr卡片信息卡集合
    获取脉冲星的Jname
    """
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


def get_Bname(psrD):
    """
    psrD为psr卡片信息卡集合
    获取脉冲星的Bname
    """
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

def get_para(psrD,para):
    """
    psrD为psr卡片信息卡集合
    获取脉冲星的参数
    """
    num = len(psrD)
    data = []
    for i in range(num):
        factor1 = psrD[i].__contains__(para)
        if factor1 == True:
            data.append(psrD[i][para][0])
        elif factor1 == False:
            data.append("*")
    return data


f = open("psrcat.db","r")   #设置文件对象
data = []
line = f.readline()
line = line[:-1]
while line:             #直到读取完文件
    line = f.readline()  #读取一行文件，包括换行符
    line = line[:-1]     #去掉换行符，也可以不去
    if line == '':   ##判断去除空行
        print("please have fun")
        #data.append(line)
    elif line[0] != "#": ## 判断去除解释行
        #print(line)
        data.append(line)
f.close() #关闭文件

Psrcard = [] ## 创建PSR信息卡集合



def get_item(item):
    """
    对一行转换为字典需要的key:value
    vlaue 为一个列表
    """
    #print(item)
    item = item.split()
    key = item[0]
    value = item[1:]
    return key,value
    
card = {}
for i in range(len(data)):
    #card = {} ## 生成每个PSR的信息卡
    if data[i][0] != "@":
        key,value = get_item(data[i])
        card[key]=value
    else:
        Psrcard.append(card)
        card = {}

#print(data[0].split())

#print(Psrcard[0])

Jname = get_Jname(Psrcard)
#print(Jname)
Bname = get_Bname(Psrcard)
data = get_para(Psrcard,"PSRB")
print(Psrcard[1:5])
#for i in range(len(data)):
 #  print(data[i])



#print(list)




"""
def get_P0():


def get_P1():

"""

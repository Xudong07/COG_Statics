#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 14:12:58 2019

@author: duanxd
"""

# Sort sid and rid as .sts file

def trans(resname, stsname, newresname):
    sindx = dict()
    rindx = dict()
    with open(stsname, 'r') as fin:
        a = fin.readline()
        num = a.split()
        snum = int(num[0])
        rnum = int(num[1])
        print("snum and rnum", snum, rnum)
        for i in range(snum):
            a = fin.readline()
            b = a.split()
            sindx.update({int(b[0]) : i+1})
            print(b)
        for j in range(rnum):
            a = fin.readline()
            b = a.split()
            rindx.update({int(b[0]): j+1+snum})
    res = open(resname,'r')
    newres = open(newresname, 'w')
    try:
        while True:
            a = res.readline()
            if not a:
                break
            b = a.split()
            sc = sindx[int(b[0])]
            rc = rindx[int(b[1])]
            midt = float(b[2])
            newres.write(str([sc, rc, midt]).replace('[','').replace(']','\n').replace(',',' '))
    finally:
        newres.close()
        res.close()
            
                       
        

if __name__=="__main__":
    stsname = "tomo.stt"
    resname = "res.txt"
    newresname = "n.txt"
    trans(resname, stsname, newresname)

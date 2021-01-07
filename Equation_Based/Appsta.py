#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 16:20:53 2019

@author: duanxd
"""

'''
apply statics correction for .tt file
'''
def L_statics(sttname, ttname, ottname):
    ssta = dict()
    rsta = dict()
    with open(sttname,'r') as fstt:
        a = fstt.readline()
        num = a.split()
        nums = int(num[0])
        numr = int(num[1])
        for i in range(nums):
            a = fstt.readline()
            b = a.split()
            ssta.update({int(b[0]) : float(b[10])})
        for j in range(numr):
            a = fstt.readline()
            b = a.split()
            rsta.update({int (b[0]) : float(b[10])})
            
            

        
        
    ftt = open(ttname,'r')
    fott = open(ottname,'w')
    try:
        a = ftt.readline()
        fott.write(a)
        b = a.split()
        nums = int(b[0])
        for i in range(nums):
            a = ftt.readline()
            fott.write(a)
            b = a.split()
            numr = int(b[1])
            sv = ssta[int(b[0])]/1000
            a = ftt.readline()
            fott.write(a)
            for j in range(numr):
                a = ftt.readline()
                b = a.split()
                rv = rsta[int(b[0])]/1000
                oot = float(b[3]) + sv + rv
                fott.write(str([int(b[0]), float(b[1]), float(b[2]), oot]).replace('[', '').replace(']', '\n').replace(',',' '))
    finally:
        ftt.close()
        fott.close()

if __name__=='__main__':
    sttname = 'tomo.stt'
    ttname = 'syn.tt'
    ottname = 'T_sta.tt'
    L_statics(sttname, ttname, ottname)

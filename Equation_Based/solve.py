#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 22:25:40 2019

@author: duanxd
"""

'''
slove m
'''
import numpy as np
def G_set(npd, spr):
    size = npd.shape
    row = size[0]
    G = np.zeros((row,spr))
    for i in range(row):
        G[i,int(npd[i,0])-1] = 1
        G[i,int(npd[i,1])-1] = 1
    return G
def slovem(newresname,mfile, staname, nstaname, spr ):
    
    osta = open(staname, 'r')
    nsta = open(nstaname, 'w')
    newres = open(newresname, 'r')
    data = np.array([])
    try:
        while True:
            a = newres.readline()
            if not a:
                break
            b = a.split()
            sc = int(b[0])
            rc = int(b[1])
            midt = float(b[2])
            data = np.append(data,[sc, rc, midt])
    finally:
        newres.close()
    npd = data.reshape(-1,3)
    print(npd.shape)
    G = G_set(npd, spr)
    print(G.shape)
    GT = G.transpose()
    d= npd[:,2]
    L1 = np.zeros((spr, spr))
    for i in range(spr):
        L1[i,i] = 1
    
    alph1 = 0.001
    Gnew = np.vstack((G,alph1*L1))
    GTnew = Gnew.transpose()
    GTG = GTnew.dot(Gnew) 
    INVG = np.linalg.inv(GTG)
    m = (INVG.dot(GT)).dot(d)
    print(m.shape)
    
    mtxt = open(mfile, 'w')
    
    
    a = osta.readline()
    nsta.write(a)
    
    for i in range(spr):
        mtxt.write(str([m[i]]).replace('[','').replace(']','\n').replace(',',' '))
        
    
        a = osta.readline()
        b = a.split()
        nsta.write(str([int(b[0]), float(b[1]), float(b[2]), float(b[3]),float(b[4]),float(b[5]),float(b[6]),-m[i] ,-m[i] ,float(b[9])-m[i], float(b[10])-m[i], float(b[11]), float(b[12])]).replace('[','').replace(']','\n').replace(',',' '))
        
            
        
            
    mtxt.close()
    osta.close()
    nsta.close()
    
    
if __name__=="__main__":
    newresname = "n.txt"
    mfile = 'm.txt'
    staname = "tomo.stt"
    nstaname = "res.stt"
    spr = 1224
    slovem( newresname, mfile, staname, nstaname, spr)

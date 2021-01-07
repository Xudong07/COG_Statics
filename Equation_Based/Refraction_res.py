#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 20:24:11 2019

@author: duanxd
"""

"""
read .tt file and solve residual statics
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
def Refrac_res_cog(ttname, doff, resname, minoff, maxoff):
    '''
    read tt file in to a list
    '''
    '''
    @a dict to store data as offset
    '''
    ttcog = dict()
    for i in range(minoff, maxoff+doff, doff):
        ttcog.update({i:np.array([])})
        ttcog.update({-i:np.array([])})
    '''
    read tt file and store related information into dict ttcog
    '''
    with open(ttname, 'r') as fin:
        a = fin.readline()
        num = a.split()
        snum = int(num[0])
        print("snum:",  snum)
        for i in range(snum):
            a = fin.readline()
            num = a.split()
            sid = int(num[0])
            rnum = int(num[1])
            a = fin.readline()
            sinfo = a.split()
            sx = float(sinfo[0])
            for j in range(rnum):
                a = fin.readline()
                rinfo = a.split()
                rx = float(rinfo[1])
                '''
                sort as offset
                '''
                offset = rx - sx
                ioffset = round(round(offset)/doff) * doff
                if (abs(ioffset)>=minoff and abs(ioffset) <= maxoff):
                    rid = int(rinfo[0])
                    t = float(rinfo[3])*1000
                    ttcog[int(ioffset)] = np.append(ttcog[int(ioffset)],[sx, sid, rid, t])
                    
    for i in range(minoff, maxoff+doff, doff):
        print("offset", i)
        for j in [-1,1]:
            data = ttcog[int(j*i)]
            dsize = data.size
            print(dsize, j*i)
            if (dsize<=12):
                print("no data", j*i)
                continue
            npd = data.reshape(-1,4)
            pdd = pd.DataFrame(npd,columns=['sx','sid','rid','t'])
            pddx = pdd.sort_values(by='sx')
            findata = pddx.values
            s = findata[:,1]
            r = findata[:,2]
            t = findata[:,3]
           
            smooth_cog_REFRAC(s, r, t, resname)
            

# smooth_cog: inversion in common offset domain
def smooth_cog_REFRAC(s, r, t, resname):
    ddim = t.size
    mdim = ddim+ddim-1
    G = Construct_G(ddim, mdim)
    GT = G.transpose()
    d = (np.diff(t)).transpose()

    
    
    tque = np.zeros((2,ddim))
    tque[0,:] = t.transpose()
   


    '''
    L1 = np.zeros((ddim, mdim))
    L2 = np.zeros((ddim-2, mdim))
    for i in range(ddim):
        L1[i,i] = 1
    for j in range(ddim-2):
        L2[j,j+ddim] = -1
        L2[j,j+ddim+1] = 1
    dzero = np.zeros((ddim+ddim-2,))
    '''
    L1 = np.zeros((ddim, mdim))
    L2 = np.zeros((ddim-1, mdim))
    for i in range(ddim):
        L1[i,i] = 1
    for j in range(ddim-1):
        L2[j,j+ddim] = 1
    dzero = np.zeros((ddim+ddim-1,))
    alph1 = 0.01
    alph2 = 0.5
    Gnew = np.vstack((np.vstack((G,alph1*L1)),alph2*L2))
    GTnew = Gnew.transpose()
    dnew = np.hstack((d,dzero))
    GTG = GTnew.dot(Gnew) 
    INVG = np.linalg.inv(GTG)
    m = (INVG.dot(GT)).dot(d)
    ''' 
    print(Gnew.shape, dnew.shape, dzero.shape)
    print(m.shape, d.shape)
    tque[1,:] = (t-m[:ddim]).transpose()
    
    for i in range(2):
        plt.plot(tque[i,:])
        
    plt.legend(['ori','res'])  
    plt.show()
    '''
    with open(resname, 'a+') as fout:
        for i in range(ddim):
            fout.write(str([int(s[i]), int(r[i]), m[i]]).replace('[','').replace(']','\n').replace(',',' '))
            
            
            
def Construct_G(ddim, mdim):
    G = np.zeros((ddim-1, mdim))
    for i in range(ddim-1):
        G[i,i] = -1
        G[i,i+1] = 1
        G[i,i+ddim] = 1
    return G   
    
                
                    
    
                
                
  
    
    




if __name__=="__main__":
    ttname = 'T_sta.tt'
    resname = 'res.txt'
    doff = 20
    Refrac_res_cog(ttname, doff, resname, 3000, 4000)

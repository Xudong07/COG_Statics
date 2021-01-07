import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.signal import medfilt
 
def plot_cog(ttname, doff, minoff, maxoff, poffb, poffe, dpoff, staname, nstaname):
    '''
    read tt file in to a list
    '''
    
    #resolve sid and rid
    sstatics = dict()
    rstatics = dict()
    sstatics_tmp = dict()
    rstatics_tmp = dict()
    osta = open(staname, 'r')
    a = osta.readline()
    b = a.split()
    s_total_num = int(b[0])
    r_total_num = int(b[1])
    print('snum:', s_total_num, 'rnum:', r_total_num)
   
    for i in range(s_total_num):
        a = osta.readline()
        b = a.split()
        sstatics.update({int(b[0]):np.array([0])})
        sstatics_tmp.update({int(b[0]):np.array([])})
    for i in range(r_total_num):
        a = osta.readline()
        b = a.split()
        rstatics.update({int(b[0]):np.array([0])})
        rstatics_tmp.update({int(b[0]):np.array([])})
    osta.close()
    #print('sstatics', sstatics,'rstatics',rstatics)
    #print('sstatics_tmp', sstatics_tmp,'rstatics_tmp',rstatics_tmp)
    ttcog = dict()
    #ttcog is to store the tt information
    #the key is offset, the data is traveltime sorted as shot x
    for i in range(minoff, maxoff+doff, doff):
        ttcog.update({i:np.array([])})
        ttcog.update({-i:np.array([])})
        #print(i,-i)
    '''
    read tt file and store related information into dict ttcog
    '''
    with open(ttname, 'r') as fin:
        a = fin.readline()
        num = a.split()
        snum = int(num[0])
        #print("snum:",  snum)
        for i in range(snum):
            a = fin.readline()
            num = a.split()
            sid = int(num[0])
            rnum = int(num[1])
            #rnum is the number of receiver in this shot
            a = fin.readline()
            sinfo = a.split()
            sx = float(sinfo[0])
            for j in range(rnum):
                a = fin.readline()
                rinfo = a.split()
                rx = float(rinfo[1])
                '''
                sort as offset
                you can sort as shot, cmp
                '''
                offset = rx - sx
                ioffset = round(offset/doff) * doff
                #calculate the offset id, round is fine
                if (abs(ioffset)>=minoff and abs(ioffset) <= maxoff):
                    rid = int(rinfo[0])
                    t = float(rinfo[3])*1000
                    ttcog[int(ioffset)] = np.append(ttcog[int(ioffset)],[sx, rx, sid, rid, t])
                    

    
    for _ in range(10):       
        #zero the tmp statics
        print('sstatics_tmp', sstatics_tmp[60],'rstatics_tmp',rstatics_tmp[6101])
        for key in sstatics_tmp:
            sstatics_tmp[key]=np.array([])
        # statics for each shot
        for key in rstatics_tmp:
               rstatics_tmp[key] = np.array([])      
        print('sstatics', sstatics[60],'rstatics',rstatics[6101])
        #print('sstatics_tmp', sstatics_tmp[60],'rstatics_tmp',rstatics_tmp[6101])
        for ppoff in range(poffb, poffe+dpoff, dpoff):
            for i in range(2):
                if(i==0):
                    poff = ppoff
                else:
                    poff = -1*ppoff
                
                data = ttcog[int(poff)]
                dsize = data.size
                #print(dsize, int(poff))
                if (dsize<=12):
                    print("no data", int(poff))
                    continue
                
                
                npd = data.reshape(-1,5)
                t = npd[:,4]
                x = npd[:,2]
                #print(t.shape)
                # shift t
                #tt = t - np.average(t)
                tt = t-medfilt(t,31)
                #tt = t-np.median(t)
             
                # write t to sstatics
                for i in range(x.size):
                    #print(x[i])
                    sstatics_tmp[int(x[i])] = np.append(sstatics_tmp[int(x[i])], [tt[i]])
                
                x = npd[:,3]
                # write t to rstatics
                for i in range(x.size):
                    #print(x[i])
                    rstatics_tmp[int(x[i])] = np.append(rstatics_tmp[int(x[i])], [tt[i]])
                
        


        #resolve statics
        for key in sstatics:
            if (sstatics_tmp[key].size==0):
                sstatics_tmp[key] = 0
                continue
            sstatics_tmp[key] = np.average(sstatics_tmp[key])
            sstatics[key] = sstatics[key]+sstatics_tmp[key]
        for key in rstatics:
            if (rstatics_tmp[key].size==0):
                rstatics_tmp[key]=0
                continue
            rstatics_tmp[key] = np.average(rstatics_tmp[key])
            rstatics[key] = rstatics[key]+rstatics_tmp[key]



        # apply statics
        for ppoff in range(poffb, poffe+dpoff, dpoff):
            for i in range(2):
                if(i==0):
                    poff = ppoff
                else:
                    poff = -1*ppoff
                
                data = ttcog[int(poff)]
                dsize = data.size
                #print(dsize, int(poff))
                if (dsize<=12):
                    print("no data", int(poff))
                    continue
                npd = data.reshape(-1,5)
                t = npd[:,4]
                s_list = npd[:,2]
                r_list = npd[:,3]
                # shift t
                for j in range(t.size):
                    t[j] = t[j] - sstatics_tmp[int(s_list[j])] - rstatics_tmp[int(r_list[j])]
                
                


    #write statics
    osta = open(staname, 'r')
    nsta = open(nstaname, 'w')

    a = osta.readline()
    nsta.write(a)
    
    for i in range(s_total_num):
        a = osta.readline()
        b = a.split()
        total_s_sta = sstatics[int(b[0])][0]
        #print(total_s_sta)
        nsta.write(str([int(b[0]), float(b[1]), float(b[2]), float(b[3]),float(b[4]),float(b[5]),float(b[6]),-total_s_sta ,-total_s_sta ,float(b[9])-total_s_sta, float(b[10])-total_s_sta, float(b[11]), float(b[12])]).replace('[','').replace(']','\n').replace(',',' '))
        
    for i in range(r_total_num):
        a = osta.readline()
        b = a.split()
        total_r_sta=rstatics[int(b[0])][0]
        #print(total_r_sta)
        nsta.write(str([int(b[0]), float(b[1]), float(b[2]), float(b[3]),float(b[4]),float(b[5]),float(b[6]),-total_r_sta,-total_r_sta ,float(b[9])-total_r_sta, float(b[10])-total_r_sta, float(b[11]), float(b[12])]).replace('[','').replace(']','\n').replace(',',' '))
        
    osta.close()
    nsta.close()
    
    '''
    #plot
    for ppoff in range(poffb, poffe+5*dpoff, 5*dpoff):
        for i in range(2):
            if(i==0):
                poff = ppoff
            else:
                poff = -1*ppoff

            data = ttcog[int(poff)]
            dsize = data.size
            #print(dsize, int(poff))
            if (dsize<=12):
                print("no data", int(poff))
                return
            
            
            npd = data.reshape(-1,5)
            pdd = pd.DataFrame(npd,columns=['sx','rx','sid','rid','t'])
        # sort as keywork
            pddx = pdd.sort_values(by='sx')
            findata = pddx.values
            t = findata[:,4]
            x = findata[:,0]
            plt.plot(x, t,'b-', label = str(poff))
    #plt.legend(loc=[1,0])
    plt.xlabel('x (m)')
    plt.ylabel('Traveltime (ms)')
    #plt.ylim(1550,2000)
    plt.title('Common offset domain')
    plt.show()
    '''









            
            
  
    
                
                    
    
                
                
  
    
    




if __name__=="__main__":
    ttname = 'syn_with_tomostatcis.tt'
    doff = 20
    poffb = 2000
    poffe = 4000
    dpoff = 20
    staname = "tomo.stt"
    nstaname = "res.stt"
    plot_cog(ttname, doff, 0, 4000, poffb, poffe, dpoff,staname,nstaname)

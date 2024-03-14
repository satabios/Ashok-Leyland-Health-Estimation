# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 13:32:37 2020

@author: sathya
"""
import os
import glob,pickle,gzip
import pandas as pd
#from collections import OrderedDict
import math
import numpy as np
#%%
#
def reformatting(vec,model):
    pcode_dir = "/home/dese/Desktop/Ashok Leyland/pcode/"
    vehicle ='a'
    vehicle_data = "/home/dese/Desktop/Ashok Leyland/vehicle_data/"
   
    dataframe = []
    print("Reading Data")
    #%%
#    os.chdir(vehicle_data)
    for v in sorted(glob.glob(vehicle_data+"*.pklz")):
        if(v[13:-5] in vec):
            data = pickle.load(gzip.open(v,'rb'))['vDF']
            
            for date in data.keys():
                dataframe.append(data[date])
    data = pd.concat(dataframe,sort=True)   
        #    data['month'] = data.eventTime.dt.month
#        break
    vehicle =model
    #%%
#    os.chdir(pcode_dir)
    val = []
    label ={}
    for pkl in sorted(glob.glob(pcode_dir+"*.pklz")):
        la = pickle.load(gzip.open(pkl,'rb'))
        val.append(la)
    for l in range(len(val)):
        label.update(val[l])
    #    for date in data.keys():
    #        dataframe.append(data[date])
    #    data = pd.concat(dataframe,sort=True) 
    #    break
    
    #%%
    vehicle =vehicle[13:-5]
    if(os.path.exists('meta_data/'+vehicle+'/merged_pcode')==False):
        os.makedirs('meta_data/'+vehicle+'/merged_pcode')
    
    #%%
    error = ["P228C"]
    dmo,dmc = label['dmo'],label['dmc']
    
        
    print("Formatting Pcodes")
    #%%
    #dataframe = data['vDF']
    available_date = dataframe
    #print("Vehicle_Available_Data","start:",available_date[0],"end:",available_date[-1]) 
    #G417, PP5_ECOMET, G442
    #dataframe.drop(['eDate','ecuMake','eventTime','serialNumber'])
    
    dmo_g423 = dmo['P228C']['tdf']
    _olst = dmo_g423[dmo_g423.vName == 'G423'].sort_values(by=['eventTime'])
    
    dmc_g423 = dmc['P228C']['tdf']
    _clst = dmc_g423[dmc_g423.vName == 'G423'].sort_values(by=['eventTime'])
                
    pcode = pd.concat([_olst,_clst])
    pcode=pcode.sort_values(['eventTime'])
    
#    if(os.path.exists('meta_data/merged_pcode')==False):
#        os.mkdir('meta_data/merged_pcode')
        
        
    clst = ['eventTime','tripNumber','ecuSourceId','SPN_FMI','pCode','messageType','occurrenceCount']
    
    pcode = pcode[clst]
    pcode.eventTime = pd.to_datetime(pcode.eventTime, format='%Y-%m-%d %H:%M:%S')
    pcode.sort_values(['eventTime','occurrenceCount'],inplace=True)
    #pcode['month'] = pcode.eventTime.dt.month
    wlst = list(zip(pcode.eventTime,pcode.tripNumber,pcode.messageType,pcode.occurrenceCount,pcode.pCode))
    pickle.dump(pcode,gzip.open('meta_data/'+vehicle+'/merged_pcode/'+"wlst.pklz",'wb'))
    #%%
    print("Finding Vechicle Trips")
    ig = np.asarray(data.ignitionStatus.values)
    
    st_ind=0
    st_list =[]
    st =ig[0]
    for j in range(int(len(ig))):
    #    print("K:",j)
        if((ig[j]!=st)and(j-st_ind>1)):
            st_list.append([ig[j-1],st_ind,j-1])
            st_ind = j
            st = ig[j]
    st_list = np.asarray(st_list)
    inte = st_list[st_list[:,0]==1][:,1:]
    on_list = []
    for on in range(len(inte)):
        on_list.append([on, data.eventTime.iloc[inte[on]].values[0],
                        data.eventTime.iloc[inte[on]].values[1],
                        ])
    if(os.path.exists('meta_data/'+vehicle+'/on_list')==False):
        os.makedirs('meta_data/'+vehicle+'/on_list')
    
    #%%
    print("Abrating Paradoxial Pcodes")
    on = []
    oc =[]
    for ind,row in  pcode.iterrows():
        occ = row['eventTime']
        for l in range(len(on_list)):
            tripn, st, en,m = on_list[l][0], on_list[l][1], on_list[l][2], int(on_list[l][1].astype(str)[5:7])
            if(tripn not in oc):
                if(st<=occ):
                    if(en>=occ):
                                                 
                          on.append([row.tripNumber,st,en,m])
    vehicle_trips = []
    for l in range(len(on)):
        if(l==0):
            oc.append(on[l][0])
            vehicle_trips.append(on[l])
        elif(on[l][0] not in oc):
            oc.append(on[l][0])
            vehicle_trips.append(on[l])
        elif(len(oc)==1):
             vehicle_trips.append(on[l])
    
    month_wise = [] 
    trip_wise ={}
    month = []
    mnt= {}
    for p in range(len(vehicle_trips)):
        if(p==0):
            month.append(vehicle_trips[p][-1])
            month_wise.append(vehicle_trips[p][:-1])
            
            for j in range(p+1,len(vehicle_trips)):
                if(vehicle_trips[p][-1] ==vehicle_trips[j][-1]):
                    month_wise.append(vehicle_trips[j][:-1])
            trip_wise = {str(month_wise[i][0]):tuple(month_wise[i][1:]) for i in range(len(month_wise))}
            mnt[str(vehicle_trips[p][-1])] = trip_wise
            month_wise = [] 
            trip_wise ={}
            
        elif(vehicle_trips[p][-1] not in month):
            month.append(vehicle_trips[p][-1])
            month_wise.append(vehicle_trips[p][:-1])
            
            for j in range(p+1,len(vehicle_trips)):
                if(vehicle_trips[p][-1] ==vehicle_trips[j][-1]):
                    month_wise.append(vehicle_trips[j][:-1])
            trip_wise = {str(month_wise[i][0]):tuple(month_wise[i][1:]) for i in range(len(month_wise))}
            mnt[str(vehicle_trips[p][-1])] = trip_wise
            month_wise = [] 
            trip_wise ={}
            
                    
    pickle.dump(mnt,gzip.open('meta_data/'+vehicle+'/on_list/'+"wdict.pklz",'wb'))       
    pickle.dump(inte,gzip.open('meta_data/'+vehicle+'/on_list/'+"vehicle_on.pklz",'wb'))    
                          
    
    #%%
    print("Fetch Original Pcode Occurences")
    pcode_lst,open_lst,closed_lst = [],[],[]
    rlst = []
    ocsd_lst,ocds_lst,ocdd_lst = [],[],[]
    ccss_lst,ccsd_lst,ccds_lst,ccdd_lst = [],[],[],[]
    ooss_lst,oosd_lst,oodd_lst,oods_lst = [],[],[],[]
    init = True
    idx = 0 
    wdict = trip_wise
#    os.chdir(pcode_dir)
    wlst = pickle.load(gzip.open('meta_data/'+vehicle+'/merged_pcode/'+"wlst.pklz",'rb')).values.tolist()
    wdict = pickle.load(gzip.open('meta_data/'+vehicle+'/on_list/'+"wdict.pklz",'rb'))
    from itertools import chain
    for item in wlst:
        
        ikeys = [list(wdict[str(item[0].month)].keys()) ]
        ikeys =  list(chain(*ikeys))
            
        for ii in range(len(ikeys)):
            if ikeys[ii] == str(item[1]):
    #            ikey = ikeys[ii]
                iidx = ii
                break
            iidx = None
        if init:
            if item[2] == 'DM1_ALERT_CLOSED':
                rlst.append(item)
            else:
                tstart = item[0]
            init = False
        else:
            if item[2] == 'DM1_ALERT_CLOSED':
                if prev_item[2] == 'DM1_ALERT_OPEN':
                    if prev_item[1] == item[1]:
                        if prev_item[3] == ite[3]:
                            pcode_lst.append((tstamrt,item[0]))
                        else:
                            ocsd_lst.append((prev_item,item))
                    else:
                        if prev_item[3] == item[3]:
                            ocds_lst.append((prev_item,item))
                        else:
                            ocdd_lst.append((prev_item,item))
                else:
                    if prev_item[1] == item[1]:
                        if prev_item[3] == item[3]:
                            ccss_lst.append((prev_item,item))
                        else:
                            ccsd_lst.append((prev_item,item))
                    else:
                        if prev_item[3] == item[3]:
                            ccds_lst.append((prev_item,item))
                        else:
                            ccdd_lst.append((prev_item,item))
            else:
                if prev_item[2] == 'DM1_ALERT_CLOSED':
                    tstart = item[0]
                else:
                    if prev_item[1] == item[1]:
                        if prev_item[3] == item[3]:
                            ooss_lst.append((prev_item,item))
                        else:
                            pcode_lst.append((tstart,item[0]-pd.Timedelta(seconds=1)))
                            oosd_lst.append((prev_item,item))
                            tstart = item[0]
                    else:
                        if prev_item[3] != item[3]:
                            pcode_lst.append((tstart,wdict[str(prev_item[0].month)][pidx][str(pkey)][1]))
                            oodd_lst.append((prev_item,item))
                            tstart = item[0]
                        else:
    #                        if (item[0]-wdict[str(item[0].month)][iidx][str(ikey)][0]).total_seconds() > 300:
                            if (item[0]-wdict[str(item[0].month)][ikeys[iidx]][0]).total_seconds() > 300:
                                oods_lst.append((prev_item,item))
                                pcode_lst.append((tstart,wdict[str(prev_item[0].month)][str(pkey)][1]))
                                tstart = item[0]
                            else:
                                pass
        prev_item = item
    #    pkeys =  [list(k.keys()) for k in wdict[item[0].month]]
        pkeys = ikeys
        for pi in range(len(pkeys)):
            if pkeys[pi] == str(prev_item[1]):
                pkey = pkeys[pi]
                pidx = pi
                break
            pidx = None
    if(os.path.exists('meta_data/'+vehicle+'/pcode')==False):
        os.makedirs('meta_data/'+vehicle+'/pcode')
    
    pickle.dump(pcode_lst,gzip.open('meta_data/'+vehicle+'/pcode/'+'pcode_lst.pklz','wb'))         
            
    
            
    
    #%%
    print("Trimming Vehicle Data for Vehicle Status on")
    onx = []
    
    new_data = pd.DataFrame()
    
    for date in inte:
        st =date[0]
        ed =date[1]
        onx.append(data.iloc[st:ed+1])
    new_dataframe = pd.concat(onx,sort=True)
    
    high = np.zeros(len(new_dataframe)).reshape(len(new_dataframe))
    #    if((st<=h_st) and(ed>=h_ed)):
    #    for h in high:
    #        h_st =h[0]
    #        h_ed =h[1]
    #        split = ed-st
    #        if((st<=h_st) and(ed>=h_ed)):
    #            
    #            x = data.iloc[st:ed]
    #            y = np.zeros((split)).reshape(split)
    #            y[h_st:h_ed] =1
    #            x['status'] =y
    #            onx.append(x)
    #        else:
    #            x = data.iloc[st:ed]
    #            y = np.zeros((split)).reshape(split)
    #            x['status'] =y
    #            onx.append(x)
                
                
              
        
    
            
    print("Time Discarded:",(len(new_dataframe)-len(dataframe))/60)
    
    new_dataframe=new_dataframe.sort_values(by=['eventTime']).reset_index(drop=True)
    
    #%%
    print("Creating mask when Pcodes occur")
    from pandas import Timestamp
    hi_lst = []
    for hi in pcode_lst:
        st = hi[0]
        en = Timestamp(hi[1])
#        print(st,en)
        for i in range(len(new_dataframe)):
            if(new_dataframe.eventTime.iloc[i] == st):
#                print(i)
                for j in range(i+1,len(new_dataframe)):
                    if(new_dataframe.eventTime.iloc[j]==en):
                        high[i:j]=1
                        hi_lst.append([i,j])
                        break
                break
    
    #2019-06-03 15:27:13 2019-06-03 15:29:05
    #80429
    #2019-11-25 12:13:44 2019-11-25 12:47:28
    #3517716        
                 
                        #%%
    new_dataframe['status'] = high
    
    
    #%%
    print("Generating Health Measures")
    start = 0
    hlt=100
    health =np.ones_like(new_dataframe.status.values)
    for hi in hi_lst:
        st = hi[0]
        en = hi[1]
        diff = st-start
        if(diff>10):
            for i in range(start,st,int(st/100)):
                health[i:i+int(st/100)]=hlt
                hlt-=1
            start =hi[1]
            hlt=100
        else:
            start =hi[1]
    new_dataframe['health_linear'] = health
    
#    import matplotlib.pyplot as plt
#    plt.rcParams["figure.figsize"] = [16,9]
#    plt.plot(new_dataframe.health)
    new_dataframe['status'] = high



    for i in range(2,10,5):  #Change 10 to a range
        health =np.ones_like(new_dataframe.status.values)
        start = 0
        hlt=100     
        
        for hi in hi_lst:
            st = hi[0]
            en = hi[1]
            diff = st-start
            x=np.logspace(1,math.log(diff,i),100,base=i,dtype='int')
            
            if(diff>10):
                
                cl =0
                for ind in x:
                    if(cl !=ind):
                        health[start+cl:ind+start]=hlt
                        hlt-=1
                        cl=ind
              
                health[x[-1]:en]=0
                start =hi[1]
                hlt=100
            else:
                start =hi[1]
                
        new_dataframe['health_'+'decay_rate_'+str(i)] = health
    
    new_dataframe=new_dataframe.drop(['eventTime','serialNumber','ecuMake','eDate'],axis=1)
    new_dataframe=new_dataframe.dropna()
    
      
    #%%
    print("Saving the reformatted vehicle data")
    if(os.path.exists('meta_data/'+vehicle+'/data/')==False):
        os.makedirs('meta_data/'+vehicle+'/data/')
    
    pickle.dump(new_dataframe,gzip.open('meta_data/'+vehicle+'/data/'+'data.pklz','wb')) 
           
    return new_dataframe
 
            
            
                    #%%
#Formatting
#reformatting()

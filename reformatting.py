# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 16:19:18 2020

@author: sathy
"""

import argparse
# from tripwise_preprocess import reformatting
# from al_health import vehicle_health
import pandas as pd
import ipdb    

import os
import glob,pickle,gzip
import pandas as pd
#from collections import OrderedDict
import math
import numpy as np



import os
import glob,pickle,gzip
import pandas as pd
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt


def reformatting(vec,model,Rate,Error):
     print('\n\n\n')
     pcode_dir = "/media/313727ac-f148-4b50-9224-3f3986e68217/ashok_leyland/pcode/"
     vehicle ='a'
     vehicle_data = "/media/313727ac-f148-4b50-9224-3f3986e68217/ashok_leyland/vehicle_data/"

     dataframe = []
     print("Reading Data")

     #    os.chdir(vehicle_data)
     # ipdb.set_trace()
     for root, dirnames, filenames in os.walk(vehicle_data):
          for vech in dirnames:
               if(vech in vec):
                    for v in sorted(glob.glob(root+'/'+vech+"/"+"*.pklz")):
                         dataframe.append(pickle.load(gzip.open(v,'rb')))
               #
               # for date in data.keys():
               #      dataframe.append(data[date])
     data = pd.concat(dataframe)
     data = data.fillna(0)
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
     error = Error
     dmo,dmc = label['dmo'],label['dmc']


     print("Formatting Pcodes")
     #%%
     #dataframe = data['vDF']
     # available_date = dataframe
     #print("Vehicle_Available_Data","start:",available_date[0],"end:",available_date[-1])
     #G417, PP5_ECOMET, G442
     #dataframe.drop(['eDate','ecuMake','eventTime','serialNumber'])

     dmo_g423 = dmo[error]['tdf']
     _olst = dmo_g423[dmo_g423.vName == vec].sort_values(by=['eventTime'])

     dmc_g423 = dmc[error]['tdf']
     _clst = dmc_g423[dmc_g423.vName == vec].sort_values(by=['eventTime'])

     pcode = pd.concat([_olst,_clst])
     pcode=pcode.sort_values(['eventTime'])
     # print(pcode.iloc[0])

     #    if(os.path.exists('meta_data/merged_pcode')==False):
     #        os.mkdir('meta_data/merged_pcode')


     clst = ['eventTime','tripNumber','ecuSourceId','SPN_FMI','pCode','messageType','occurrenceCount']

     pcode = pcode[clst]
     pcode.eventTime = pd.to_datetime(pcode.eventTime, format='%Y-%m-%d %H:%M:%S')
     pcode.sort_values(['eventTime','occurrenceCount'],inplace=True)
     #pcode['month'] = pcode.eventTime.dt.month
     wlst = list(zip(pcode.eventTime,pcode.tripNumber,pcode.messageType,pcode.occurrenceCount,pcode.pCode))
     pickle.dump(pcode,gzip.open('meta_data/'+vehicle+'/merged_pcode/'+"wlst.pklz",'wb'), protocol=4)
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


     pickle.dump(mnt,gzip.open('meta_data/'+vehicle+'/on_list/'+"wdict.pklz",'wb'), protocol=4)
     pickle.dump(inte,gzip.open('meta_data/'+vehicle+'/on_list/'+"vehicle_on.pklz",'wb'), protocol=4)


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

     pcode_months = []
     vec_months = wdict.keys()

     for mnt in wlst:
          pcode_months.append(mnt[0].month)
     #    os.chdir(pcode_dir)
     wlst = pickle.load(gzip.open('meta_data/'+vehicle+'/merged_pcode/'+"wlst.pklz",'rb')).values.tolist() #pcode
     wdict = pickle.load(gzip.open('meta_data/'+vehicle+'/on_list/'+"wdict.pklz",'rb'))
     from itertools import chain
     # print(wlst)
     # ipdb.set_trace()
     for item in wlst:
          # print(item[0].month)
          if item[0] in pcode_months:
               ikeys = [list(wdict[str(item[0].month)].keys()) ]
               # print(ikeys)
               ikeys =  list(chain(*ikeys))
               # ipdb.set_trace()

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

     pickle.dump(pcode_lst,gzip.open('meta_data/'+vehicle+'/pcode/'+'pcode_lst.pklz','wb'), protocol=4)




     #%%
     print("Trimming Vehicle Data for Vehicle Status on")
     onx = []

     new_data = pd.DataFrame()
     # print(data.iloc[0:2])
     # ipdb.set_trace()
     for date in inte:
          st =int(date[0])
          ed =int(date[1])
          # print(st,ed)
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
     new_dataframe = (new_dataframe -np.min(new_dataframe))/(np.max(new_dataframe) -np.min(new_dataframe))
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
          if(diff>10):  #Change the time desired
               for i in range(start,st,int(st/100)):
                    health[i:i+int(st/100)]=hlt
                    hlt-=1
               start =hi[1]
               hlt=100
          else:
               start =hi[1]
     new_dataframe['health_linear'] = health

     # import matplotlib.pyplot as plt
     # plt.rcParams["figure.figsize"] = [16,9]
     # plt.plot(high)
     # new_dataframe['status'] = high


     o,c = Rate[0],Rate[1]
     for i in range(o,c,5):  #Change 10 or to a range within 100
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

        # import matplotlib.pyplot as plt
          plt.rcParams["figure.figsize"] = [16,9]
          # plt.plot(health)
          # plt.show()

          new_dataframe['health_'+'decay_rate_'+str(i)] = health

     # ipdb.set_trace()
     new_dataframe=new_dataframe.drop(['eventTime','ecuMake'],axis=1)
     # print(new_dataframe.columns)
     new_dataframe=new_dataframe.select_dtypes(exclude=['object'])
     # print(new_dataframe.columns)
     new_dataframe.dropna()
     # print(new_dataframe.columns)



     #%%
     print("Saving the reformatted vehicle data")

     # pa = pd.DataFrame()
     # pa ['health'] = health
     # pa['status'] = status
     # plt.rcParams["figure.figsize"] = [96,54]
     # new_dataframe.plot(subplots=True)
     # plt.show()

     for col in new_dataframe.columns:
          if len(new_dataframe[col].unique()) == 1:
               # print(col)
               new_dataframe.drop(col,inplace=True,axis=1)
     print("Numberof Parameters:",new_dataframe.shape[1])
     # ipdb.set_trace()
     # plt.plot(new_dataframe.status)
     #
     # plt.show()

     return new_dataframe

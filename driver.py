import argparse

# from tripwise_preprocess import reformatting
# from al_health import vehicle_health
import pandas as pd


import os
import glob,pickle,gzip
import pandas as pd
#from collections import OrderedDict
import math
import numpy as np


from sklearn.preprocessing import PowerTransformer
import os
import glob,pickle,gzip
import pandas as pd
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
from keras.layers import Dense, Input, Conv1D, LSTM, Activation, Dropout
from keras.models import Model, Sequential
from keras.callbacks import History
history = History()
#%%
from vehicle_health import vehicle_health
from reformatting import reformatting

 
    

from pandas_profiling import ProfileReport
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

if __name__=="__main__":


     parser = argparse.ArgumentParser(description='Vehicle Health Comprehension')
     parser.add_argument('--Vehicle_List', nargs='+', type=str,help='For master model enter all the vehcile models required')
     parser.add_argument('--Model',type=str,help='Depicts the vehicle model master/individual')
     parser.add_argument('--Decay_Rate', nargs='+', type=int,help='For master model enter all the vehcile models required')
     parser.add_argument('--Error_Code',type=str,help='For master model enter all the vehcile models required')
     # parser.add_argument('--Data',type=str,help='New Data File Name')
     args = vars(parser.parse_args())
     # args, leftovers = parser.parse_known_args()
     # if args.Data is not None:
     #      data = args['Model']
     #      model = load_model('/metadata/'+data+'.h5')
     #      data = np.asarray(pickle.load(gzip.open(data+'.pklz','rb')))
     #
     #
     #      scaler = MinMaxScaler(feature_range=(0, 1))
     #      x_data = scaler.fit_transform(data)
     #      x_data = np.expand_dims(x_data,axis=1)
     #
     #      prediction=[]
     #      for row in x_data.shape[0]:
     #           prediction.append(model.predict(x_data[row,:,:]))
     #      x_data = pd.DataFrame(x_data)
     #
     #      prof = ProfileReport(x_data)
     #  a    prof.to_file(output_file='output.html')

     # print(args)
     Vehicle_List = args['Vehicle_List']

     
     Model = args['Model']
     Rate = args['Decay_Rate']
     Error = args['Error_Code']

     # in
     frame = []
     for vehicle in Vehicle_List:
# jjj
         frame.append(reformatting(vehicle,Model,Rate,Error))
     data = pd.concat(frame, ignore_index=True)
     if(os.path.exists('meta_data/'+Model+'/data/')==False):
          os.makedirs('meta_data/'+Model+'/data/')
     pickle.dump(data,gzip.open('meta_data/'+Model+'/data/'+'data.pklz','wb'), protocol=4)
     # data = pickle.load(gzip.open("meta_data/"+Model+"/data/data.pklz",'rb'))
     model = vehicle_health(Model,data)
     if(os.path.exists('meta_data/'+Model+'/model/')==False):
          os.makedirs('meta_data/'+Model+'/model/')
     model.save('meta_data/'+Model+'/model/'+Model+'.h5')

     if(os.path.exists('meta_data/'+Model+'/inference/')==False):
          os.makedirs('meta_data/'+Model+'/inference/')



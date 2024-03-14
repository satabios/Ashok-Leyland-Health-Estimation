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
from keras.models import load_model



from pandas_profiling import ProfileReport
from keras.models import load_model
# from sklearn.preprocessing import MinMaxScaler

if __name__=="__main__":


    parser = argparse.ArgumentParser(description='Vehicle Health Retraining')
    parser.add_argument('--Vehicle_List', nargs='+', type=str,help='For master model enter all the vehcile models required')
    parser.add_argument('--Model',type=str,help='Depicts the vehicle model master/individual')
    parser.add_argument('--Decay_Rate', nargs='+', type=int,help='For master model enter all the vehcile models required')
    # parser.add_argument('--Data',type=str,help='New Data File Name')
    args = vars(parser.parse_args())

    Vehicle_List = args['Vehicle_List']
    Model = args['Model']
    Rate = args['Decay_Rate']
    #in
    frame = []
    for vehicle in Vehicle_List:
        # jjj
        frame.append(reformatting(vehicle,Model,Rate))
    data = pd.concat(frame, ignore_index=True)
    if(os.path.exists('meta_data/'+Model+'/data/')==False):
        os.makedirs('meta_data/'+Model+'/data/')
    pickle.dump(data,gzip.open('meta_data/'+Model+'/data/'+'data.pklz','wb'))
    # data = pickle.load(gzip.open("meta_data/"+Model+"/data/data.pklz",'rb'))
    vehicle_health(Model,data)

    if(os.path.exists('meta_data/'+Model+'/inference/')==False):
        os.makedirs('meta_data/'+Model+'/inference/')



    inp_shape = len(data.columns)
    #label_health_linear = data['health_linear'].values
    #label = data['health_decay_rate_2'].values
    label ={}
    for col in data.columns:
        if(col[:6]=='health'):
            label[col]= data[col]
    status = data['status']
    data=data.drop(list(label.keys()),axis=1)
    data=data.drop(['status'],axis=1)
    #
    x_data = data.to_numpy()
    #%%

    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range=(0, 1))
    x_data = scaler.fit_transform(x_data)

    #%%

    ##Transforms

    ##





    #%%
    # inp = Input(shape=(inp_shape,))
    # x = Dense(32,activation="relu")(inp)
    # # x = Dense(32,activation="relu")(x)
    # # x = Dense(28,activation="relu")(x)
    # x = Dense(16,activation="relu")(x)
    # # x = Dense(12,activation="linear")(x)
    # # x = Dense(16,activation="linear")(x)
    # # x = Dense(28,activation="relu")(x)
    # x = Dense(32,activation="relu")(x)
    # out = Dense(inp_shape)(x)
    # model = Model(inp,out)
    # model.compile(optimizer='adam', loss='mean_squared_error',metrics=['accuracy'])
    # #x = Dene(32,activation="relu")
    # #%%
    # model.fit(x_data,x_data, epochs=150, batch_size=1024, shuffle=True)#,
    #    # validation_data=(latent_test, latent_test))
    # #Model
    #%%
    # x_data.shape
    # label.shape


    # x_data.shape

    # label_lst ={}
    # for col in x_data.columns:
    #      if(col[:6]=='health'):
    #           label_lst[col]= x_data[col]
    #
    x_data = np.expand_dims(x_data,axis=1)
    # (10,n,1,1,21)

    # (samples, time, channels, rows, cols)
    # if data_format='channels_last' 5D tensor with shape: (samples, time, rows, cols, channels)
    #
    # pt = PowerTransformer()
    # pt.fit(data)
    # x_data = pt.transform(data)

    #%%
    print("Training the model")
    max_acc= -20
    health = 0
    for k,labl in label.items():

        labl=labl.to_numpy()
        rate_of_split = 0.9
        x_train, x_test, y_train,y_test = x_data[:int(x_data.shape[0]*rate_of_split),:,:],x_data[int(x_data.shape[0]*rate_of_split):,:,:], labl[:int(x_data.shape[0]*rate_of_split)],labl[int(x_data.shape[0]*rate_of_split):]

        #Model
    model = load_model('meta_data/'+Model+'/model/'+Model+'.h5')
    model.fit(x_train, y_train,
              batch_size=512,
              epochs=1,verbose=1,
              validation_data=(x_test, y_test),callbacks=[history])
        # hit.history
    if(history.history['val_accuracy'][0]>max_acc):
        max_acc = history.history['val_accuracy'][0]
    health = np.append(y_train,y_test)
    print("Saving the model")
    model.save(Model+'.h5')
    print(k,":",history.history['accuracy'][-1])

    data ['health'] = health
    data['status'] = status
    plt.rcParams["figure.figsize"] = [16,9]
    data.plot(subplots=True)
    plt.show()
    # return None





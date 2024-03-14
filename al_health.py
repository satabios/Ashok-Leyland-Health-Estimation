# -*- coding: utf-8 -*-



import os 
import glob,pickle,gzip
import pandas as pd
from collections import OrderedDict
import numpy as np    
import matplotlib.pyplot as plt

#%%
def vehicle_health(Model_Name,data):
#    vehicle ='G423'
#    os.chdir('C:/Users/sathya/Desktop/AL/Ashok Leyland')
#    data = pickle.load(gzip.open("meta_data/"+vehicle+"/data/data.pklz",'rb'))
    import matplotlib.pyplot as plt
    plt.rcParams["figure.figsize"] = [16,9]
    data.plot(subplots=True)
    plt.show()
    
    #%%
    
    #label_health_linear = data['health_linear'].values
    #label = data['health_decay_rate_2'].values
    label ={}
    for col in data.columns:
        if(col[:6]=='health'):
            label[col]= data[col]
            
    data=data.drop(list(label.keys()),axis=1)
    data=data.drop(['status'],axis=1)
    
    x_data = data.to_numpy()
    #%%
    
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range=(0, 1))
    x_data = scaler.fit_transform(x_data)
    
    #%%
    
    ##Autoencoder
        
    from keras.layers import Dense, Input, Conv1D, LSTM, Activation, Dropout
    from keras.models import Model, Sequential
    
    inp_shape = len(data.columns)
    
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
    # #%%
    # x_data.shape
    # label.shape
    #
    x_data = np.expand_dims(x_data,axis=1)
    # x_data.shape
    
    label_lst ={}
    for col in x_data.columns:
        if(col[:6]=='health'):
            label_lst[col]= x_data[col]
    # (10,n,1,1,21)
    
    # (samples, time, channels, rows, cols)
    # if data_format='channels_last' 5D tensor with shape: (samples, time, rows, cols, channels)
    
    #%%
            
    max_acc= 0
    
    for k,label in label_lst.items():
        
        label=label.to_numpy()
        rate_of_split = 0.9
        x_train, x_test, y_train,y_test = x_data[:int(x_data.shape[0]*rate_of_split),:,:],x_data[int(x_data.shape[0]*rate_of_split):,:,:], label[:int(x_data.shape[0]*rate_of_split)],label[int(x_data.shape[0]*rate_of_split):]
        
        #Model
        model = Sequential()
        
        model.add(LSTM(64,activation="relu"))
        
        # model.add(LSTM(16,activation="relu"))
        # model.add(BatchNormalization())
        
        # We project onto a single unit output layer, and squash it with a sigmoid:
        model.add(Dense(1))
        model.add(Activation('relu'))
        
        model.compile(loss='mean_squared_error',
                      optimizer='adam',
                      metrics=['accuracy'])
        model.fit(x_train, y_train,
                  batch_size=256,
                  epochs=30,
                  validation_data=(x_test, y_test))
        if(history.history['accuracy'][-1]>max_acc):
            max_acc = history.history['accuracy'][-1]
            model.save('/metadata/'+Model_Name+'.h5')
        print(k,":",history.history['accuracy'][-1])

#%%
#Validate the data

#h,s,f,t,p,z=1,1,1,1,1,1
#for i in range(len(label)):
#  if(label[i]==15):
#    h=i
#  elif(label[i]==14):
#    s=i
#  elif(label[i]==13):
#    f=i
#  elif(label[i]==12):
#    t=i
#  elif(label[i]==12):
#    z=i
#  elif(label[i]==11):
#    p=i
#  elif(label[i]==10):
#    r=i
#
#it =[h,s,f,t,z,p,r]
#for t in it:
#  print(model.predict(np.expand_dims(x_data[t,:,:],axis=0))[0])


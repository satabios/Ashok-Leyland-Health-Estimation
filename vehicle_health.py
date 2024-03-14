# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 16:18:07 2020

@author: sathy
"""
from keras.layers import Dense, Input, Conv1D, LSTM, Activation, Dropout
from keras.models import Model, Sequential
import matplotlib.pyplot as plt
from keras.callbacks import History
import  numpy as np
history = History()


def vehicle_health(Model_Name,data):

     label ={}
     for col in data.columns:
          if(col[:6]=='health'):
               label[col]= data[col]
     status = data['status']
     data=data.drop(list(label.keys()),axis=1)
     data=data.drop(['status'],axis=1)
     #
     x_data = data.to_numpy()

     x_data = np.expand_dims(x_data,axis=1)

     print("Training the model")
     max_acc= -20
     health = 0
     for k,labl in label.items():

          labl=labl.to_numpy()
          plt.plot(labl)
          plt.show()
          rate_of_split = 0.9
          x_train, x_test, y_train,y_test = x_data[:int(x_data.shape[0]*rate_of_split),:,:],x_data[int(x_data.shape[0]*rate_of_split):,:,:], labl[:int(x_data.shape[0]*rate_of_split)],labl[int(x_data.shape[0]*rate_of_split):]

          #Model
          model = Sequential()

          model.add(LSTM(64,activation="relu"))
          model.add(Dense(1))
          model.add(Activation('relu'))

          model.compile(loss='mean_squared_error',
                        optimizer='adam',
                        metrics=['accuracy'])
          model.fit(x_train, y_train,
                    batch_size=512,
                    epochs=1,verbose=1,
                    validation_data=(x_test, y_test),callbacks=[history])
          # hit.history
          if(history.history['val_accuracy'][0]>max_acc):
               max_acc = history.history['val_accuracy'][0]
               health = labl
          health = np.append(y_train,y_test)

          print(k,":",history.history['accuracy'][-1])
          #
     import pandas as pd
     x_data = pd.DataFrame(np.squeeze(x_data,axis=1))
     plt.rcParams["figure.figsize"] = [16,9]
     x_data['health']= health
     x_data['status']= status

     x_data.plot(subplots=True)
     plt.show()



     return model



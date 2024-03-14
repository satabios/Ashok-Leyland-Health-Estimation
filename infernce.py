from pandas_profiling import ProfileReport
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import pickle, gzip, argparse
import numpy as np
import pandas as pd


if __name__=="__main__":


    parser = argparse.ArgumentParser(description='Vehicle Health Estimation')

    parser.add_argument('--Model',type=str,help='Depicts the vehicle model master/individual')
    parser.add_argument('--Data',type=str,help='New Data File Name')
    args = vars(parser.parse_args())
    args, leftovers = parser.parse_known_args()

    model = args.Model
    data = args.Data
    model = load_model('meta_data/'+args.Model+'/model/'+model+'.h5')
    data = np.asarray(pickle.load(gzip.open('meta_data/'+args.Model+'/inference/'+'test.pklz','rb')).drop(['eventTime','serialNumber','ecuMake','eDate'],axis=1))


    scaler = MinMaxScaler(feature_range=(0, 1))
    x_data = scaler.fit_transform(data)
    x_data = np.expand_dims(x_data,axis=1)

    prediction=[]
    for row in range(x_data.shape[0]):
        prediction.append(model.predict((np.expand_dims(x_data[row,:,:],axis=0))))
    x_data = pd.DataFrame(np.squeeze(np.asarray(prediction)))

    prof = ProfileReport(x_data, minimal=True)
    prof.to_file(output_file='output.html')




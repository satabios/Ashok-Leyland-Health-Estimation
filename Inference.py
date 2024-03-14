


import argparse
import pickle,gzip
from  keras.models import load_model

if __name__=="__main__":


    parser = argparse.ArgumentParser(description='Vehicle Health Inferencing')
    # parser.add_argument('--Vehicle_List', nargs='+', type=str,help='For master model enter all the vehcile models required')
    parser.add_argument('--Model',type=str,help='Enter the Model that depicts the vehicle model master/individual')
    parser.add_argument('--Data',type=str,help='New Data File Name')
    args = vars(parser.parse_args())
    data = args['Data']
    Model = args['Model']

    data = pickle.load(gzip.open('Inference/'+data+'.pklz','rb')).sort_values(by=['eventTime']).reset_index(drop=True)

import pickle,gzip
import numpy as np
import glob
import argparse


parser = argparse.ArgumentParser(description='Vehicle Data Unification')
parser.add_argument('--Vehicle_List', nargs='+', type=str,help='Enter the vehicle to unify')
args = vars(parser.parse_args())
vehicles = args['Vehicle_List']

vehicle_data =[]
for vehicle in vehicles:
    for vec in sorted(glob.glob('vehicle_data/'+vehicle)):
        for fil in sorted(glob.glob(vec+'/*.pklz')):
            print(fil)
            # file = fil.split('/')[-1]
            vehicle_data.append(pickle.load(gzip.open(fil,'rb')))
    pickle.dump(vehicle_data,gzip.open('vehicle_data/'+vehicle+".pklz",'wb'))
    vehicle_data =[]
        # if(vec.split('/')[-1] is in ve)
        # for fil in sorted(glob.glob(vec))





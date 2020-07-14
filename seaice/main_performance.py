#!/usr/bin/env python3

import pickle
import numpy as np
import sea_ice_timer as si_py
import sea_ice_gt4py_timer as si_gt4py

BACKEND = ['python', 'numpy', 'gtx86', 'gtcuda']

IN_VARS = ["im", "km", "ps", "t1", "q1", "delt", "sfcemis", "dlwflx", \
           "sfcnsw", "sfcdsw", "srflag", "cm", "ch", "prsl1", "prslki", \
           "islimsk", "wind", "flag_iter", "lprnt", "ipr", "cimin", \
           "hice", "fice", "tice", "weasd", "tskin", "tprcp", "stc", \
           "ep", "snwdph", "qsurf", "snowmt", "gflux", "cmm", "chh", \
           "evap", "hflx"]

OUT_VARS = ["hice", "fice", "tice", "weasd", "tskin", "tprcp", "stc", \
            "ep", "snwdph", "qsurf", "snowmt", "gflux", "cmm", "chh", \
            "evap", "hflx"]

SCALAR_VARS = ["delt", "cimin", 'im', 'km']

TWOD_VARS = ['stc']
BOOL_VARS = ['flag_iter']
INT_VARS = ['islimsk']

GP = [32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]
FP = [0., 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 1]

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def init_dict(num_gridp, frac_gridp):
    d = {}
    sea_ice_point = load_obj('sea_ice_point')
    land_point = load_obj('land_point')
    
    num_sea_ice = int(num_gridp*frac_gridp)
    for var in IN_VARS:
        if var in SCALAR_VARS:
            d[var] = sea_ice_point[var]
        elif var in TWOD_VARS:
            d[var] = np.empty((num_gridp, 4))
            d[var][:num_sea_ice,:] = sea_ice_point[var]
            d[var][num_sea_ice:,:] = land_point[var]
        elif var in BOOL_VARS:
            d[var] = np.ones(num_gridp, dtype=bool)
            d[var][:num_sea_ice] = sea_ice_point[var]
            d[var][num_sea_ice:] = land_point[var]
        elif var in INT_VARS:
            d[var] = np.ones(num_gridp, dtype=np.int32)
            d[var][:num_sea_ice] = sea_ice_point[var]
            d[var][num_sea_ice:] = land_point[var]
        else:
            d[var] = np.empty(num_gridp)
            d[var][:num_sea_ice] = sea_ice_point[var]
            d[var][num_sea_ice:] = land_point[var]


    d['im'] = num_gridp

    return d


for implement in BACKEND:
    print('Implementation: ', implement)
    time = {}
    for frac in FP:
        time[float(frac)] = {}
        for grid_points in GP:
            print('Running ', grid_points, 'gridpoints with ', 100*frac, '% sea_ice.', end = '')
            in_dict = init_dict(grid_points, frac)
            if implement == 'python':
                out_data, elapsed_time = si_py.run(in_dict)
            else:
                out_data, elapsed_time = si_gt4py.run(in_dict, backend=implement)
            time[frac][float(grid_points)] = elapsed_time
    
    print(time)


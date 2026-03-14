from h5py import *
from numpy import *
from numpy.matlib import *
from matplotlib.pyplot import *
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from scipy.signal import find_peaks

def shape_extraction(path):
    if path[0:6]=='/media':
        pathITG=path
    else:
        pathITG='/media/test-Samsung-SSD/roma/Work/simulations/'+path
    struct=File(pathITG,'r')
    r_sc=array(struct["/data/var2d/generic/potsc/rsc"])
    z_sc=array(struct["/data/var2d/generic/potsc/zsc"])
    struct.close()
    return r_sc, z_sc

def phi_extraction(path):
    if path[0:6]=='/media':
        pathITG=path
    else:
        pathITG='/media/test-Samsung-SSD/roma/Work/simulations/'+path
    #pathITG='/media/test-Samsung-SSD/roma/ITG_from_Alexey/Simulations/'+path
    struct=File(pathITG,'r')
    phi_sc=array(struct["/data/var2d/generic/potsc/data"])
    phi_t=array(struct["/data/var2d/generic/potsc/time"])
    phi_s=array(struct["/data/var2d/generic/potsc/coord1"])
    phi_theta=array(struct["/data/var2d/generic/potsc/coord2"])
    struct.close()
    return phi_sc, phi_t,phi_s,phi_theta


def q_extraction(path):
    if path[0:6]=='/media':
        pathITG=path
    else:
        pathITG='/media/test-Samsung-SSD/roma/Work/simulations/'+path
    struct=File(pathITG,'r')
    q=array(struct["/equil/profiles/generic/q"])
    s=array(struct["/equil/profiles/generic/sgrid_eq"]) 
    struct.close()
    return s,q

def n_extraction(path):
    if path[0:6]=='/media':
        pathITG=path
    else:
        pathITG='/media/test-Samsung-SSD/roma/Work/simulations/'+path
    struct=File(pathITG,'r')
    nf=array(struct["/equil/profiles/fast/n_pic"])
    ni=array(struct["/equil/profiles/hydrogen/n_pic"])
    s=array(struct["/equil/profiles/hydrogen/s_prof"]) 
    struct.close()
    return s,ni, nf

def T_extraction(path):
    if path[0:6]=='/media':
        pathITG=path
    else:
        pathITG='/media/test-Samsung-SSD/roma/Work/simulations/'+path
    struct=File(pathITG,'r')
    Tf=array(struct["/equil/profiles/fast/t_pic"])
    Ti=array(struct["/equil/profiles/hydrogen/t_pic"])
    s=array(struct["/equil/profiles/hydrogen/s_prof"]) 
    struct.close()
    return s, Ti, Tf


def n_extraction_deut(path):
    if path[0:6]=='/media':
        pathITG=path
    else:
        pathITG='/media/test-Samsung-SSD/roma/Work/simulations/'+path
    struct=File(pathITG,'r')
    nf=array(struct["/equil/profiles/fast/n_pic"])
    ni=array(struct["/equil/profiles/deuterium/n_pic"])
    s=array(struct["/equil/profiles/deuterium/s_prof"]) 
    struct.close()
    return s,ni, nf

def T_extraction_deut(path):
    if path[0:6]=='/media':
        pathITG=path
    else:
        pathITG='/media/test-Samsung-SSD/roma/Work/simulations/'+path
    struct=File(pathITG,'r')
    Tf=array(struct["/equil/profiles/fast/t_pic"])
    Ti=array(struct["/equil/profiles/deuterium/t_pic"])
    s=array(struct["/equil/profiles/deuterium/s_prof"]) 
    struct.close()
    return s, Ti, Tf
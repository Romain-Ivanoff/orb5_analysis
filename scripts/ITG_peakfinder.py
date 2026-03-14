from h5py import *
from numpy import *
from numpy.matlib import *
from matplotlib.pyplot import *
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from scipy.signal import find_peaks
from scipy.stats import linregress
from numpy.random import randint
from matplotlib.ticker import ScalarFormatter
import os
import re

def phi_extraction(path):
    if path[0:6]=='/media':
        pathITG=path
    else:
        pathITG='/media/test-Samsung-SSD/roma/Work/simulations/'+path
    struct=File(pathITG,'r')
    phi_sc=array(struct["/data/var2d/generic/potsc/data"])
    phi_t=array(struct["/data/var2d/generic/potsc/time"])
    phi_s=array(struct["/data/var2d/generic/potsc/coord1"])
    phi_theta=array(struct["/data/var2d/generic/potsc/coord2"])
    struct.close()
    return phi_sc, phi_t,phi_s,phi_theta


def ITG_peak_finder_old(path, tmin=10000,tmax=30000):
    #Function to find the peak of the ITG by takinfg the average in poloidal plane 
    #By default it is suited for linear simulations, as it uses last time moment, but i_time can be used any
    phi_sc, phi_t,phi_s,phi_theta = phi_extraction(path)
    '''
    aver_phi=np.zeros((len(phi_t),len(phi_s)))
    for i_t in range (len(phi_t)):
        for i_s in range (len(phi_s)):
            aver_phi[i_t,i_s]=sum(phi_sc[i_t,:,i_s])
    i_s_max=(np.where(aver_phi[i_time]==max(aver_phi[i_time])))[0][0]
    '''

    #at time it=-1:
    i_time=-1
    phi_at_t=phi_sc[i_time]
    #phi_at_t_theta0=phi_at_t[0]
    phi_av=np.zeros(len(phi_s))
    for i_s in range (len(phi_s)):
        phi_av[i_s]=sum(abs(phi_at_t[:,i_s]))
    
    i_s_max=(np.where(phi_av==max(phi_av)))[0][0]
    
    #at time gap tmin tmax: 
    i_tmin=np.where((phi_t-tmin)==0)[0][0]
    i_tmax=np.where((phi_t-tmax)==0)[0][0]
    phi_t_slice=phi_sc[i_tmin:i_tmax]


    for i_s in range (len(phi_s)):
            phi_av[i_s]=sum(abs(phi_t_slice[:,:,i_s]))
    i_s_max=(np.where(phi_av==max(phi_av)))[0][0]

    return i_s_max
 
def ITG_peak_finder(path, tmin=None, tmax=None, smin=None,smax=None):
    #Function to find the peak of the ITG by takinfg the average in poloidal plane 
    phi_sc, phi_t,phi_s,phi_theta = phi_extraction(path)
    i_tmin,i_tmax,=0,0
    if tmin!=None:
        i_tmin=np.argmin(np.abs(phi_t-tmin))
    if tmax!=None:
        i_tmax=np.argmin(np.abs(phi_t-tmax))

    aver_phi_in_t=np.zeros(len(phi_s))
    
    for i_s in range (len(phi_s)):
        aver_phi_in_t[i_s]=sum(abs(phi_sc[i_tmin:i_tmax,:,i_s]))
    aver_phi_in_t=aver_phi_in_t[smin:smax]
    i_s_max=argmin(abs(aver_phi_in_t-max(aver_phi_in_t[smin:smax])))
    #print(i_s_max)
    return i_s_max

def ITG_peak_s(path,tmin,tmax):
    struct=File(path,'r')
    phi_s=array(struct["/data/var2d/generic/potsc/coord1"])
    struct.close()
    i_s=ITG_peak_finder(path,tmin, tmax)
    s=phi_s[i_s]
    return s
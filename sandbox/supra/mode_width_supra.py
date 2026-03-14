from h5py import *
from numpy import *
from numpy.matlib import *
from matplotlib.pyplot import *
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from scipy.signal import find_peaks
from matplotlib.ticker import ScalarFormatter

import os
import re
import sys
sys.path.append('/media/test-Samsung-SSD/roma/Work/orb5_analysis/scripts/')
from amplitude_phi import phi_extraction

sys.path.append('/media/test-Samsung-SSD/roma/Work/orb5_analysis/sandbox/supra/')
from psi_convertion import profiles_extraction

path_dt10_ntot7='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/shaped/n_scan/n100_dt10_ntot7/orb5_res.h5'
path_shaped='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/inputs/ogyropsi.h5_Roman_shaped_zerobeta'

phi_sc, phi_t,phi_s,phi_theta=phi_extraction(path_dt10_ntot7)
r_norm, s, psi, Te, ne=profiles_extraction(path_shaped)

phi_averaged=np.zeros_like(phi_s)
for ith in range(len(phi_theta)): 
    phi_averaged=phi_averaged+abs(phi_sc[-1,ith,:])
    #print(phi_averaged[100]-phi_sc[-1,ith,100])

plot(s,-np.gradient(Te,s)/np.min(np.gradient(Te,s)))
plot(phi_s,phi_averaged/max(phi_averaged))
#plot(phi_s,phi_sc[-1,0])

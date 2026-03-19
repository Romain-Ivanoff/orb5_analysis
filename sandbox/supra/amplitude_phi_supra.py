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
from amplitude_phi import *
#from potential_space import *
from gamma import gamma_box_slopes
from ITG_peakfinder import ITG_peak_finder
figure(figsize=(7, 6))

path_n110='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/noEP/toroidal_scan/high_n/n110_dt10_ntot7/orb5_res.h5'
path_n110_s_test='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/noEP/toroidal_scan/tests/n110_dt10_ntot7_s_test/orb5_res.h5'

path_200='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/noEP/toroidal_scan/high_n/n200_dt10_ntot7/orb5_res.h5'
path_220='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/noEP/toroidal_scan/high_n/n220_dt10_ntot7/orb5_res.h5'
path_240='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/noEP/toroidal_scan/high_n/n240_dt10_ntot7/orb5_res.h5'
path_260='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/noEP/toroidal_scan/high_n/n260_dt10_ntot7/orb5_res.h5'

path_kin_n110_dt5_n7='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/noEP/ES_kin/res_test/n110_dt5_ntot7/orb5_res.h5'
path_kin_n110_dt10_n7='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/noEP/ES_kin/res_test/n110_dt10_ntot7/orb5_res.h5'
path_kin_n110_dt5_n8='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/noEP/ES_kin/res_test/n110_dt5_ntot8_high/orb5_res.h5'
path_kin_n110_dt10_n7_high='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/noEP/ES_kin/res_test/n110_dt10_ntot7_high/orb5_res.h5'
'''
amplitude_phi_max(path_n110_s_test,r's test')
amplitude_phi_max(path_n110,r'$n=110$')
amplitude_phi_max(path_200,r'$n=200$')
amplitude_phi_max(path_240,r'$n=240$')
amplitude_phi_max(path_260,r'$n=260$')
'''

amplitude_phi_max(path_kin_n110_dt5_n7,r'$dt5_n7$')
amplitude_phi_max(path_kin_n110_dt10_n7,r'$dt10_n7$')
amplitude_phi_max(path_kin_n110_dt10_n7_high,r'$dt10_n7_high$')
amplitude_phi_max(path_kin_n110_dt5_n8,r'$dt5_n8$')

grid()
legend(fontsize=14)
xlim(30000, 60000)
#ylim(1.2e-8, 5.5e-8)

ax = gca()
tight_layout()

gamma_dt5_n7=(gamma_box_slopes(path_kin_n110_dt5_n7,i_s=0, tmin=35000, tmax=60000, n_boxes=4, min_pts_per_box=8,nsel_itg_loc='max_all_space'))[0]
gamma_dt10_n7=(gamma_box_slopes(path_kin_n110_dt10_n7,i_s=0, tmin=35000, tmax=60000, n_boxes=4, min_pts_per_box=8,nsel_itg_loc='max_all_space'))[0]
gamma_dt10_n7_high=(gamma_box_slopes(path_kin_n110_dt10_n7_high,i_s=0, tmin=35000, tmax=60000, n_boxes=4, min_pts_per_box=8,nsel_itg_loc='max_all_space'))[0]
gamma_dt5_n8=(gamma_box_slopes(path_kin_n110_dt5_n8,i_s=0, tmin=35000, tmax=60000, n_boxes=4, min_pts_per_box=8,nsel_itg_loc='max_all_space'))[0]

print(min(gamma_dt5_n8,gamma_dt10_n7_high,gamma_dt10_n7,gamma_dt5_n7)/max(gamma_dt5_n8,gamma_dt10_n7_high,gamma_dt10_n7,gamma_dt5_n7))
print(gamma_dt10_n7_high*10**5,gamma_dt10_n7*10**5,gamma_dt5_n7*10**5,gamma_dt5_n8*10**5)

#phi_sc, phi_t,phi_s,phi_theta=phi_extraction(path)
#plot_2D(path_dt10_ntot7, -1)
#print(ITG_peak_finder(path_dt10_ntot6, tmin=10000, tmax=60000))
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/supra/phi_convergence.pdf', dpi=300)



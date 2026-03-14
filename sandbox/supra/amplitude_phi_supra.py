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
from ITG_peakfinder import ITG_peak_finder
figure(figsize=(7, 6))
#path='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/test/n100_dt10/orb5_res.h5'
path_dt10_ntot6='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/shaped/test/n100_dt10_ntot6/orb5_res.h5'
path_dt10_ntot7='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/shaped/n_scan/n100_dt10_ntot7/orb5_res.h5'
path_dt5='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/shaped/test/n100_dt5/orb5_res.h5'


path_any='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/shaped/n_scan/resolution_test/n150_dt10_ntot7/orb5_res.h5'

path_n110='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/noEP/toroidal_scan/high_n/n110_dt10_ntot7/orb5_res.h5'
path_n110_s_test='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/noEP/toroidal_scan/tests/n110_dt10_ntot7_s_test/orb5_res.h5'

path_200_high_res='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/shaped/n_scan/n200_dt10_ntot7/orb5_res.h5'
path_200_low_res='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/shaped/n_scan/tests/low_res/n200_dt10_ntot7/orb5_res.h5'
path_200_high_res_new='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/shaped/n_scan/tests/res_test/n200_dt10_ntot7_mult/orb5_res.h5'
path_200_low_res_dm9='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/shaped/n_scan/tests/deltam_test/n200_dt10_ntot7_deltam9/orb5_res.h5'
path_260='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/noEP/toroidal_scan/high_n/n260_dt10_ntot7/orb5_res.h5'
path_n110_noFLR='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/shaped/noFLR/n110/orb5_res.h5'
path_alexey='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/noEP/toroidal_scans/lx180/n30/orb5_res.h5'
'''
ampltude_phi_legend(path_dt10_ntot6,r'$dt=10,\,n_{tot}=6.4\cdot10^6$',i_s=170)
ampltude_phi_legend(path_dt10_ntot7,r'$dt=10,\,n_{tot}=6.4\cdot10^6$,',i_s=170)
ampltude_phi_legend(path_dt5,r'$dt=5,\,n_{tot}=6.4\cdot10^7$',i_s=170)
'''
'''
ampltude_phi_legend(path_200_low_res,r'$n=200$, low res',i_s=170)
ampltude_phi_legend(path_200_low_res_dm9,r'$n=200, dm=9$, low res',i_s=170)
ampltude_phi_legend(path_200_high_res,r'$n=200$ high res',i_s=170)
ampltude_phi_legend(path_200_high_res_new,r'$n=200$ high res',i_s=170)
'''
ampltude_phi_legend(path_n110_s_test,r's test',i_s=170)
ampltude_phi_legend(path_n110,r'$n=110$',i_s=170)
ampltude_phi_legend(path_260,r'$n=260$',i_s=100)


'''
ampltude_phi_legend(path_dt10_ntot7,r'$140$',i_s=140)
ampltude_phi_legend(path_dt10_ntot7,r'$150$',i_s=150)
ampltude_phi_legend(path_dt10_ntot7,r'$160$',i_s=160)
ampltude_phi_legend(path_dt10_ntot7,r'$170$',i_s=170)
ampltude_phi_legend(path_dt10_ntot7,r'$180$',i_s=180)
ampltude_phi_legend(path_dt10_ntot7,r'$190$',i_s=190)
ampltude_phi_legend(path_dt10_ntot7,r'$200$',i_s=200)
ampltude_phi_legend(path_dt10_ntot7,r'$210$',i_s=210)
ampltude_phi_legend(path_dt10_ntot7,r'$220$',i_s=220)
ampltude_phi_legend(path_dt10_ntot7,r'$230$',i_s=230)
ampltude_phi_legend(path_dt10_ntot7,r'$240$',i_s=240)
ampltude_phi_legend(path_dt10_ntot7,r'$250$',i_s=250)
'''



grid()
legend(fontsize=14)
#xlim(0, 4)
#ylim(1.2e-8, 5.5e-8)

ax = gca()
'''
formatter = ScalarFormatter(useMathText=True)
formatter.set_scientific(True)      # use scientific notation
formatter.set_powerlimits((-8, 8))  # include your small range
formatter.set_useOffset(True)        # <--- enable offset to show exponent on top

ax.yaxis.set_major_formatter(formatter)
'''
tight_layout()


#phi_sc, phi_t,phi_s,phi_theta=phi_extraction(path)
#plot_2D(path_dt10_ntot7, -1)
#print(ITG_peak_finder(path_dt10_ntot6, tmin=10000, tmax=60000))
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/supra/phi_convergence.pdf', dpi=300)



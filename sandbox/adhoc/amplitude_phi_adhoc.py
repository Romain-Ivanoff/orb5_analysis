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

#__________________________________________
#compilers comparison

figure(figsize=(7, 6))
path_unst='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/temperature_scan/pitagora/unstable_eta/lin-n20-nH10-TH10/orb5_res.h5'

amplitude_phi_max(path_unst,'unst')

'''
ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/const_beta_scan/pitagora/old_compiler/lin-n20-nH10-TH00/orb5_res.h5','old',i_s=120)
ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/temperature_scan/pitagora/lin-n20-nH10-TH10/orb5_res.h5','new',i_s=120)
ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/test/lin-n20-nH10-TH10/orb5_res.h5','test',i_s=120)
'''

grid()
legend(fontsize=14)
#xlim(-0.5, 10)
#ylim(7*10**(-10),4.6*10**(-7))
tight_layout()
#savefig('../ITER/Pictures/phi_time_s_0.47_nH00_ITER.pdf')


'''
ampltude_phi_legend('Alexey-case/const-beta/pitagora/lin-n20-nH1-TH100/orb5_res.h5', r'$n_f=1\%,T_f=100$')
ampltude_phi_legend('Alexey-case/const-beta/pitagora/lin-n20-nH5-TH20/orb5_res.h5', r'$n_f=5\%,T_f=20$')
ampltude_phi_legend('Alexey-case/const-beta/pitagora/lin-n20-nH10-TH10/orb5_res.h5', r'$n_f=10\%,T_f=10$')
ampltude_phi_legend('Alexey-case/const-beta/pitagora/lin-n20-nH20-TH05/orb5_res.h5', r'$n_f=20\%,T_f=5$')
ampltude_phi_legend('Alexey-case/const-beta/pitagora/lin-n20-nH25-TH04/orb5_res.h5', r'$n_f=25\%,T_f=4$')
ampltude_phi_legend('Alexey-case/const-beta/pitagora/lin-n20-nH50-TH02/orb5_res.h5', r'$n_f=50\%,T_f=2$')
ampltude_phi_legend('Alexey-case/const-beta/pitagora/lin-n20-nH100-TH01/orb5_res.h5', r'$n_f=100\%,T_f=1$')
ampltude_phi_legend('Alexey-case/const-beta/pitagora/lin-n20-nH10-TH00/orb5_res.h5', r'$n_f=0,T_f=0$')
legend(fontsize=14)
grid()
tight_layout()
#savefig('../Alexey-case/gamma_ITG/const_beta/Pictures/phi_t_evol.pdf')
'''
1
'''

path_test='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/const_beta_scan/pitagora/new-compiler/lin-n20-nH1-TH100/orb5_res.h5'
print(ITG_peak_finder(path_test,i_time=-1))
'''

#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/pitagora/anisotropic/lin-n20-nH10-TH30/orb5_res.h5','new',i_s=120)
1





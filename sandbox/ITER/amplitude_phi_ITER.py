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


figure(figsize=(7, 6))
'''
ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_adiabatic/Old_compiler/dt20_4species/orb5_res.h5',r'$ES, n_f=0, dt=20$',i_s=100)
ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_adiabatic/Old_compiler/dt50_4species/orb5_res.h5',r'$ES, n_f=0, dt=50$',i_s=100)
ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/EM_kinetic/Old_compiler/dt20_4species_full/orb5_res.h5',r'$EM, n_f=0, dt=20$',i_s=100)


'''
#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/slowingdown-EP/ES/nH01_dt20/orb5_res.h5',r'$ES, adiabatic, n_f=1\%$',i_s=100)
#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_adiabatic/dt20_4species/orb5_res.h5',r'$ES, adiabatic, n_f=0$',i_s=100)
#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_adiabatic/dt20_4species_test/orb5_res.h5',r'$ES, adiabatic, n_f=0$ test',i_s=100)
#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_adiabatic/dt20_4species/orb5_res.h5',r'$ES, adiabatic, n_f=0$, 2nd ITG',i_s=46)
#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_kinetic/dt20_4species/orb5_res.h5',r'$ES, kinetic,\, m_i/m_e=400, n_f=0$, $dt=20$',i_s=100)
#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_kinetic/dt10_4species_m800/orb5_res.h5',r'$ES, kinetic,\, m_i/m_e=800, n_f=0$',i_s=100)
#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_kinetic/dt10_4species_m400/orb5_res.h5',r'$ES, kinetic,\, m_i/m_e=400, n_f=0$, $dt=10$',i_s=100)
#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_kinetic/dt20_4species/orb5_res.h5',r'$ES, kinetic, n_f=0$, TEM',i_s=297)
#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_kinetic/dt20_4species/orb5_res.h5',r'$ES, kinetic, n_f=0$, 2nd ITG',i_s=46)
path_ES_EP_adele='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/maxwellian-EP/T_prof/ES/nH01_dt20/orb5_res.h5'
path_ES_noEP_adele='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_adiabatic/dt20_4species/orb5_res.h5'
path_ES_noEP_kinele='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_kinetic/dt20_4species/orb5_res.h5'

path_EM_noEP='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/EM_kinetic/dt10_4species/orb5_res.h5'
path_EM_EP='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/maxwellian-EP/T_prof/EM/nH01_dt20/orb5_res.h5'
path_SD_test_1='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/slowingdown-EP/test/ES_dt30_nH01/orb5_res.h5'
i_s_ITG1=100
i_s_ITG2=46
i_s_TEM=297
ampltude_phi_legend(path_EM_noEP, 'EM, noEP',i_s_ITG1)
ampltude_phi_legend(path_EM_EP, 'EM, EP',i_s_ITG1)
ampltude_phi_legend(path_ES_noEP_kinele, 'ES kin, noEP',i_s_ITG1)
ampltude_phi_legend(path_ES_EP_adele, 'ES, EP',i_s_ITG1)
ampltude_phi_legend(path_ES_noEP_adele, 'ES, noEP',i_s_ITG1)
ampltude_phi_legend(path_SD_test_1, 'ES, SD',i_s_ITG1)


#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/EM_kinetic/dt10_4species/orb5_res.h5',r'$EM, n_f=0, dt10$',i_s=100)
#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/EM_kinetic/dt20_4species/orb5_res.h5',r'$EM, n_f=0, dt20$',i_s=100)

#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/EM_kinetic/Old_compiler/dt10_4species_short/orb5_res.h5',r'$EM, n_f=0, dt10$',i_s=100)
#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/EM_kinetic/dt10_4species/orb5_res.h5',r'$EM, n_f=0$, dt10 test',i_s=100) 
#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_adiabatic/dt20_4species/orb5_res.h5',r'$ES, adiabatic, n_f=0$, 2nd ITG',i_s=46)


'''
ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/slowingdown-EP/EM/nH01_dt20/orb5_res.h5',r'$EM, n_f=1\%$',i_s=100)
ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/EM_kinetic/dt20_4species/orb5_res.h5',r'$EM, n_f=0$',i_s=100)
'''
#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/EM_kinetic/dt20_4species_full/orb5_res.h5',r'$EM, n_f=0$',i_s=100)
#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/slowingdown-EP/EM/nH01_dt20_full/orb5_res.h5',r'$EM, n_f=1\%$',i_s=100)
#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/maxwellian-EP/T_prof/ES/nH01_dt20/orb5_res.h5',r'$ES, adiabatic, n_f=1\%$',i_s=100)

#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/slowingdown-EP/EM_dt20_nH01/orb5_res.h5',r'$EM, n_f=1\%$',i_s=100)

grid()
legend(fontsize=14)
#xlim(-0.5, 10)
#ylim(7*10**(-10),4.6*10**(-7))

#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/ITER/slowingdown/potential/phi_time_s_0.47_ITER.pdf')

#savefig('../Alexey-case/space_profiles/Pictures/phi_t_evol.pdf')


#Detecting the s coordinates of the modes
path_ES_EP_adele='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/slowingdown-EP/ES/nH01_dt20/orb5_res.h5'
path_ES_noEP_adele='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_adiabatic/dt20_4species/orb5_res.h5'
path_ES_noEP_kinele='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_kinetic/dt20_4species/orb5_res.h5'
path_EM_noEP='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/EM_kinetic/dt20_4species/orb5_res.h5'
path_EM_EP='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/slowingdown-EP/EM/nH01_dt20/orb5_res.h5'

#phi_space_plot(path_ES_noEP_kinele, -50)
#phi_space_plot(path_ES_noEP_adele, -50)
#phi_space_plot(path_ES_EP_adele, -50)
#phi_space_plot(path_EM_noEP, -1)
#TEM: i_s=297
#Main ITG i_s=100
#Second ITG i_s=46

#_____________________________________
#To see the KBM/TEM with OLD SIMS
'''
figure(figsize=(7, 6))

ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_adiabatic/Old_compiler/dt20_4species/orb5_res.h5',r'$ES, n_f=0, dt=20$',i_s=372)
ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_adiabatic/Old_compiler/dt50_4species/orb5_res.h5',r'$ES, n_f=0, dt=50$',i_s=372)
ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/EM_kinetic/Old_compiler/dt20_4species_full/orb5_res.h5',r'$EM, n_f=0, dt=20$',i_s=372)

grid()
legend(fontsize=14)
tight_layout()
#savefig('../ITER/Pictures/phi_time_s_0.69_nH00_ITER.pdf')
'''

#test slowing down
#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/maxwellian-EP/T_prof/ES/nH01_dt20/orb5_res.h5',r'Maxw',i_s=100)
#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/slowingdown-EP/test/ES_dt30_nH01/orb5_res.h5',r'$dt=30$',i_s=100)
#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/slowingdown-EP/test/ES_dt10_nH01/orb5_res.h5',r'$dt=10$',i_s=100)
#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/slowingdown-EP/test/iso_ES_dt30_nH01/orb5_res.h5','iso SD',i_s=100)
#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/slowingdown-EP/test/quazi_iso_dt30/orb5_res.h5',r'$\sigma=3$',i_s=100)
#ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/slowingdown-EP/test/sym_ani/orb5_res.h5',r'$\xi=0$',i_s=100)
legend(fontsize=14)
tight_layout()
# savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/ITER/slowingdown/potential/phi_time_s_0.69_nH01_ITER_test_SD.pdf')
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/ITER/maxwellian/potential/ITER-EM-dt-conv.pdf')
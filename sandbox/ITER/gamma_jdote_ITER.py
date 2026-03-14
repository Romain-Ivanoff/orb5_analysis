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

from gamma_MPR import *
from gamma_MPR import gamma_MPR_av
path_ES_EP_adele='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/maxwellian-EP/T_prof/ES/nH01_dt20/orb5_res.h5'
path_ES_noEP_adele='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_adiabatic/dt20_4species/orb5_res.h5'
path_ES_noEP_kinele='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_kinetic/dt20_4species/orb5_res.h5'

path_EM_noEP='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/EM_kinetic/dt20_4species/orb5_res.h5'
path_EM_EP='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/maxwellian-EP/T_prof/EM/nH01_dt20/orb5_res.h5'
path_SD_test_1='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/slowingdown-EP/test/ES_dt30_nH01/orb5_res.h5'

tmin=100000
tmax=200000
tmin_EM=70000
tmax_EM=100000
tmin_SD,tmin_SD=165000, 200000
species=['hydrogen','neon','beryllium','fast']
species_noEP_adele=['hydrogen','neon','beryllium']
species_kinele=['hydrogen','neon','beryllium', 'electrons','fast']
species_kinele_noEP=['hydrogen','neon','beryllium', 'electrons']
gamma_ES_noEP_adele=gamma_MPR_av(path_ES_noEP_adele,species_noEP_adele, tmin, tmax)
gamma_ES_noEP_kinele=gamma_MPR_av(path_ES_noEP_kinele,species_kinele_noEP, tmin, tmax)
gamma_EM_noEP=gamma_MPR_av(path_EM_noEP,species_kinele_noEP, tmin_EM, tmax_EM)
gamma_ES_adele=gamma_MPR_av(path_ES_EP_adele,species, tmin, tmax)
gamma_EM_EP=gamma_MPR_av(path_EM_EP,species_kinele, tmin_EM, tmax_EM)

#print(gamma_EM_noEP)
#print(gamma_ES_noEP_adele)

fig,ax=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))
ax.yaxis.set_major_formatter(formatter)
it_min,it_max=1,-1

def total_contribution_plot():
#Total contribution:
    gamma_ES_noEP_adele_tot,err_ES_noEP_adele_tot=0,0
    for i in range (3):
        gamma_ES_noEP_adele_tot+=gamma_ES_noEP_adele[i,1]
        err_ES_noEP_adele_tot+=gamma_ES_noEP_adele[i,2]

    gamma_ES_noEP_kinele_tot,err_ES_noEP_kinele_tot=0,0
    gamma_EM_noEP_tot,err_EM_noEP_tot=0,0
    gamma_ES_adele_tot,err_ES_adele_tot=0,0
    for i in range (4):
        gamma_ES_noEP_kinele_tot+=gamma_ES_noEP_kinele[i,1]
        err_ES_noEP_kinele_tot+=gamma_ES_noEP_kinele[i,2]
        
        gamma_EM_noEP_tot+=gamma_EM_noEP[i,1]
        err_EM_noEP_tot+=gamma_EM_noEP[i,2]
        
        gamma_ES_adele_tot+=gamma_ES_adele[i,1]
        err_ES_adele_tot+=gamma_ES_adele[i,2]
    gamma_EM_EP_tot,err_EM_EP_tot=0,0
    for i in range (5):
        gamma_EM_EP_tot+=gamma_EM_EP[i,1]
        err_EM_EP_tot+=gamma_EM_EP[i,2]


    ax.errorbar(0,gamma_ES_noEP_adele_tot, err_ES_noEP_adele_tot, marker='o',capsize=5, label=r'$n_f=0\%$ ES adiabatic')
    #ax.errorbar(0,gamma_ES_noEP_kinele_tot, err_ES_noEP_kinele_tot, marker='o',capsize=5, label=r'$n_f=0\%$ ES kinetic')
    ax.errorbar(0,gamma_EM_noEP_tot, err_EM_noEP_tot, marker='o',capsize=5, label=r'$n_f=0\%$ EM')
    ax.errorbar(1,gamma_ES_adele_tot,err_ES_adele_tot, marker='o',capsize=5, label=r'$n_f=1\%$ Maxwellian, ES adiabatic')
    ax.errorbar(1,gamma_EM_EP_tot,err_EM_EP_tot, marker='o',capsize=5, label=r'$n_f=1\%$ Maxwellian, EM')
    return

def ions_contribution_plot():
#ions contribution:
    #ax.errorbar(0,gamma_ES_noEP_adele[0,1], gamma_ES_noEP_adele[0,2], marker='o',capsize=5, label=r'$n_f=0\%$ ES adiabatic')
    #ax.errorbar(0,gamma_ES_noEP_kinele[0,1], gamma_ES_noEP_kinele[0,2], marker='o',capsize=5, label=r'$n_f=0\%$ ES kinetic')
    #ax.errorbar(0,gamma_EM_noEP[0,1], gamma_EM_noEP[0,2], marker='o',capsize=5, label=r'$n_f=0\%$ EM')
    #ax.errorbar(1,gamma_ES_adele[0,1], gamma_ES_adele[0,2], marker='o',capsize=5, label=r'$n_f=1\%$ Maxwellian, ES adiabatic')
    #ax.errorbar(1,gamma_EM_EP[0,1], gamma_EM_EP[0,2], marker='o',capsize=5, label=r'$n_f=1\%$ Maxwellian, EM')
    return

def EP_contribution_plot():
#ions contribution:
    ax.errorbar(1,gamma_ES_adele[-1,1], gamma_ES_adele[-1,2], marker='o',capsize=5, label=r'$n_f=1\%$ Maxwellian, ES adiabatic')
    ax.errorbar(1,gamma_EM_EP[-1,1], gamma_EM_EP[-1,2], marker='o',capsize=5, label=r'$n_f=1\%$ Maxwellian, EM')
    return

#total_contribution_plot()
EP_contribution_plot()

ax.grid()
ax.legend(fontsize=16)
ax.set_xlabel(r'$\tilde{n}_f, \%$', fontsize=18)
ax.set_ylabel(r"$\gamma/\Omega_{ci}$", fontsize=18)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/ITER/slowingdown/growthrate/ITER_gamma_MPR_ITG_all.pdf')

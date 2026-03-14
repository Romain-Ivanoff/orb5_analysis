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
import sys
sys.path.append('/media/test-Samsung-SSD/roma/Work/orb5_analysis/scripts/')
from temp_convertion import temperature_fin
from gamma import *

path_ES_EP_adele='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/maxwellian-EP/T_prof/ES/nH01_dt20/orb5_res.h5'
path_ES_noEP_adele='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_adiabatic/dt20_4species/orb5_res.h5'
path_ES_noEP_kinele_m400='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_kinetic/dt20_4species/orb5_res.h5'
path_ES_noEP_kinele_m400='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_kinetic/dt10_4species_m400/orb5_res.h5'
path_ES_noEP_kinele_m800='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_kinetic/dt10_4species_m800/orb5_res.h5'

path_EM_noEP='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/EM_kinetic/dt20_4species/orb5_res.h5'
path_EM_EP='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/maxwellian-EP/T_prof/EM/nH01_dt20/orb5_res.h5'
path_SD_test_1='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/slowingdown-EP/test/ES_dt30_nH01/orb5_res.h5'
tmin=20000
tmax=200000
tmin_EM=25000
tmax_EM=200000
i_s_ITG1=100
i_s_ITG2=46
i_s_TEM=297
    
#noEP:
slopes, stderrs = gamma_box_slopes(path_ES_noEP_adele,i_s_ITG1, tmin, tmax)
gamma_ITG_ES_adele_noEP,err_ITG_ES_adele_noEP=slopes.mean(),slopes.std()

slopes, stderrs = gamma_box_slopes(path_ES_noEP_kinele_m800,i_s_ITG1, tmin, tmax)
gamma_ITG_ES_kinele_noEP_m800,err_ITG_ES_kinele_noEP_m800=slopes.mean(),slopes.std()

slopes, stderrs = gamma_box_slopes(path_ES_noEP_kinele_m400,i_s_ITG1, tmin, tmax)
gamma_ITG_ES_kinele_noEP_m400,err_ITG_ES_kinele_noEP_m400=slopes.mean(),slopes.std()

slopes, stderrs = gamma_box_slopes(path_EM_noEP,i_s_ITG1, tmin_EM, tmax_EM)
gamma_ITG_EM_noEP,err_ITG_EM_noEP=slopes.mean(),slopes.std()


fig,ax=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))
ax.yaxis.set_major_formatter(formatter)

ax.errorbar(1/400,gamma_ITG_EM_noEP,err_ITG_EM_noEP, marker='s',mfc ='w',capsize=5, label=r'EM, $m_i/m_e=400$')
ax.errorbar(0,gamma_ITG_ES_adele_noEP,err_ITG_ES_adele_noEP, marker='o',capsize=5, label=r'ES, adiabatic')

#ax.errorbar(0,gamma_weakITG_EM_noEP,err_weakITG_EM_noEP, marker='s',mfc ='w',capsize=5, label=r'$n_f=0$ EM, 2nd ITG')

ax.errorbar(1/800,gamma_ITG_ES_kinele_noEP_m800,err_ITG_ES_kinele_noEP_m800, marker='s',capsize=5, label=r'ES kinetic, $m_i/m_e=800$')
ax.errorbar(1/400,gamma_ITG_ES_kinele_noEP_m400,err_ITG_ES_kinele_noEP_m400, marker='s',capsize=5, label=r'ES kinetic, $m_i/m_e=400$')
#ax.errorbar(1,gamma_weakITG_ES_adele_EP,err_weakITG_ES_adele_EP, marker='s',capsize=5, label=r'$n_f=1\%$ ES adiabatic 2nd ITG')

#ax.axhline(y=gamma_ITG_ES_adele_noEP, xmin=0, xmax=1, ls='--')
#ax.axhline(y=gamma_ITG_EM_noEP, xmin=0, xmax=1, ls='--', color='orange')
ax.plot(
    [1/1836, 1/1836],
    [2.35/100000, 3.23/100000],
    ls='--',
    color='black', label='realistic mass'
)
ax.grid()
ax.legend(fontsize=16)
ax.set_xlabel(r'$m_e/m_i$', fontsize=18)
ax.set_ylabel(r"$\gamma/\Omega_{ci}$", fontsize=18)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/ITER/slowingdown/growthrate/ITER_gamma_ITG_all.pdf')


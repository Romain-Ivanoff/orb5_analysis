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
path_ES_noEP_kinele='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_kinetic/dt20_4species/orb5_res.h5'

path_EM_noEP='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/EM_kinetic/dt10_4species/orb5_res.h5'
path_EM_EP='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/maxwellian-EP/T_prof/EM/nH01_dt20/orb5_res.h5'
path_SD_test_1='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/slowingdown-EP/test/ES_dt30_nH01/orb5_res.h5'

tmin=30000
tmax=200000
tmin_EM=40000
tmax_EM=100000
i_s_ITG1=100
i_s_ITG2=46
i_s_TEM=297
nsel_itg_loc='s'
#noEP:
slopes, stderrs = gamma_box_slopes(path_ES_noEP_adele,i_s_ITG1, tmin, tmax,nsel_itg_loc)
gamma_ITG_ES_adele_noEP,err_ITG_ES_adele_noEP=slopes, stderrs
'''
slopes, stderrs = gamma_box_slopes(path_ES_noEP_adele,i_s_ITG2, tmin, tmax,nsel_itg_loc)
gamma_weakITG_ES_adele_noEP,err_weakITG_ES_adele_noEP=slopes, stderrs
'''
slopes, stderrs = gamma_box_slopes(path_ES_noEP_kinele,i_s_ITG1, tmin, tmax,nsel_itg_loc,n_boxes=1)
gamma_ITG_ES_kinele_noEP,err_ITG_ES_kinele_noEP=slopes, stderrs

'''
slopes, stderrs = gamma_box_slopes(path_ES_noEP_kinele,i_s_ITG2, tmin, tmax,nsel_itg_loc)
gamma_weakITG_ES_kinele_noEP,err_weakITG_ES_kinele_noEP=slopes, stderrs

slopes, stderrs = gamma_box_slopes(path_ES_noEP_kinele,i_s_TEM, tmin, tmax,nsel_itg_loc)
gamma_TEM_ES_noEP,err_TEM_ES_noEP=slopes, stderrs
'''
slopes, stderrs = gamma_box_slopes(path_EM_noEP,i_s_ITG1, tmin, tmax,nsel_itg_loc)
gamma_ITG_EM_noEP,err_ITG_EM_noEP=slopes, stderrs
'''
slopes, stderrs = gamma_box_slopes(path_EM_noEP,i_s_ITG2, tmin, tmax,nsel_itg_loc)
gamma_weakITG_EM_noEP,err_weakITG_EM_noEP=slopes, stderrs
'''
#EP:

slopes, stderrs = gamma_box_slopes(path_ES_EP_adele,i_s_ITG1, tmin, tmax,nsel_itg_loc)
gamma_ITG_ES_adele_EP,err_ITG_ES_adele_EP=slopes, stderrs
'''
slopes, stderrs = gamma_box_slopes(path_ES_EP_adele,i_s_ITG2, tmin, tmax,nsel_itg_loc)
gamma_weakITG_ES_adele_EP,err_weakITG_ES_adele_EP=slopes, stderrs
'''
slopes, stderrs = gamma_box_slopes(path_EM_EP,i_s_ITG1, tmin_EM, tmax_EM,nsel_itg_loc)
gamma_ITG_EM_EP,err_ITG_EM_EP=slopes, stderrs
'''
slopes, stderrs = gamma_box_slopes(path_EM_EP,i_s_ITG2, tmin_EM, tmax_EM,nsel_itg_loc)
gamma_weakITG_EM_EP,err_weakITG_EM_EP=slopes, stderrs

slopes, stderrs = gamma_box_slopes(path_EM_noEP,i_s_TEM, 60000, 110000,nsel_itg_loc)
gamma_TEM_EM_noEP,err_TEM_EM_noEP=slopes, stderrs

slopes, stderrs = gamma_box_slopes(path_EM_EP,i_s_TEM, 60000, 110000,nsel_itg_loc)
gamma_TEM_EM_EP,err_TEM_EM_EP=slopes, stderrs
'''
#SD EPs, test____________________________________
slopes, stderrs = gamma_box_slopes(path_SD_test_1,i_s_ITG1, 165000, 200000,nsel_itg_loc)
gamma_ITG_ES_EP_SD1,err_ITG_ES_EP_SD1=slopes, stderrs

 
#MAIN ITG BRANCH____________________________________________________________
fig,ax=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))
ax.yaxis.set_major_formatter(formatter)
ax.errorbar(0,gamma_ITG_ES_adele_noEP,err_ITG_ES_adele_noEP, marker='o',capsize=5, label=r'$n_f=0\%$ ES')
#ax.errorbar(0,gamma_weakITG_ES_adele_noEP,err_weakITG_ES_adele_noEP, marker='o',capsize=5, label=r'$n_f=0\%$ ES adiabatic, 2nd ITG')
#ax.errorbar(0,gamma_weakITG_ES_kinele_noEP,err_weakITG_ES_kinele_noEP, marker='o',mfc ='w',capsize=5, label=r'$n_f=0\%$ ES kinetic, 2nd ITG')

#ax.errorbar(0,gamma_TEM_ES_noEP,err_TEM_ES_noEP, marker='x',capsize=5, label=r'$n_f=0\%$ ES kinetic, TEM')

ax.errorbar(0,gamma_ITG_EM_noEP,err_ITG_EM_noEP, marker='o',mfc ='w',capsize=5, label=r'$n_f=0\%$, EM')
#ax.errorbar(0,gamma_weakITG_EM_noEP,err_weakITG_EM_noEP, marker='s',mfc ='w',capsize=5, label=r'$n_f=0$ EM, 2nd ITG')
ax.errorbar(0,gamma_ITG_ES_kinele_noEP,err_ITG_ES_kinele_noEP, marker='o',mfc ='w',capsize=5, label=r'$n_f=0\%$ ES kinetic')



ax.errorbar(1,gamma_ITG_ES_adele_EP,err_ITG_ES_adele_EP, marker='s',capsize=5, label=r'$n_f=1\%$ Maxwellian, ES')
#ax.errorbar(1,gamma_weakITG_ES_adele_EP,err_weakITG_ES_adele_EP, marker='s',capsize=5, label=r'$n_f=1\%$ ES adiabatic 2nd ITG')

ax.errorbar(1,gamma_ITG_EM_EP,err_ITG_EM_EP, marker='s',mfc ='w',capsize=5, label=r'$n_f=1\%$ Maxwellian, EM')
ax.errorbar(1,gamma_ITG_ES_EP_SD1,err_ITG_ES_EP_SD1, marker='s',capsize=5, label=r'$n_f=1\%$ slowingdown, ES')

#print((gamma_ITG_ES_adele_noEP-gamma_ITG_ES_adele_EP)/gamma_ITG_ES_adele_noEP)
#print((gamma_ITG_EM_noEP-gamma_ITG_EM_EP)/gamma_ITG_EM_noEP)
ax.axhline(y=gamma_ITG_ES_adele_noEP, xmin=0, xmax=1, ls='--')
ax.axhline(y=gamma_ITG_EM_noEP, xmin=0, xmax=1, ls='--', color='orange')
ax.grid()
ax.legend(fontsize=16)
ax.set_xlabel(r'$\tilde{n}_f, \%$', fontsize=18)
ax.set_ylabel(r"$\gamma/\Omega_{ci}$", fontsize=18)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/Pictures/linear_ITG/ITER/slowingdown/growthrate/ITER_gamma_ITG_kin.pdf')

'''
#WEAK ITG___________________________________________________________________
fig,ax1=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))
ax1.yaxis.set_major_formatter(formatter)
ax1.errorbar(0,gamma_weakITG_ES_adele_noEP,err_weakITG_ES_adele_noEP, marker='o',capsize=5, label=r'$n_f=0\%$ ES adiabatic')
ax1.errorbar(0,gamma_weakITG_ES_kinele_noEP,err_weakITG_ES_kinele_noEP, marker='o',mfc ='w',capsize=5, label=r'$n_f=0\%$ ES kinetic')

#ax1.errorbar(0,gamma_TEM_ES_noEP,err_TEM_ES_noEP, marker='x',capsize=5, label=r'$n_f=0\%$ ES kinetic, TEM')
ax1.errorbar(0,gamma_weakITG_EM_noEP,err_weakITG_EM_noEP, marker='s',mfc ='w',capsize=5, label=r'$n_f=0$ EM')

ax1.errorbar(1,gamma_weakITG_ES_adele_EP,err_weakITG_ES_adele_EP, marker='s',capsize=5, label=r'$n_f=1\%$ ES adiabatic')
ax1.errorbar(1,gamma_weakITG_EM_EP,err_weakITG_EM_EP, marker='s',mfc ='w',capsize=5, label=r'$n_f=1\%$ EM')


ax1.grid()
ax1.legend(fontsize=16)

ax1.set_xlabel(r'$\tilde{n}_f, \%$', fontsize=18)
ax1.set_ylabel(r"$\gamma/\Omega_{ci}$", fontsize=18)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/ITER/slowingdown/growthrate/ITER_gamma_ITG_harmonic.pdf')



#TEM_______________________________________________________________________

fig,ax2=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))
ax2.yaxis.set_major_formatter(formatter)
ax2.errorbar(0,gamma_TEM_ES_noEP,err_TEM_ES_noEP, marker='x',capsize=5, label=r'$n_f=0\%$ ES kinetic, TEM')
ax2.errorbar(0,gamma_TEM_EM_noEP,err_TEM_EM_noEP, marker='x',capsize=5, label=r'$n_f=0\%$ EM, TEM')
ax2.errorbar(1,gamma_TEM_EM_EP,err_TEM_EM_EP, marker='x',capsize=5, label=r'$n_f=1\%$ EM, TEM')

ax2.grid()
ax2.legend(fontsize=16)

ax2.set_xlabel(r'$\tilde{n}_f, \%$', fontsize=18)
ax2.set_ylabel(r"$\gamma/\Omega_{ci}$", fontsize=18)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
tight_layout()

#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/ITER/slowingdown/growthrate/ITER_gamma_TEM.pdf')
'''


''' 
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(7,6), gridspec_kw={'height_ratios': [1,1]})

formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))

# -------------------------
# Plot on both axes
# -------------------------
for ax in (ax1, ax2):
    ax.yaxis.set_major_formatter(formatter)

    ax.errorbar(0,gamma_ITG_ES_noEP_dt20 ,err_ITG_ES_noEP_dt20,mfc ='w', marker='o',capsize=5, label=r'$n_f=0\%$ ES, $dt=20$')
    ax.errorbar(0,gamma_ITG_ES_noEP_dt50 ,err_ES_noEP_dt50,mfc ='w', marker='o',capsize=5, label=r'$n_f=0\%$ ES, $dt=50$')
    ax.errorbar(0,gamma_ITG_EM_noEP_dt20 ,err_EM_noEP_dt20, marker='s',capsize=5, label=r'$n_f=0\%$ EM, $dt=20$')
    ax.errorbar(0,gamma_ITG_KBM_noEP_dt20 ,err_KBM_noEP_dt20, marker='o',capsize=5, label=r'KBM, EM, no EP, $dt=20$')

    ax.errorbar(1,gamma_ES_EP_dt20 ,err_ES_EP_dt20, marker='o',mfc ='w',capsize=5, label=r'$n_f=1\%$ ES, $dt=20$')
    ax.errorbar(1,gamma_EM_EP_dt20 ,err_EM_EP_dt20, marker='s',capsize=5, label=r'$n_f=1\%$ EM, $dt=20$')
    ax.errorbar(1,gamma_EM_EP_dt30 ,err_EM_EP_dt30, marker='s',capsize=5, label=r'$n_f=1\%$ EM, $dt=30$')

    ax.grid()

# -------------------------
# Zoom each y-axis
# -------------------------
ax1.set_ylim(6.5e-5, 7.5e-5)    # KBM region
ax2.set_ylim(1.95e-5, 2.35e-5)  # ITG region

# -------------------------
# Decorations
# -------------------------
ax2.set_xlabel(r'$\tilde{n}_f, \%$', fontsize=18)
ax1.set_ylabel(r"$\gamma/\Omega_{ci}$", fontsize=18)
ax2.set_ylabel(r"$\gamma/\Omega_{ci}$", fontsize=18)

# Add "break marks" to indicate discontinuity
ax1.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.tick_params(labeltop=False)  # don't show tick labels on top plot
d = .015  # size of diagonal lines
kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
ax1.plot((-d,+d), (-d,+d), **kwargs)        # top-left diagonal
ax1.plot((1-d,1+d), (-d,+d), **kwargs)      # top-right diagonal
kwargs.update(transform=ax2.transAxes)      # switch to the bottom axes
ax2.plot((-d,+d), (1-d,1+d), **kwargs)      # bottom-left diagonal
ax2.plot((1-d,1+d), (1-d,1+d), **kwargs)    # bottom-right diagonal

# Legend (o
'''

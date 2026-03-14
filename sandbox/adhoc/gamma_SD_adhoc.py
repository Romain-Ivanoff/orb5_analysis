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




base_path_TH='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/temperature_scan/pitagora/'
base_path_SD_iso='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/pitagora/isotropic/'
base_path_SD_aniso='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/pitagora/anisotropic/'
path_TH00='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/const_beta_scan/pitagora/lin-n20-nH10-TH00/orb5_res.h5'
#base_path_TH='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/temperature_scan/leonardo/gamma-comparison-SD'
base_path_TH='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/temperature_scan/pitagora/'
tmin=10000
tmax=30000
#TH, gamma_scan, err_scan=gamma_temp_scan(base_path_TH,i_s=160,nsel_max_itg=True, tmin=10000, tmax=30000, min_pts_per_box=8)
TH, gamma_scan, err_scan=gamma_temp_scan(base_path_TH,i_s=144,nsel_max_itg=False, tmin=tmin, tmax=tmax, min_pts_per_box=8)
TH_SD_iso, gamma_scan_SD_iso, err_scan_SD_iso=gamma_temp_scan(base_path_SD_iso,i_s=144,nsel_max_itg=False, tmin=tmin, tmax=tmax, min_pts_per_box=8,nl_slowingdown=True)
TH_SD_aniso, gamma_scan_SD_aniso, err_scan_SD_aniso=gamma_temp_scan(base_path_SD_aniso,i_s=144,nsel_max_itg=False, tmin=tmin, tmax=tmax, min_pts_per_box=8,nl_slowingdown=True)
144
slopes, stderrs =gamma_box_slopes(path=path_TH00,i_s=140, tmin=tmin, tmax=tmax, n_boxes=4, min_pts_per_box=8,nsel_max_itg=True)
TH00, gamma_0, err_0=0,slopes.mean(),slopes.std()

'''
TH_SD_fin_aniso=np.zeros(len(TH_SD_aniso))
TH_SD_fin_iso=np.zeros(len(TH_SD_iso))
for i in range(len(TH_SD_aniso)):
    TH_SD_fin_aniso[i]=temperature_fin(1,TH_SD_aniso[i]*5) ###TO CORRECT
for i in range(len(TH_SD_iso)):
    TH_SD_fin_iso[i]=temperature_fin(1,TH_SD_iso[i]*5) ###TO CORRECT
'''
fig,ax=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
#print(TH_SD_iso)
formatter.set_powerlimits((-3, 3))
ax.yaxis.set_major_formatter(formatter)
#ax.errorbar(TH00, gamma_0, err_0, marker='s',mfc ='w',capsize=5, label=r'$n_f=0$')

ax.errorbar(TH[0:-1], gamma_scan[0:-1], err_scan[0:-1], marker='s',mfc ='w',capsize=5, label=r'Maxwellian')
ax.errorbar(TH_SD_iso, gamma_scan_SD_iso, err_scan_SD_iso, marker='o',capsize=5, label=r'Isotropic SD')
ax.errorbar(TH_SD_aniso, gamma_scan_SD_aniso, err_scan_SD_aniso, marker='o',capsize=5, label=r'$\xi=-0.66,\,\sigma=0.22$')

ax.grid()
ax.legend(fontsize=16)

ax.set_xlabel(r'$T_{f}\,/T_i$', fontsize=18)
ax.set_ylabel(r"$\gamma/\Omega_{ci}$", fontsize=18)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
fig.tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/adhoc/slowingdown/growthrate/temperature_scan/gamma_SD_temp_scan.pdf')



def old():
    #OLD SD FROM LEONARDO________________________________
    base_path_TH='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/temperature_scan/Pitagora/new-compiler/'
    base_path_SD_iso='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/leonardo/isotropic/'
    base_path_SD_ksi03_sigma02='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/leonardo/anisotropic/TH-ksi-03-sigma02/'
    base_path_SD_ksi08_sigma01='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/leonardo/anisotropic/TH-ksi-08-sigma01/'
    base_path_SD_ksi08_sigma02='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/leonardo/anisotropic/TH-ksi-08-sigma02/'
    path_TH00='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/const_beta_scan/pitagora/lin-n20-nH10-TH00/orb5_res.h5'
    #base_path_TH='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/temperature_scan/leonardo/gamma-comparison-SD'
    base_path_TH='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/temperature_scan/pitagora/'
    tmin=10000
    tmax=30000
    #TH, gamma_scan, err_scan=gamma_temp_scan(base_path_TH,i_s=160,nsel_max_itg=True, tmin=10000, tmax=30000, min_pts_per_box=8)
    TH, gamma_scan, err_scan=gamma_temp_scan(base_path_TH,i_s=120,nsel_max_itg=True, tmin=tmin, tmax=tmax, min_pts_per_box=8)
    TH_SD_iso, gamma_scan_SD_iso, err_scan_SD_iso=gamma_temp_scan(base_path_SD_iso,i_s=120,nsel_max_itg=True, tmin=tmin, tmax=tmax, min_pts_per_box=8)
    TH_SD_ksi03_sigma02, gamma_scan_SD_ksi03_sigma02, err_scan_SD_ksi03_sigma02=gamma_temp_scan(base_path_SD_ksi03_sigma02,i_s=120,nsel_max_itg=True, tmin=tmin, tmax=tmax, min_pts_per_box=8)
    TH_SD_ksi08_sigma01, gamma_scan_SD_ksi08_sigma01, err_scan_SD_ksi08_sigma01=gamma_temp_scan(base_path_SD_ksi08_sigma01,i_s=120,nsel_max_itg=True, tmin=tmin, tmax=tmax, min_pts_per_box=8)
    TH_SD_ksi08_sigma02, gamma_scan_SD_ksi08_sigma02, err_scan_SD_ksi08_sigma02=gamma_temp_scan(base_path_SD_ksi08_sigma02,i_s=120,nsel_max_itg=True, tmin=tmin, tmax=tmax, min_pts_per_box=8)

    slopes, stderrs =gamma_box_slopes(path=path_TH00,i_s=140, tmin=tmin, tmax=tmax, n_boxes=4, min_pts_per_box=8,nsel_max_itg=True)
    TH00, gamma_0, err_0=0,slopes.mean(),slopes.std()
    TH_SD_fin=np.zeros(len(TH_SD_ksi08_sigma01))
    for i in range(len(TH_SD_ksi08_sigma01)):
        TH_SD_fin[i]=temperature_fin(1,TH_SD_ksi08_sigma01[i]*5) ###TO CORRECT

    fig,ax=subplots(figsize=(7,6))
    formatter = ScalarFormatter(useMathText=True)
        
    formatter.set_powerlimits((-3, 3))
    ax.yaxis.set_major_formatter(formatter)
    ax.errorbar(TH00, gamma_0, err_0, marker='s',mfc ='w',capsize=5, label=r'$n_f=0$')

    ax.errorbar(TH[0:], gamma_scan[0:], err_scan[0:], marker='s',mfc ='w',capsize=5, label=r'Maxwellian')
    ax.errorbar(TH_SD_fin, gamma_scan_SD_iso, err_scan_SD_iso, marker='o',capsize=5, label=r'Isotropic SD')
    ax.errorbar(TH_SD_fin, gamma_scan_SD_ksi03_sigma02,err_scan_SD_ksi03_sigma02, marker='o',capsize=5, label=r'$\xi=-0.3,\,\sigma=0.1$')
    ax.errorbar(TH_SD_fin, gamma_scan_SD_ksi08_sigma01, err_scan_SD_ksi08_sigma01, marker='o',capsize=5, label=r'$\xi=-0.8,\,\sigma=0.1$')
    ax.errorbar(TH_SD_fin, gamma_scan_SD_ksi08_sigma02, err_scan_SD_ksi08_sigma02, marker='o',capsize=5, label=r'$\xi=-0.8,\,\sigma=0.2$')

    ax.grid()
    ax.legend(fontsize=16)
    fig.tight_layout()
    ax.set_xlabel(r'$T_{EP}/T_i$', fontsize=18)
    ax.set_ylabel(r"$\gamma/\Omega_{ci}$", fontsize=18)
    rc('xtick', labelsize=16)
    rc('ytick', labelsize=16)
    #savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/adhoc/maxwellian/growthrate/temperature_profile/const_beta/gama_const_beta_profile.pdf')
    return 0



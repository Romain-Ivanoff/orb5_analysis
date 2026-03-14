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
from gamma_MPR import *
from gamma import gamma_temp_scan


tmin, tmax=10000,30000
species=['deuterium','fast']

base_path_TH='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/temperature_scan/pitagora/MPR'
base_path_SD_iso='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/pitagora/isotropic/'
base_path_SD_aniso='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/pitagora/anisotropic/'


#from phi:
TH_phi, gamma_scan_phi, err_scan_phi=gamma_temp_scan(base_path_TH,i_s=144, nsel_max_itg=True, tmin=tmin, tmax=tmax, n_boxes=4, min_pts_per_box=8)
TH_SD_iso_phi, gamma_scan_SD_iso_phi, err_scan_SD_iso_phi=gamma_temp_scan(base_path_SD_iso,i_s=144,nsel_max_itg=False, tmin=tmin, tmax=tmax, min_pts_per_box=8,nl_slowingdown=True)
TH_SD_aniso_phi, gamma_scan_SD_aniso_phi, err_scan_SD_aniso_phi=gamma_temp_scan(base_path_SD_aniso,i_s=144,nsel_max_itg=False, tmin=tmin, tmax=tmax, min_pts_per_box=8,nl_slowingdown=True)


#from MPR:
path_maxw='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/temperature_scan/pitagora/MPR' 
TH_maxw,gamma_scan_maxw=gamma_MPR_temp_scan(path_maxw,species, tmin, tmax)

path_iso='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/pitagora/isotropic' 
TH_iso,gamma_scan_iso=gamma_MPR_temp_scan(path_iso,species, tmin, tmax,nl_slowingdown=True)

path_aniso='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/pitagora/anisotropic' 
TH_aniso,gamma_scan_aniso=gamma_MPR_temp_scan(path_aniso,species, tmin, tmax,nl_slowingdown=True)

#test iso:   
path_iso_test='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/pitagora/isotropic/resolution_test' 
TH_iso_test,gamma_scan_iso_test=gamma_MPR_temp_scan(path_iso_test,species, tmin, tmax,nl_slowingdown=True)

path_iso_new='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/pitagora/isotropic/increased-res/' 
TH_iso_new,gamma_scan_iso_new=gamma_MPR_temp_scan(path_iso_new,species, tmin, tmax,nl_slowingdown=True)
      


def contribution_gamma(a=1):#by default EPs
    #a=1 EPs, a=0 ions
    ax.errorbar(TH_maxw[it_min:it_max],gamma_scan_maxw[:,a,1][it_min:it_max], gamma_scan_maxw[:,a,2][it_min:it_max], marker='o',capsize=5, label='Maxwellian')
    #ax.errorbar(TH_maxw[it_min:it_max],gamma_scan_maxw[:,0,1][it_min:it_max]+gamma_scan_maxw[:,1,1][it_min:it_max], gamma_scan_maxw[:,0,2][it_min:it_max]+gamma_scan_maxw[:,1,2][it_min:it_max], marker='o',capsize=5)
    ax.errorbar(TH_iso,gamma_scan_iso[:,a,1], gamma_scan_iso[:,a,2], marker='o',markersize=8,capsize=5, label='Isotropic SD')
    #ax.errorbar(TH_iso,gamma_scan_iso[:,0,1]+gamma_scan_iso[:,1,1], gamma_scan_iso[:,0,2]+gamma_scan_iso[:,1,2], marker='o',capsize=5)
    #ax.errorbar(TH_SD_iso, gamma_scan_SD_iso, err_scan_SD_iso, marker='o',capsize=5, label=r'Isotropic SD')
    ax.errorbar(TH_aniso,gamma_scan_aniso[:,a,1], gamma_scan_aniso[:,a,2], marker='o',capsize=5, label='Anisotropic SD\n' + r'$\xi=-0.66,\,\sigma=0.22$')
    #ax.errorbar(TH_iso_test,gamma_scan_iso_test[:,a,1], gamma_scan_iso_test[:,a,2], marker='o',capsize=5, label='Isotropic SD test')
    #ax.errorbar(TH_iso_new,gamma_scan_iso_new[:,a,1], gamma_scan_iso_new[:,a,2], marker='o',markersize=8,capsize=5, label='Isotropic SD res')
    
    #ax.errorbar(TH_iso_test,gamma_scan_iso_test[0][1,1], gamma_scan_aniso[0][1,2], marker='o',capsize=5, label='Anisotropic SD, high res\n' + r'$\xi=-0.66,\,\sigma=0.22$')
    #print(gamma_scan_iso_test[0][1,1])
    #print(gamma_scan_iso[6,1,1])
    #ax.errorbar(TH_aniso,gamma_scan_aniso[:,0,1]+gamma_scan_aniso[:,1,1], gamma_scan_aniso[:,0,2]+gamma_scan_aniso[:,1,2], marker='o',capsize=5)
    return

def total_gamma():
    #from MPR:
    #ax.errorbar(TH_maxw[it_min:it_max],gamma_scan_maxw[:,0,1][it_min:it_max]+gamma_scan_maxw[:,1,1][it_min:it_max], gamma_scan_maxw[:,0,2][it_min:it_max]+gamma_scan_maxw[:,1,2][it_min:it_max], marker='o',capsize=5, label='Maxwellian')
    ax.errorbar(TH_iso,gamma_scan_iso[:,0,1]+gamma_scan_iso[:,1,1], gamma_scan_iso[:,0,2]+gamma_scan_iso[:,1,2], marker='o',capsize=5, label='Isotropic SD')
    #ax.errorbar(TH_iso_new,gamma_scan_iso_new[:,0,1]+gamma_scan_iso_new[:,1,1], gamma_scan_iso_new[:,0,2]+gamma_scan_iso_new[:,1,2], marker='o',capsize=5, label='Isotropic SD res')
    #ax.errorbar(TH_aniso,gamma_scan_aniso[:,0,1]+gamma_scan_aniso[:,1,1], gamma_scan_aniso[:,0,2]+gamma_scan_aniso[:,1,2], marker='o',capsize=5, label='Anisotropic SD\n' + r'$\xi=-0.66,\,\sigma=0.22$')

    #from phi:

    #ax.errorbar(TH_phi[0:-1], gamma_scan_phi[0:-1], err_scan_phi[0:-1], marker='o',capsize=5, label=r'Maxwellian, $phi$')
    ax.errorbar(TH_SD_iso_phi, gamma_scan_SD_iso_phi, err_scan_SD_iso_phi, marker='o',capsize=5, label=r'Isotropic, $phi$')
    #ax.errorbar(TH_SD_aniso_phi, gamma_scan_SD_aniso_phi, err_scan_SD_aniso_phi, marker='o',capsize=5, label=r'Anisotropic, $phi$')
    #ax.errorbar(TH_iso_test,gamma_scan_iso_test[:,0,1]+gamma_scan_iso_test[:,1,1], gamma_scan_iso_test[:,0,2]+gamma_scan_iso_test[:,1,2], marker='o',capsize=5, label='Isotropic SD test')
    
    return

def contribution_gamma_Maxw(a=1):#by default EPs
    #a=1 EPs, a=0 ions
    ax.errorbar(TH_maxw[it_min:it_max],gamma_scan_maxw[:,a,1][it_min:it_max], gamma_scan_maxw[:,a,2][it_min:it_max], marker='o',capsize=5, label='Maxwellian')
    #ax.errorbar(TH_maxw[it_min:it_max],gamma_scan_maxw[:,0,1][it_min:it_max]+gamma_scan_maxw[:,1,1][it_min:it_max], gamma_scan_maxw[:,0,2][it_min:it_max]+gamma_scan_maxw[:,1,2][it_min:it_max], marker='o',capsize=5)
    #ax.errorbar(TH_iso,gamma_scan_iso[:,a,1], gamma_scan_iso[:,a,2], marker='o',capsize=5, label='Isotropic SD')
    #ax.errorbar(TH_iso,gamma_scan_iso[:,0,1]+gamma_scan_iso[:,1,1], gamma_scan_iso[:,0,2]+gamma_scan_iso[:,1,2], marker='o',capsize=5)
    #ax.errorbar(TH_SD_iso, gamma_scan_SD_iso, err_scan_SD_iso, marker='o',capsize=5, label=r'Isotropic SD')
    #ax.errorbar(TH_aniso,gamma_scan_aniso[:,a,1], gamma_scan_aniso[:,a,2], marker='o',capsize=5, label='Anisotropic SD\n' + r'$\xi=-0.66,\,\sigma=0.22$')
    #ax.errorbar(TH_iso_test,gamma_scan_iso_test[:,a,1], gamma_scan_iso_test[:,a,2], marker='o',capsize=5, label='Isotropic SD test')
    #ax.errorbar(TH_iso_test,gamma_scan_iso_test[0][1,1], gamma_scan_aniso[0][1,2], marker='o',capsize=5, label='Anisotropic SD, high res\n' + r'$\xi=-0.66,\,\sigma=0.22$')
    #print(gamma_scan_iso_test[0][1,1])
    #print(gamma_scan_iso[6,1,1])
    #ax.errorbar(TH_aniso,gamma_scan_aniso[:,0,1]+gamma_scan_aniso[:,1,1], gamma_scan_aniso[:,0,2]+gamma_scan_aniso[:,1,2], marker='o',capsize=5)
    return

def iso_comparison(a=1):
    #a=1 EPs, a=0 ions
    ax.errorbar(TH_iso,gamma_scan_iso[:,a,1], gamma_scan_iso[:,a,2], marker='o',capsize=5, label='Isotropic SD')
    #ax.errorbar(TH_iso,gamma_scan_iso[:,0,1]+gamma_scan_iso[:,1,1], gamma_scan_iso[:,0,2]+gamma_scan_iso[:,1,2], marker='o',capsize=5)
    #ax.errorbar(TH_SD_iso, gamma_scan_SD_iso, err_scan_SD_iso, marker='o',capsize=5, label=r'Isotropic SD')
    ax.errorbar(TH_iso_test,gamma_scan_iso_test[:,a,1], gamma_scan_iso_test[:,a,2], marker='o',capsize=5, label='Isotropic SD test')
    #ax.errorbar(TH_iso_test,gamma_scan_iso_test[0][1,1], gamma_scan_aniso[0][1,2], marker='o',capsize=5, label='Anisotropic SD, high res\n' + r'$\xi=-0.66,\,\sigma=0.22$')
    
    ax.errorbar(TH_iso_new,gamma_scan_iso_new[:,a,1], gamma_scan_iso_new[:,a,2], marker='o',capsize=5, label='Isotropic SD new')

    return 

fig,ax=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))
ax.yaxis.set_major_formatter(formatter)
it_min,it_max=1, -1

#total_gamma()
contribution_gamma(a=1)
#contribution_gamma(a=1)
#contribution_gamma_Maxw(a=1)
#iso_comparison(a=1)
ax.grid()
ax.legend(fontsize=16)

ax.set_xlabel(r'$T_{f}\,/T_i$', fontsize=18)
ax.set_ylabel(r"$\gamma\,/\Omega_{ci}$", fontsize=18)

rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
fig.tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/adhoc/slowingdown/growthrate/temperature_scan/gamma_EP_SD_temp_scan.pdf')

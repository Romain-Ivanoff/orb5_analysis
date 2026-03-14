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
from omega import *

base_path_beta = "/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/const_beta_scan/pitagora/"
base_path_TH='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/temperature_scan/pitagora/'
base_path_iso='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/pitagora/isotropic/' 
base_path_iso_res='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/pitagora/isotropic/increased-res/' 
base_path_aniso='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/pitagora/anisotropic/' 

TH, omega_scan_temp=omega_scan(base_path_TH,i_s=140, nsel_max_itg=True,tmin=10000, tmax=30000)
TH_beta, omega_scan_beta=omega_scan(base_path_beta,i_s=140, nsel_max_itg=True,tmin=10000, tmax=30000)
TH_iso, omega_scan_iso=omega_scan(base_path_iso,i_s=140, nsel_max_itg=True,tmin=10000, tmax=30000,nl_slowingdown=True)
TH_aniso, omega_scan_aniso=omega_scan(base_path_aniso,i_s=140, nsel_max_itg=True,tmin=10000, tmax=30000,nl_slowingdown=True)

fig,ax=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
    
formatter.set_powerlimits((-3, 3))
ax.yaxis.set_major_formatter(formatter)
#TH=np.delete(TH,2)
#omega_scan_temp=np.delete(omega_scan_temp,2)
#TH_beta=np.delete(TH_beta,4)
#omega_scan_beta=np.delete(omega_scan_beta,4)
ax.plot(TH, omega_scan_temp, marker='o', label=r'$\tilde{n}_f=10\%$')
#ax.plot(TH_beta, omega_scan_beta, marker='o', label=r'$\tilde{T}_f\cdot\tilde{n}_f=10\cdot 10\%=const$')
ax.plot(TH_iso, omega_scan_iso, marker='o', label='iso')
ax.plot(TH_iso, omega_scan_iso, marker='o', label='aniso')
#ax.plot(TH_iso_res, omega_scan_iso_res, marker='o', label='iso')

#ax.set_ylim(0.00062,0.00063)
ax.set_xlim(-2,55)
ax.grid()
ax.legend(fontsize=16)
fig.tight_layout()
ax.set_xlabel(r'$T_{f}\,/T_i$', fontsize=18)
ax.set_ylabel(r"$\omega/\Omega_{ci}$", fontsize=18)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/adhoc/slowingdown/growthrate/temperature_scan/omega_SD_profile.pdf')

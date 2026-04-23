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



base_path_beta = "/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/const_beta_scan/pitagora/"
base_path_TH='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/temperature_scan/pitagora/'
base_path_SD_aniso='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/pitagora/anisotropic/'
base_path_unst_leo='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/temperature_scan/leonardo/unstable-eta/'
base_path_unst='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/temperature_scan/pitagora/unstable_eta/'
TH, gamma_scan, err_scan=gamma_temp_scan(base_path_TH,i_s=0, nsel_itg_loc='max_all_space', tmin=10000, tmax=30000, n_boxes=4, min_pts_per_box=8)
TH_beta, gamma_scan_beta, err_scan_beta=gamma_temp_scan(base_path_beta,i_s=0, nsel_itg_loc='max_all_space', tmin=10000, tmax=30000, n_boxes=4, min_pts_per_box=8)

#TH_unst, gamma_scan_unst, err_scan_unst=gamma_temp_scan(base_path_unst_leo,i_s=144, nsel_itg_loc='other', tmin=900, tmax=15500, n_boxes=1, min_pts_per_box=2)
TH_unst, gamma_scan_unst, err_scan_unst=gamma_temp_scan(base_path_unst,i_s=0, nsel_itg_loc='max_all_space', tmin=10000, tmax=30000, n_boxes=4, min_pts_per_box=8)

TH_SD_aniso, gamma_scan_SD_aniso, err_scan_SD_aniso=gamma_temp_scan(base_path_SD_aniso,i_s=0,nsel_itg_loc='max_all_space',tmin=10000, tmax=30000, n_boxes=4,min_pts_per_box=8, nl_slowingdown=True)

fig,ax=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
    
formatter.set_powerlimits((-3, 3))
ax.yaxis.set_major_formatter(formatter)
ax.errorbar(TH, gamma_scan, err_scan, marker='o',capsize=5, label=r'Maxwellian, $\tilde{n}_f=10\%$, $\eta_f^{-1}=0.15$')
#ax.errorbar(TH_beta, gamma_scan_beta, err_scan_beta, marker='o',capsize=5, label=r'$\tilde{T}_f\cdot\tilde{n}_f=10\cdot 10\%=const$')
ax.errorbar(TH_unst, gamma_scan_unst, err_scan_unst, marker='o',capsize=5, label=r'Maxwellian, $\tilde{n}_f=10\%$, $\eta_f^{-1}=4$')
ax.errorbar(TH_SD_aniso, gamma_scan_SD_aniso, err_scan_SD_aniso, marker='o',capsize=5, label=r'Anisotropic SD, $\xi=-0.66,\,\sigma=0.22$')


ax.grid()
ax.legend(fontsize=16)
fig.tight_layout()
ax.set_xlabel(r'$T_{f}\,/T_i$', fontsize=18)
ax.set_ylabel(r"$\gamma\cdot\Omega_{ci}^{-1}$", fontsize=18)
ax.set_xlim(-5,105)
ax.set_xlim(-1,55)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/Pictures/linear_ITG/adhoc/maxwellian/growthrate/temperature_profile/unstable_eta/gamma_TH_stab_profile_comp.pdf')
#savefig('/media/test-Samsung-SSD/roma/Work/Pictures/linear_ITG/adhoc/maxwellian/growthrate/temperature_profile/unstable_eta/gamma_TH_stab_profile_comp.png', dpi=300, bbox_inches='tight')

path_test='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/temperature_scan/pitagora/lin-n20-nH10-TH50/orb5_res.h5'
path_SD_ksi='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/ksi-scan/leonardo/ksi-scan-sigma02/ksi--02/orb5_res.h5'
path_beta_sim='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/const_beta_scan/pitagora/lin-n20-nH20-TH05/orb5_res.h5'
#print(ITG_peak_finder(path_beta_sim))
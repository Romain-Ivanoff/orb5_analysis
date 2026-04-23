from h5py import *
from numpy import *
from numpy.matlib import *
from matplotlib.pyplot import *
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from scipy.signal import find_peaks
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter
import os
import re
import sys
sys.path.append('/media/test-Samsung-SSD/roma/Work/orb5_analysis/scripts/')

from gamma import *

base_path_beta='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/EP/'
TH, gamma_scan, err_scan=gamma_temp_scan(base_path_beta,i_s=0, nsel_itg_loc='max_all_space', tmin=12000, tmax=30000, n_boxes=4, min_pts_per_box=8)

fig,ax=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
    
formatter.set_powerlimits((-3, 3))
ax.yaxis.set_major_formatter(formatter)
ax.errorbar(TH, gamma_scan, err_scan, marker='o',capsize=5, label=r'$\tilde{n}_f=6.5\%$, $\eta_f^{-1}=0.15$')

ax.grid()
ax.legend(fontsize=16)
fig.tight_layout()
ax.set_xlabel(r'$T_{f}\,/T_i$', fontsize=18)
ax.set_ylabel(r"$\gamma\cdot\Omega_{ci}^{-1}$", fontsize=18)
ax.set_xlim(-5,105)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/Pictures/linear_ITG/supra/maxwellian_EP/gamma_TH_profile_comp.pdf')
#savefig('/media/test-Samsung-SSD/roma/Work/Pictures/linear_ITG/supra/maxwellian_EP/gamma_TH_profile_comp.png', dpi=300, bbox_inches='tight')

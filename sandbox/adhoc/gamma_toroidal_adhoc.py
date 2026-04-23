def old_spec():
    path_TH00='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/spectrum_scan/leonardo/TH00'
    path_TH10='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/spectrum_scan/leonardo/TH10'
    tmin=10000
    tmax=30000
    n_TH00, gamma_TH00, err_TH00=gamma_toroidal_scan(path_TH00,i_s=144, nsel_max_itg=False, tmin=tmin, tmax=tmax)
    n_TH10, gamma_TH10, err_TH10=gamma_toroidal_scan(path_TH10,i_s=144, nsel_max_itg=False, tmin=tmin, tmax=tmax)


    '''
    figure(figsize=(7, 6))
    ampltude_phi_legend('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/spectrum_scan/leonardo/TH00/n08/orb5_res.h5','old',i_s=140)
    grid()
    legend(fontsize=14)
    tight_layout()
    '''

    fig,ax=subplots(figsize=(7,6))
    formatter = ScalarFormatter(useMathText=True)
        
    formatter.set_powerlimits((-3, 3))
    ax.yaxis.set_major_formatter(formatter)
    ax.errorbar(n_TH00, gamma_TH00, err_TH00, marker='o',capsize=5, label=r'$\tilde{n}_f=0\%$')
    ax.errorbar(n_TH10, gamma_TH10, err_TH10, marker='o',capsize=5, label=r'$\tilde{n}_f=10\%,\, \tilde{T}_f=10$')
    ax.grid()
    ax.legend(fontsize=16)
    fig.tight_layout()
    ax.set_xlabel(r'$n$', fontsize=18)
    ax.set_ylabel(r"$\gamma/\Omega_{ci}$", fontsize=18)
    rc('xtick', labelsize=16)
    rc('ytick', labelsize=16)
    tight_layout()
    #savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/adhoc/maxwellian/growthrate/toroidal_spectrum/gama_n_profile.pdf')
    return 0


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
from kperp import n_kperp_convertion_folder
from kperp import n_kperp_convertion_folder_adhoc

base_alexey_lx180='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/noEP/toroidal_scan/lx180/'
base_alexey_lx360='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/noEP/toroidal_scan/lx360/'
base_alexey_lx360_eta='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/noEP/toroidal_scan/lx360_eta/'
base_alexey_lx360_B='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/noEP/toroidal_scan/lx360_B/'
base_alexey_lx360noFLR='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/noEP/toroidal_scan/lx360noFLR/'
base_alexey_lx540='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/noEP/toroidal_scan/lx540/'
base_TH10_old='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/toroidal_scan/TH10_underresolved/'

def get_spec_adhoc(base_path):
    n, gamma, err=gamma_toroidal_scan(base_path,i_s=0, tmin=12000, tmax=60000, nsel_itg_loc='max_all_space', n_boxes=4,min_pts_per_box=8)
    kperp=n_kperp_convertion_folder_adhoc(base_path,tmin=12000, tmax=60000)
    return kperp, n, gamma*10**5, err*10**5

kperp_alexey_lx180, n_alexey_lx180, gamma_alexey_lx180, err_alexey_lx180 = get_spec_adhoc(base_alexey_lx180)
kperp_alexey_lx360, n_alexey_lx360, gamma_alexey_lx360, err_alexey_lx360 = get_spec_adhoc(base_alexey_lx360)
kperp_alexey_lx360noFLR, n_alexey_lx360noFLR, gamma_alexey_lx360noFLR, err_alexey_lx360noFLR = get_spec_adhoc(base_alexey_lx360noFLR)
kperp_alexey_lx360_eta, n_alexey_lx360_eta, gamma_alexey_lx360_eta, err_alexey_lx360_eta = get_spec_adhoc(base_alexey_lx360_eta)
kperp_alexey_lx360_TH10, n_alexey_lx360_TH10, gamma_alexey_lx360_TH10, err_alexey_lx360_TH10 = get_spec_adhoc(base_TH10_old)
kperp_alexey_lx540, n_alexey_lx540, gamma_alexey_lx540, err_alexey_lx540 = get_spec_adhoc(base_alexey_lx540)



fig,ax1=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))
ax1.yaxis.set_major_formatter(formatter)

ax1.errorbar(kperp_alexey_lx180, gamma_alexey_lx180, err_alexey_lx180, color='w',label=r'$lx:$',marker='o',capsize=5)

ax1.errorbar(kperp_alexey_lx180, gamma_alexey_lx180, err_alexey_lx180, label=r'$180$',marker='o',capsize=5)
ax1.errorbar(kperp_alexey_lx360, gamma_alexey_lx360, err_alexey_lx360, label=r'$360$',marker='o',capsize=5)
ax1.errorbar(kperp_alexey_lx360noFLR, gamma_alexey_lx360noFLR, err_alexey_lx360noFLR, label=r'$360$, no FLR',marker='o',capsize=5)
ax1.errorbar(kperp_alexey_lx360_eta, gamma_alexey_lx360_eta, err_alexey_lx360_eta, label=r'$360, \eta^{-1}=0.3$',marker='o',capsize=5)
ax1.errorbar(kperp_alexey_lx360_TH10, gamma_alexey_lx360_TH10, err_alexey_lx360_TH10, label=r'$360, T_f=10$',marker='o',capsize=5)
ax1.errorbar(kperp_alexey_lx540, gamma_alexey_lx540, err_alexey_lx540, label=r'$540$',marker='o',capsize=5)


ax_top = ax1.twiny()

ax_top.set_xlim(ax1.get_xlim())

labels_fmt = [f"{v:g}" for v in n_alexey_lx360_eta]

ax_top.set_xticks(kperp_alexey_lx360_eta)
ax_top.set_xticklabels(labels_fmt)
ax_top.tick_params(axis='x', labelrotation=45)
ax1.set_xlabel(r'$k_\theta\rho_s$', fontsize=18)

formatter = FuncFormatter(lambda x, _: f'{x:g}')
ax1.xaxis.set_major_formatter(formatter)

ax1.grid()
ax1.legend(fontsize=14,ncol=3)
ax1.set_ylim(0,200)
ax_top.set_xlabel(r'n', fontsize=18)
ax1.set_ylabel(r"$\gamma\cdot\Omega_{ci}^{-1}\cdot10^{-5}$", fontsize=18)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
fig.tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/Pictures/linear_ITG/adhoc/noEP/gamma_toroidal_comp_noFLR.pdf')

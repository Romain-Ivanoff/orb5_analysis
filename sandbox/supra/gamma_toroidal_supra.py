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


base_path_high='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/noEP/toroidal_scan/high_n'
base_path_noFLR='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/noEP/toroidal_scan/noFLR/'
path_ogyropsi='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/inputs/ogyropsi.h5_Roman_shaped_zerobeta'

n_high, gamma_high, err_high=gamma_toroidal_scan(base_path_high,i_s=190, nsel_itg_loc='max_all_space', tmin=10000, tmax=30000, n_boxes=4,min_pts_per_box=8)
n_noFLR, gamma_noFLR, err_noFLR=gamma_toroidal_scan(base_path_noFLR,i_s=190, nsel_itg_loc='max_all_space', tmin=10000, tmax=30000, n_boxes=4,min_pts_per_box=8)

kperprho_high=n_kperp_convertion_folder(base_path_high, path_ogyropsi, tmin=10000, tmax=30000)
kperprho_noFLR=n_kperp_convertion_folder(base_path_noFLR, path_ogyropsi, tmin=10000, tmax=30000)

fig,ax=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))
ax.yaxis.set_major_formatter(formatter)

ax.errorbar(kperprho_noFLR, gamma_noFLR*10**5, err_noFLR*10**5, label='FLR off',marker='o',capsize=5,color='red')
ax.errorbar(kperprho_high, gamma_high*10**5, err_high*10**5, label='FLR on',marker='o',capsize=5)

ax_top = ax.twiny()

ax_top.set_xlim(ax.get_xlim())

labels_fmt = [f"{v:g}" for v in n_noFLR]

ax_top.set_xticks(kperprho_noFLR)
ax_top.set_xticklabels(labels_fmt)
ax_top.tick_params(axis='x', labelrotation=0, labelcolor='red')
ax.set_xlabel(r'$k_\theta\rho_s$', fontsize=18)
#ax.set_xlim(0,1)
formatter = FuncFormatter(lambda x, _: f'{x:g}')
ax.xaxis.set_major_formatter(formatter)

ax.grid()
ax.legend(fontsize=16, loc=2)
ax_top.set_xlabel(r'n', fontsize=18, color='red')
ax.set_ylabel(r"$\gamma\cdot\Omega_{ci}^{-1}\cdot10^{-5}$", fontsize=18)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
fig.tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/Pictures/linear_ITG/supra/noEP/growthrate/gamma_toroidal_FLR.pdf')
#savefig('/media/test-Samsung-SSD/roma/Work/Pictures/linear_ITG/supra/noEP/growthrate/gamma_toroidal_FLR.png', dpi=300, bbox_inches='tight')



def comp_with_Alexey_case():
    base_path_old='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/noEP/toroidal_scan/tests/low_res'
    n_old, gamma_old, err_old=gamma_toroidal_scan(base_path_old,i_s=190, nsel_max_itg=False, tmin=12000, tmax=30000, n_boxes=4,min_pts_per_box=8,nl_slowingdown=False, nsel_box_err=True, nsel_max_all_space=True)
    kperprho_old=n_kperp_convertion_folder(base_path_old, path_ogyropsi)

    base_alexey_lx180='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/noEP/toroidal_scan/lx180/'
    base_alexey_lx360='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/noEP/toroidal_scan/lx360/'
    base_alexey_lx360_eta='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/noEP/toroidal_scan/lx360_eta/'
    base_alexey_lx360_B='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/noEP/toroidal_scan/lx360_B/'
    base_alexey_lx540='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/noEP/toroidal_scan/lx540/'

    n_alexey_lx180, gamma_alexey_lx180, err_alexey_lx180=gamma_toroidal_scan(base_alexey_lx180,i_s=190, nsel_max_itg=False, tmin=12000, tmax=60000, n_boxes=4,min_pts_per_box=8,nl_slowingdown=False, nsel_box_err=True, nsel_max_all_space=True)
    n_alexey_lx360, gamma_alexey_lx360, err_alexey_lx360=gamma_toroidal_scan(base_alexey_lx360,i_s=190, nsel_max_itg=False, tmin=12000, tmax=60000, n_boxes=4,min_pts_per_box=8,nl_slowingdown=False, nsel_box_err=True, nsel_max_all_space=True)
    n_alexey_lx360_eta, gamma_alexey_lx360_eta, err_alexey_lx360_eta=gamma_toroidal_scan(base_alexey_lx360_eta,i_s=190, nsel_max_itg=False, tmin=12000, tmax=60000, n_boxes=4,min_pts_per_box=8,nl_slowingdown=False, nsel_box_err=True, nsel_max_all_space=True)
    n_alexey_lx360_B, gamma_alexey_lx360_B, err_alexey_lx360_B=gamma_toroidal_scan(base_alexey_lx360_B,i_s=190, nsel_max_itg=False, tmin=12000, tmax=60000, n_boxes=4,min_pts_per_box=8,nl_slowingdown=False, nsel_box_err=True, nsel_max_all_space=True)
    n_alexey_lx540, gamma_alexey_lx540, err_alexey_lx540=gamma_toroidal_scan(base_alexey_lx540,i_s=190, nsel_max_itg=False, tmin=12000, tmax=60000, n_boxes=4,min_pts_per_box=8,nl_slowingdown=False, nsel_box_err=True, nsel_max_all_space=True)

    kperp_alexey_lx180=n_kperp_convertion_folder_adhoc(base_alexey_lx180, tmin=12000, tmax=30000)
    kperp_alexey_lx360=n_kperp_convertion_folder_adhoc(base_alexey_lx360, tmin=12000, tmax=30000)
    kperp_alexey_lx360_eta=n_kperp_convertion_folder_adhoc(base_alexey_lx360_eta, tmin=12000, tmax=30000)
    kperp_alexey_lx360_B=n_kperp_convertion_folder_adhoc(base_alexey_lx360_B, tmin=12000, tmax=30000)
    kperp_alexey_lx540=n_kperp_convertion_folder_adhoc(base_alexey_lx540, tmin=12000, tmax=30000)


    fig,ax=subplots(figsize=(7,6))
    formatter = ScalarFormatter(useMathText=True)
    formatter.set_powerlimits((-3, 3))
    ax.yaxis.set_major_formatter(formatter)

    ax1 = ax.twinx()


    ax.errorbar(kperprho_old, gamma_old*10**5, err_old*10**5, label='low res',marker='o',capsize=5)
    ax.errorbar(kperprho_high, gamma_high*10**5, err_high*10**5, color='red', label='FLR',marker='o',capsize=5)
    ax.errorbar(kperprho_noFLR, gamma_noFLR*10**5, err_noFLR*10**5, color='black', label='no FLR',marker='o',capsize=5)

    ax1.errorbar(kperp_alexey_lx180, gamma_alexey_lx180*10**5, err_alexey_lx180*10**5, label=r'$lx=180$',marker='o',capsize=5)
    ax1.errorbar(kperp_alexey_lx360, gamma_alexey_lx360*10**5, err_alexey_lx360*10**5, label=r'$lx=360$',marker='o',capsize=5)
    ax1.errorbar(kperp_alexey_lx360_eta, gamma_alexey_lx360_eta*10**5, err_alexey_lx360_eta*10**5, label=r'adhoc, $lx=360, \eta^{-1}=0.3$',marker='o',capsize=5)
    ax1.errorbar(kperp_alexey_lx360_B, gamma_alexey_lx360_B*10**5, err_alexey_lx360_B*10**5, label=r'$lx=360, B$',marker='o',capsize=5)
    ax1.errorbar(kperp_alexey_lx540, gamma_alexey_lx540*10**5, err_alexey_lx540*10**5, label=r'$lx=540$',marker='o',capsize=5)


    ax_top = ax.twiny()

    ax_top.set_xlim(ax.get_xlim())

    labels_fmt = [f"{v:g}" for v in n_noFLR]

    ax_top.set_xticks(kperprho_noFLR)
    ax_top.set_xticklabels(labels_fmt)
    ax_top.tick_params(axis='x', labelrotation=45)
    ax.set_xlabel(r'$k_\theta\rho_s$', fontsize=18)

    formatter = FuncFormatter(lambda x, _: f'{x:g}')
    ax.xaxis.set_major_formatter(formatter)
    #Delta m convergence:_____________________

    ax.grid()
    ax.legend(fontsize=16, loc=2)
    ax1.legend(fontsize=16, loc=4)
    #ax1.set_ylim(0,120)
    ax_top.set_xlabel(r'n', fontsize=18)
    ax.set_ylabel(r"$\gamma\cdot\Omega_{ci}^{-1}\cdot10^{-5}$", fontsize=18)
    #ax1.set_ylabel(r"$\gamma\cdot\Omega_{ci}^{-1}\cdot10^{-5}$", fontsize=18)
    rc('xtick', labelsize=16)
    rc('ytick', labelsize=16)
    fig.tight_layout()
    #savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/supra/toroidal_spectrum_FLR_comp.pdf')

    return
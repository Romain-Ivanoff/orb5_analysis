import numpy as np
import matplotlib.pyplot as plt
from scipy.special import wofz, iv
from scipy.optimize import root
import warnings

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

def read_gamma(name="itg_scan.txt"):
    data = np.loadtxt(name)
    kperp_vals = data[:,0]
    gamma_kperp = data[:,1]
    kpar_best = data[:,2]
    return kperp_vals, gamma_kperp

def peak(kperp_vals, gamma_kperp):
    imax = np.nanargmax(gamma_kperp)

    kperp_peak = kperp_vals[imax]
    gamma_peak = gamma_kperp[imax]
    scatter(kperp_peak, gamma_peak, color='red', zorder=3)

    return



fig,ax=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))
ax.yaxis.set_major_formatter(formatter)


kperp_vals, gamma_kperp=read_gamma('itg_scan_eta_13.2.txt')

ax.plot(kperp_vals,gamma_kperp, label=r'$\eta_i^{-1}=0.075$')
peak(kperp_vals, gamma_kperp)
kperp_vals, gamma_kperp=read_gamma('itg_scan_eta_6.6.txt')
peak(kperp_vals, gamma_kperp)
ax.plot(kperp_vals,gamma_kperp, label=r'$\eta_i^{-1}=0.15$')
kperp_vals, gamma_kperp=read_gamma('itg_scan_eta_3.3.txt')
peak(kperp_vals, gamma_kperp)
ax.plot(kperp_vals,gamma_kperp, label=r'$\eta_i^{-1}=0.3$')

ax.set_xlabel(r'$k_\perp\rho_s$', fontsize=18)
ax.set_xlim(0.5,1.5)
ax.set_ylim(0.1,0.6)
formatter = FuncFormatter(lambda x, _: f'{x:g}')
ax.xaxis.set_major_formatter(formatter)

ax.grid()
ax.legend(fontsize=16)

ax.set_ylabel(r"$\gamma$", fontsize=18)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
fig.tight_layout()
#savefig('gamma_toroidal_slab.pdf')

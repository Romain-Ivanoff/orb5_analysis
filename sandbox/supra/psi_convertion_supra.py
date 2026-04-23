from h5py import *
from numpy import *
from numpy.matlib import *
from matplotlib.pyplot import *
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from scipy.signal import find_peaks
from matplotlib.ticker import ScalarFormatter
import sys
sys.path.append('/media/test-Samsung-SSD/roma/Work/orb5_analysis/scripts')
from ITG_peakfinder import ITG_peak_finder

path_circ='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/inputs/ogyropsi.h5_Roman_circ_zerobeta'
path_res='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/test/n80/orb5_res.h5'
path_shaped='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/inputs/ogyropsi.h5_Roman_shaped_zerobeta'
path_high='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/shaped/n_scan/resolution_test/n130_dt10_ntot7/orb5_res.h5'

def profiles_extraction(path):
    struct=File(path,'r')
    psi_rz=array(struct["/data/var2d/psiRZ"])
    R=array(struct["/data/var2d/R"])
    struct.close()
    r_norm=(R[0]-R[0,0])/(R[0,-1]-R[0,0])
    R_len=len(r_norm)
    s=np.linspace(0,1,R_len)
    psi=s**2
    ne=(1-r_norm**2)**0.1
    Te=(1-r_norm**2)

    d = np.zeros_like(ne)
    data = np.column_stack((psi, Te, ne, d))
    return r_norm, s, psi, Te, ne

r_norm, s, psi, Te, ne=profiles_extraction(path_shaped)
#r_norm_circ, s_circ, psi_circ, Te_circ, ne_circ=profiles_extraction(path_circ)

def plot_prodiles():
    
    fig,ax=subplots(figsize=(7,6))
    formatter = ScalarFormatter(useMathText=True)
    formatter.set_powerlimits((-3, 3))
    ax.yaxis.set_major_formatter(formatter)
    ax1=twinx(ax)
    ax.plot(s,ne*1.815, label=r'$n_e$')
    ax1.plot(s,Te*28, label=r'$T_e$', color='orange')
    #ax.plot(psi,ne, label=r'$\psi$')
    #ax.plot(r_norm,ne, label=r'$r/a$')
    ax.grid()
    ax.legend(fontsize=16, loc=3)
    ax1.legend(fontsize=16, loc=1)
    ax.set_xlabel(r's', fontsize=18)
    ax1.set_ylabel(r'$T_e, \,keV$', fontsize=18)
    ax.set_ylabel(r"$n_e, \,10^{20}\,m^{-3}$", fontsize=18)
    rc('xtick', labelsize=16)
    rc('ytick', labelsize=16)
    fig.tight_layout()
    #savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/supra/ne_profile_all.pdf')
    #savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/supra/nT_profiles.pdf')


    #np.savetxt("electrons_profile_shaped.dat", data, fmt="%.8e")
    return 0
#plot_prodiles()

def kperprhoi(n, path):
    struct=File(path,'r')
    q=array(struct["/equil/profiles/generic/q"])
    s_q=array(struct["/equil/profiles/generic/sgrid_eq"])
    Ti=array(struct["/equil/profiles/hydrogen/t_pic"])
    s_T=array(struct["/equil/profiles/hydrogen/s_prof"])
    Ti=Ti*27.9*1000
    Bc=array(struct["/equil/sc/B_c"])
    r_sc=array(struct["/equil/sc/r_c"])
    B_norm=array(struct["/equil/scalars/generic/b_norm"])
    B=1/B_norm*Bc[0]
    
    
    L_norm=array(struct["/equil/scalars/generic/d_norm"])
    #print(L_norm)
    struct.close()
    mi=1.67*10**(-27)
    e=1.6*10**(-19)
    q=np.delete(q,-1)
    Ti=np.delete(Ti,-1)
    kperprhoi=n*q*sqrt(mi/e*Ti*2)/B
    #print(len(q))
    #print(len(B))
    #print(len(Ti))
    #print(np.max(Bc))
    #print(q[200])
    return kperprhoi

def ITG_peak_s(path):
    struct=File(path,'r')
    phi_s=array(struct["/data/var2d/generic/potsc/coord1"])
    struct.close()
    i_s=ITG_peak_finder(path_high,i_time=-1)
    s=phi_s[i_s]
    return s

def kperp_plot():
    val=kperprhoi(180, path_high)/r_norm/1.6
    fig,ax=subplots(figsize=(7,6))
    plot(r_norm*1.6,val)
    ax.set_xlim(0.5,1)
    ax.set_ylim(0,1)
    return 1


def n_kperp_convertion(path, pathogropsi,n):

    struct=File(pathogropsi,'r')
    R=array(struct["/data/var2d/R"])
    struct.close()
    r_norm=(R[0]-R[0,0])/(R[0,-1]-R[0,0])
    R_len=len(r_norm)
    s=np.linspace(0,1,R_len)

    struct=File(path,'r')
    q=array(struct["/equil/profiles/generic/q"])
    Ti=array(struct["/equil/profiles/hydrogen/t_pic"])
    Bc=array(struct["/equil/sc/B_c"])
    B_norm=array(struct["/equil/scalars/generic/b_norm"])
    B=Bc[0]/B_norm
    struct.close()
    Ti=Ti*27.9*1000

    mi=1.67*10**(-27)
    e=1.6*10**(-19)
    q=np.delete(q,-1)
    Ti=np.delete(Ti,-1)
    kperprhoi=n*q*sqrt(mi/e*Ti*2)/B/r_norm/1.6 #minor radius in meters
    idx = np.argmin(np.abs(ITG_peak_s(path)-s))

    return kperprhoi[idx]

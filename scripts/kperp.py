from h5py import *
from numpy import *
from numpy.matlib import *
from matplotlib.pyplot import *
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from scipy.signal import find_peaks
import sys
sys.path.append('/media/test-Samsung-SSD/roma/Work/orb5_analysis/scripts')
#from amplitude_phi import ITG_peak_finder
from gamma import process_toroidal_n_folders
from ITG_peakfinder import ITG_peak_s
path='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/PEPR_SUPRA/shaped/n_scan/resolution_test/n110_dt10_ntot7/orb5_res.h5'

path_circ='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/PEPR_SUPRA/inputs/ogyropsi.h5_Roman_circ_zerobeta'
path_res='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/PEPR_SUPRA/test/n80/orb5_res.h5'
path_shaped='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/PEPR_SUPRA/inputs/ogyropsi.h5_Roman_shaped_zerobeta'
path_high='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/PEPR_SUPRA/shaped/n_scan/resolution_test/n130_dt10_ntot7/orb5_res.h5'
base_path_high='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/PEPR_SUPRA/shaped/n_scan/resolution_test/'
adhoc_path='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/noEP/toroidal_scan/lx360/n50/orb5_res.h5'


#ITG_peak_s(adhoc_path)

def n_kperp_convertion(path, pathogropsi,tmin,tmax):

    struct=File(pathogropsi,'r')
    R=array(struct["/data/var2d/R"])
    struct.close()
    r_norm=(R[0]-R[0,0])/(R[0,-1]-R[0,0])
    R_len=len(r_norm)
    s=np.linspace(0,1,R_len)

    struct=File(path,'r')
    q=array(struct["/equil/profiles/generic/q"])
    Ti=array(struct["/equil/profiles/hydrogen/t_pic"])
    n=array(struct["/parameters/fields/nfilt1"])
    Bc=array(struct["/equil/sc/B_c"])
    B_norm=array(struct["/equil/scalars/generic/b_norm"])
    B=Bc[0]/B_norm
    struct.close()
    Ti=Ti*27.9*1000
    
    mi=1.67*10**(-27)
    e=1.6*10**(-19)
    q=np.delete(q,-1)
    Ti=np.delete(Ti,-1)
    a=1.6
    kperprhoi=n*q*sqrt(mi/e*Ti)/B/r_norm/a #minor radius in meters
    idx = np.argmin(np.abs(ITG_peak_s(path,tmin,tmax)-s))


    return kperprhoi[idx]



def n_kperp_convertion_adhoc(path,tmin,tmax):
    struct=File(path,'r')
    q=array(struct["/equil/profiles/generic/q"])
    Ti=array(struct["/equil/profiles/deuterium/t_pic"])

    Bc=array(struct["/equil/sc/B_c"])
    rsc=array(struct["/equil/sc/r_c"])
    s_extr=array(struct["/equil/sc/coord1"])

    d_norm=array(struct["/equil/scalars/generic/d_norm"])
    B_norm=array(struct["/equil/scalars/generic/b_norm"])
    R0=array(struct["/equil/scalars/generic/r0_mid"])/d_norm
    a=array(struct["/equil/scalars/generic/a_mid"])/d_norm

    lx=array(struct["/parameters/equil/lx"])
    n=array(struct["/parameters/fields/nfilt1"])
    struct.close()

    s_ITG=ITG_peak_s(path,tmin,tmax)
    idx_s=np.argmin(np.abs(s_ITG-s_extr))
    r=rsc[0]/d_norm-R0
    r_itg=r[idx_s]

    B=Bc[0]/B_norm
    q_itg=q[idx_s]
    Bspeak=B[len(B)// 2]
    Tispeak=Ti[len(Ti)// 2]

    kperprhoi=2*n/lx*q_itg*Bspeak/(B[idx_s])*sqrt(Ti[idx_s]/Tispeak)*a/r_itg
    #kperprhoi=2*n/lx*q_itg*Bspeak/(B[idx_s])*sqrt(Ti[idx_s]/Tispeak)*a/0.5
    #print(r_itg)
    return kperprhoi

'''
struct=File(adhoc_path,'r')
q=array(struct["/equil/profiles/generic/q"])
Ti=array(struct["/equil/profiles/deuterium/t_pic"])

Bc=array(struct["/equil/sc/B_c"])
rsc=array(struct["/equil/sc/r_c"])
s_extr=array(struct["/equil/sc/coord1"])
struct.close()

print(shape(q))
print(shape(Ti))
print(shape(rsc))
print(shape(s_extr))
'''

def n_kperp_convertion_folder(base_path, pathogropsi,tmin,tmax):
    arr=process_toroidal_n_folders(base_path)
    k_perp_arr=np.zeros(len(arr))
    n_arr=np.zeros(len(arr))
    it=0
    for ns in arr:
        n_arr[it]=ns
        k_perp_arr[it]=n_kperp_convertion(arr[ns]+'/orb5_res.h5', pathogropsi,tmin,tmax)
        it+=1
    return k_perp_arr

def n_kperp_convertion_folder_adhoc(base_path,tmin,tmax):
    arr=process_toroidal_n_folders(base_path)
    k_perp_arr=np.zeros(len(arr))
    n_arr=np.zeros(len(arr))
    it=0
    for ns in arr:
        n_arr[it]=ns
        k_perp_arr[it]=n_kperp_convertion_adhoc(arr[ns]+'/orb5_res.h5',tmin,tmax)
        it+=1
    return k_perp_arr

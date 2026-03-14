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
from matplotlib.ticker import MaxNLocator
import os
import re

import sys
sys.path.append('/media/test-Samsung-SSD/roma/Work/orb5_analysis/scripts/')
from temp_convertion import temperature_fin
from ITG_peakfinder import *

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def phi_extraction(path):
    if path[0:6]=='/media':
        pathITG=path
    else:
        pathITG='/media/test-Samsung-SSD/roma/Work/simulations/'+path
    struct=File(pathITG,'r')
    phi_sc=array(struct["/data/var2d/generic/potsc/data"])
    phi_t=array(struct["/data/var2d/generic/potsc/time"])
    phi_s=array(struct["/data/var2d/generic/potsc/coord1"])
    phi_theta=array(struct["/data/var2d/generic/potsc/coord2"])
    struct.close()
    return phi_sc, phi_t,phi_s,phi_theta


def fit_slope_logA(t, phi, tmin=None, tmax=None):
    """
    Fit log(A_t) = gamma * t + intercept.
    Returns slope (gamma), std_err, intercept, r^2.
    """
    # mask time window
    mask = (phi > 0)  # avoid log of non-positive
    if tmin is not None:
        mask &= (t >= tmin)
    if tmax is not None:
        mask &= (t <= tmax)

    tt = t[mask]
    yy = np.log(phi[mask])

    slope, intercept, r_value, p_value, std_err = linregress(tt, yy)
    return slope, std_err, intercept, r_value**2

def gamma_box_slopes(path,i_s=140, tmin=None, tmax=None, n_boxes=4, min_pts_per_box=8,nsel_max_itg=False, nsel_max_all_space=False):
    phi_sc, phi_t,phi_s,phi_theta=phi_extraction(path)
    phi_max_pol_s=np.zeros(len(phi_t))
    phi_max=np.zeros(len(phi_t))
    if nsel_max_itg==True:
        i_s=ITG_peak_finder(path,tmin, tmax)
    for i_t in range(len(phi_t)):
        phi_max_pol_s[i_t]=np.max(phi_sc[i_t,:,i_s])
        phi_max[i_t]=np.max(phi_sc[i_t])
    #######
    #print(ITG_peak_finder(path,tmin, tmax, 0, 130)) 
    #######
    mask = (phi_t >= tmin) & (phi_t <= tmax)
    tt = phi_t[mask]
    y = np.log(phi_max_pol_s[mask])
    N = len(tt)
    if nsel_max_all_space==True:
        y = np.log(phi_max[mask])
    # adjust number of boxes if data too short
    if N < n_boxes * min_pts_per_box:
        n_boxes = max(1, N // min_pts_per_box)
    if n_boxes == 0:
        raise ValueError("Not enough points for segmentation")

    edges = np.linspace(0, N, n_boxes+1, dtype=int)
    slopes, stderrs = [], []

    for i in range(n_boxes):
        i0, i1 = edges[i], edges[i+1]
        if i1 - i0 < 3:
            continue
        slope, err, _, _ = fit_slope_logA(tt[i0:i1], np.exp(y[i0:i1]))
        slopes.append(slope)
        stderrs.append(err)

    return np.array(slopes), np.array(stderrs)

def process_temperature_folders(base_path, target_temps=None):
    """
    Scans subfolders named like THxx, extracts temperatures, and applies a function.
    
    Parameters:
    - base_path (str): Path containing THxx subfolders.
    - target_temps (list or array, optional): Only process folders with these temperatures.
    - func (callable, optional): Function to apply to each folder. Must take folder_path as input.
    
    Returns:
    - dict: {temperature: result of func(folder_path)}
    """
    pattern = re.compile(r"TH(\d+)")
    temps_and_folders = []

    # Scan folders
    for folder in os.listdir(base_path):
        full_path = os.path.join(base_path, folder)
        if os.path.isdir(full_path):
            match = pattern.search(folder)
            if match:
                temp_value = int(match.group(1))
                temps_and_folders.append((temp_value, full_path))

    # Sort by temperature
    temps_and_folders.sort(key=lambda x: x[0])
    
    # Extract paths
    results = {}
    for temp, folder_path in temps_and_folders:
        if target_temps is None or temp in target_temps:
            results[temp] = folder_path
    
    return results

def process_toroidal_n_folders(base_path, target_ns=None):
    """
    Scans subfolders named like nxx, extracts ns, and applies a function.
    
    Parameters:
    - base_path (str): Path containing nxx subfolders.
    - target_ns (list or array, optional): Only process folders with these ns.
    - func (callable, optional): Function to apply to each folder. Must take folder_path as input.
    
    Returns:
    - dict: {n: result of func(folder_path)}
    """
    pattern = re.compile(r"n(\d+)")
    ns_and_folders = []

    # Scan folders
    for folder in os.listdir(base_path):
        full_path = os.path.join(base_path, folder)
        if os.path.isdir(full_path):
            match = pattern.search(folder)
            if match:
                n_value = int(match.group(1))
                ns_and_folders.append((n_value, full_path))

    # Sort by n
    ns_and_folders.sort(key=lambda x: x[0])
    
    # Extract paths
    results = {}
    for n, folder_path in ns_and_folders:
        if target_ns is None or n in target_ns:
            results[n] = folder_path
    
    return results

def gamma_temp_scan(base_path,i_s=140, nsel_max_itg=False, tmin=None, tmax=None, n_boxes=4, min_pts_per_box=8, nl_slowingdown=False, nsel_box_err=True, nsel_max_all_space=False):
    arr=process_temperature_folders(base_path)
    gamma_scan=np.zeros(len(arr))
    err_scan=np.zeros(len(arr))
    TH=np.zeros(len(arr))
    it=0
    for temps in arr:
        if nsel_max_itg==True:
            i_s=ITG_peak_finder(arr[temps]+'/orb5_res.h5',tmin, tmax)
            #print(i_s)
        slopes, stderrs = gamma_box_slopes(arr[temps]+'/orb5_res.h5',i_s, tmin, tmax, n_boxes, min_pts_per_box, nsel_max_all_space)
        gamma_scan[it],err_scan[it]=slopes.mean(),slopes.std()
        if nsel_box_err==False:
            slopes, stderrs = gamma_box_slopes(arr[temps]+'/orb5_res.h5',i_s, tmin, tmax, 1, min_pts_per_box, nsel_max_all_space)
            err_scan[it]=slopes.std()
        TH[it]=temps
        #print(TH[it])
        it+=1
    if nl_slowingdown == True:
        E_birth=5
        for i in range(len(TH)):
            TH[i]=temperature_fin(1,TH[i]*E_birth) ###TO CORRECT
            #print(TH[i])
        
    return TH, gamma_scan, err_scan/sqrt(n_boxes)

def gamma_toroidal_scan(base_path,i_s=140, nsel_max_itg=False, tmin=None, tmax=None, n_boxes=4,min_pts_per_box=8,nl_slowingdown=False, nsel_box_err=True, nsel_max_all_space=False):
    arr=process_toroidal_n_folders(base_path)
    gamma_scan=np.zeros(len(arr))
    err_scan=np.zeros(len(arr))
    n_arr=np.zeros(len(arr))
    it=0
    for ns in arr:
        if nsel_max_itg==True:
            i_s=ITG_peak_finder(arr[ns]+'/orb5_res.h5',tmin, tmax)
            #print(i_s)
        slopes, stderrs = gamma_box_slopes(arr[ns]+'/orb5_res.h5',i_s, tmin, tmax, n_boxes, min_pts_per_box, nsel_max_itg, nsel_max_all_space)
        gamma_scan[it],err_scan[it]=slopes.mean(),slopes.std()
        if nsel_box_err==False:
            slopes, stderrs = gamma_box_slopes(arr[ns]+'/orb5_res.h5',i_s, tmin, tmax, 1, min_pts_per_box, nsel_max_itg, nsel_max_all_space)
            err_scan[it]=slopes.std()
        n_arr[it]=ns
        it+=1
    if nl_slowingdown == True:
        E_birth=5
        for i in range(len(n_arr)):
            n_arr[i]=temperature_fin(1,n_arr[i]*E_birth) ###TO CORRECT
    
        
    return n_arr, gamma_scan, err_scan/sqrt(n_boxes)




def gamma_profile(path, tmin=None, tmax=None,n_boxes=4, min_pts_per_box=8,nsel_box_err=True,n_samples=64):   # <- number of phi_s points you want
    phi_sc, phi_t, phi_s, phi_theta = phi_extraction(path)
    # choose evenly spaced indices across phi_s
    if n_samples is None or n_samples >= len(phi_s):
        idx = np.arange(len(phi_s))
    else:
        idx = np.linspace(0, len(phi_s)-1, n_samples).astype(int)

    phi_s_sparse = phi_s[idx]
    gamma_arr = np.zeros(len(idx))

    for j, i_s in enumerate(idx):
        slopes, stderrs= gamma_box_slopes(path, i_s, tmin, tmax,n_boxes, min_pts_per_box,False, False)
        gamma_arr[j] = slopes.mean()

    return phi_s_sparse, gamma_arr


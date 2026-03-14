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
sys.path.append('/media/test-Samsung-SSD/roma/Work/orb5_analysis/scripts/')
from temp_convertion import *
from ITG_peakfinder import *

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

def omega(path, i_s, tmin, tmax):
    phi_sc, phi_t,phi_s,phi_theta=phi_extraction(path)
    dt = phi_t[1]-phi_t[0]             # time step (adjust to your data)
    i_tmin=np.where((phi_t-tmin)==0)[0][0]
    i_tmax=np.where((phi_t-tmax)==0)[0][0]
    # Extract the data at the desired radius
    phi_at_r= phi_sc[:, :, i_s]   # shape (Nt, Ntheta)
    phi_sc=phi_sc[i_tmin:i_tmax]
    # Average over theta, or pick a specific theta depending on what you want
    phi_time_series = np.mean(phi_sc[:, :, i_s], axis=1)   # shape (Nt,)
    #phi_time_series=phi_sc[:, 0, radial_index]
    # Fourier Transform in time
    freqs = np.fft.fftfreq(phi_time_series.size, d=dt)
    fft_vals = np.fft.fft(phi_time_series)

    # Only keep positive frequencies
    pos_mask = freqs > 0
    freqs = freqs[pos_mask]
    fft_vals = np.abs(fft_vals[pos_mask])

    omega=freqs[np.argmax(fft_vals)]*2*pi

    return omega

def omega_plot(path, i_s):
    phi_sc, phi_t,phi_s,phi_theta=phi_extraction(path)
    dt = phi_t[1]-phi_t[0]             # time step (adjust to your data)

    # Extract the data at the desired radius
    phi_at_r = phi_sc[:, :, i_s]   # shape (Nt, Ntheta)

    # Average over theta, or pick a specific theta depending on what you want
    phi_time_series = np.mean(phi_sc[:, :, i_s], axis=1)   # shape (Nt,)
    #phi_time_series=phi_sc[:, 0, radial_index]
    # Fourier Transform in time
    freqs = np.fft.fftfreq(phi_time_series.size, d=dt)
    fft_vals = np.fft.fft(phi_time_series)

    # Only keep positive frequencies
    pos_mask = freqs > 0
    freqs = freqs[pos_mask]
    fft_vals = np.abs(fft_vals[pos_mask])

    # Plot spectrum
    figure(figsize=(8,5))
    plot(freqs*2*pi, fft_vals, label=f'Radial index {i_s}')
    xlabel('Frequency [Omeca_ci]')
    ylabel('Amplitude')
    title('Fourier Transform of phi_sc at max mode amplitude location')
    legend()
    grid(True)
    show()
    omega=freqs[np.argmax(fft_vals)]*2*pi
    return omega

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

def omega_scan(base_path,i_s=140, nsel_max_itg=False, tmin=10000, tmax=30000, nl_slowingdown=False):
    arr=process_temperature_folders(base_path)
    omega_scan=np.zeros(len(arr))
    TH=np.zeros(len(arr))
    it=0
    for temps in arr:
        if nsel_max_itg==True:
            i_s=ITG_peak_finder(arr[temps]+'/orb5_res.h5', tmin=tmin,tmax=tmax)
            #Òprint(i_s, temps)
        omega_scan[it] = omega(arr[temps]+'/orb5_res.h5',i_s,tmin,tmax)
        TH[it]=temps
        it+=1
        #print(ITG_peak_finder(arr[temps]+'/orb5_res.h5'))###TO CORRECT
    if nl_slowingdown == True:
        E_birth=5
        for i in range(len(TH)):
            TH[i]=temperature_fin(1,TH[i]*E_birth) ###TO CORRECT

    return TH, omega_scan
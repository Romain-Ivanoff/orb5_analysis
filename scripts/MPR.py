from h5py import *
from numpy import *
from numpy.matlib import *
from matplotlib.pyplot import *
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from scipy.signal import find_peaks
import re
import sys
sys.path.append('/media/test-Samsung-SSD/roma/Work/orb5_analysis/scripts/')
from amplitude_phi import phi_extraction, ITG_peak_finder
from omega import omega
from temp_convertion import temperature_fin
from scipy.ndimage import zoom

def extract_TH_number(path):
    """
    Extracts the number that follows 'TH' in a given path string.
    '00' is interpreted as 0.
    Example: '/data/TH10_sample.txt' → 10
    """
    match = re.search(r'TH(\d+)', path)
    if match:
        num_str = match.group(1)
        num = int(num_str)
        return num
    else:
        print("No 'TH' followed by digits found in the path, taken 0.")
        return 0

def res_curve(path,TH,tmin, tmax, nsel_adhoc=True, nsel_slowingdown=False):#resonant parabola in mu-vpar space
    if path[0:6]=='/media':
        pathITG=path
    else:
        pathITG='/media/test-Samsung-SSD/roma/Work/simulations/'+path
    struct=File(pathITG,'r')
    espec_ep=array(struct["/data/var2d/fast/efspec1mn/data"])
    espec_ep_m=array(struct["/data/var2d/fast/efspec1mn/coord2"])
    jdote_ep_v = array(struct['data/var2d/fast/mpr_jdote_es/coord1'])
    #q_arr=array(struct['equil/profiles/generic/q'])
    #s_q=array(struct['equil/profiles/generic/sgrid_eq'])
    #idx = np.argmin(np.abs(s_q - s))
    #q=q_arr[idx]
    #print(w,q/ky/Tf*w)
    struct.close()

    phi_sc, phi_t,phi_s,phi_theta = phi_extraction(path)
    Tf=int(TH)
    shift=np.ones_like(jdote_ep_v)

    if nsel_slowingdown==True:
        0#To recalculate with E_birth
    if nsel_adhoc==True:
        i_s= ITG_peak_finder(path, i_time=-1)
        s=phi_s[i_s]
        w=omega(path, i_s, tmin,tmax)
        w=w*180 #in omega_ci units for adhoc case
        m=espec_ep_m[np.where(espec_ep[-1,:,0]==max(espec_ep[-1,:,0]))]
        a=180 #for adhoc case
        q=1 # hydrogen
        ky=abs(m/a)
        kappay=0.2
        mu=shift*q*w/ky/kappay-2*(jdote_ep_v)**2/2

    return mu

def smoothening(jdote_ep_mu,jdote_ep_v,jdote_ep,i_time, unsampling_rate=4):
    data_smooth = zoom(jdote_ep[i_time], (unsampling_rate, unsampling_rate),order=1,mode='nearest')  # 4x upsampling in both axes
    #jdote_ep_v = linspace(jdote_ep_v[0], jdote_ep_v[-1], data_smooth.shape[1])
    #jdote_ep_mu = linspace(jdote_ep_mu[0], jdote_ep_mu[-1], data_smooth.shape[0])
    jdote_ep_tloc=data_smooth
    jdote_ep_mu = np.linspace(jdote_ep_mu.min(), jdote_ep_mu.max(), len(jdote_ep_mu) * unsampling_rate)
    jdote_ep_v  = np.linspace(jdote_ep_v.min(), jdote_ep_v.max(), len(jdote_ep_v) * unsampling_rate)

    return jdote_ep_mu, jdote_ep_v, jdote_ep_tloc

def jdote_extraction(path, specie='D'):#path form the folder Simulations
    if path[0:6]=='/media':
        pathITG=path
    else:
        pathITG='/media/test-Samsung-SSD/roma/Work/simulations/'+path
    struct=File(pathITG,'r')
    if specie=='D':
        spec='deuterium'
    elif specie=='H':
        spec='hydrogen'
    jdote_i = array(struct['data/var2d/'+spec+'/mpr_jdote_es/data'])
    jdote_i_t = array(struct['data/var2d/'+spec+'/mpr_jdote_es/time'])
    jdote_i_v = array(struct['data/var2d/'+spec+'/mpr_jdote_es/coord1'])
    jdote_i_mu = array(struct['data/var2d/'+spec+'/mpr_jdote_es/coord2'])

    Tf=extract_TH_number(path)
    if Tf!=0:
        jdote_ep = array(struct['data/var2d/fast/mpr_jdote_es/data'])
        jdote_ep_t = array(struct['data/var2d/fast/mpr_jdote_es/time'])
        jdote_ep_v = array(struct['data/var2d/fast/mpr_jdote_es/coord1'])
        jdote_ep_mu = array(struct['data/var2d/fast/mpr_jdote_es/coord2'])
    else:
        jdote_ep,jdote_ep_t,jdote_ep_v,jdote_ep_mu=jdote_i,jdote_i_t,jdote_i_v,jdote_i_mu  
        print('No fast particles, EP power exchange set the same as background ions')
    struct.close()
    return jdote_i,jdote_i_t,jdote_i_v,jdote_i_mu,jdote_ep,jdote_ep_t,jdote_ep_v,jdote_ep_mu


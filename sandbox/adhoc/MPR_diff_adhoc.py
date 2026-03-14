from h5py import *
from numpy import *
from numpy.matlib import *
from matplotlib.pyplot import *
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from scipy.signal import find_peaks
from scipy.interpolate import griddata
import re
import sys
sys.path.append('/media/test-Samsung-SSD/roma/Work/orb5_analysis/scripts/')
from MPR import jdote_extraction, res_curve, extract_TH_number,smoothening


path_TH10='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/temperature_scan/pitagora/MPR/lin-n20-nH10-TH10/orb5_res.h5' 
path_TH05='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/temperature_scan/pitagora/MPR/lin-n20-nH10-TH02/orb5_res.h5' 

path=path_TH05
i_time=-1
TH=extract_TH_number(path_TH10)

a=jdote_extraction(path_TH05, specie='D')
jdote_i,jdote_i_t,jdote_i_v,jdote_i_mu,jdote_ep,jdote_ep_t,jdote_ep_v,jdote_ep_mu=a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7]
jdote_ep_v_init=jdote_ep_v
jdote_ep_tloc=jdote_ep[i_time]

#smoothening
rate=6
mu1,v1,t1=smoothening(jdote_ep_mu,jdote_ep_v,jdote_ep,i_time, unsampling_rate=rate)

a=jdote_extraction(path_TH10, specie='D')
jdote_i,jdote_i_t,jdote_i_v,jdote_i_mu,jdote_ep,jdote_ep_t,jdote_ep_v,jdote_ep_mu=a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7]
jdote_ep_v_init=jdote_ep_v
jdote_ep_tloc=jdote_ep[i_time]
mu2,v2,t2=smoothening(jdote_ep_mu,jdote_ep_v,jdote_ep,i_time, unsampling_rate=rate)

V1, MU1 = np.meshgrid(v1, mu1, indexing='xy')
V2, MU2 = np.meshgrid(v2, mu2, indexing='xy')

# --- FLATTEN HEATMAP 2 FOR INTERPOLATION ---
points2 = np.column_stack((V2.ravel(), MU2.ravel()))   # (x, y)
values2 = t2.ravel()

# --- INTERPOLATE HEATMAP 2 TO GRID OF HEATMAP 1 ---
t2_interp = griddata(points2, values2, (V1, MU1), method='linear')

# --- RESIDUAL ---
residual = t1 - t2_interp
tmin,tmax=10000,30000

fig1, ax1=subplots(figsize=(7,6))
heatmap2=ax1.pcolormesh(v1, mu1,  residual, shading='auto', cmap='RdBu_r')
fig1.colorbar(heatmap2, ax=ax1)
ax1.set_xlabel(r'$V_\parallel/c_s$', fontsize=18)
ax1.set_ylabel(r'$\mu \cdot B_0/\,T_i$', fontsize=18)
#ax1.set_title(f'EP Power excahnge at t={jdote_ep_t[i_time]}, TH={TH}')
mu_res=res_curve(path_TH10,TH,tmin,tmax)
ax1.plot(jdote_ep_v_init,mu_res, color='black')

ax1.set_xlim(-5,5)
ax1.set_ylim(jdote_ep_mu[0],10)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
tight_layout


#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/adhoc/maxwellian/MPR/pitagora/EP_MPR_TH10_adhoc_maxwellian.eps')

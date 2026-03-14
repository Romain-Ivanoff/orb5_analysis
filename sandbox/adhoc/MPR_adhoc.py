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
from MPR import jdote_extraction, res_curve, extract_TH_number,smoothening


path_maxw='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/temperature_scan/pitagora/MPR/lin-n20-nH10-TH10/orb5_res.h5' 
path_SD_iso='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/pitagora/isotropic/lin-n20-nH10-TH05/orb5_res.h5'
path_SD_aniso='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/pitagora/anisotropic/lin-n20-nH10-TH05/orb5_res.h5'
path_maxw_TH05='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/temperature_scan/pitagora/MPR/lin-n20-nH10-TH05/orb5_res.h5' 
path_maxw_TH02='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/temperature_scan/pitagora/MPR/lin-n20-nH10-TH02/orb5_res.h5' 
path_maxw_TH10='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/temperature_scan/pitagora/MPR/lin-n20-nH10-TH10/orb5_res.h5' 

path=path_SD_iso
path=path_maxw_TH02
i_time=-1
TH=extract_TH_number(path)

a=jdote_extraction(path, specie='D')
jdote_i,jdote_i_t,jdote_i_v,jdote_i_mu,jdote_ep,jdote_ep_t,jdote_ep_v,jdote_ep_mu=a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7]
jdote_ep_v_init=jdote_ep_v
jdote_ep_tloc=jdote_ep[i_time]
vmax=-4.969782915192666e-13
vmin=3.452868482063253e-12
#smoothening
jdote_ep_mu, jdote_ep_v, jdote_ep_tloc=smoothening(jdote_ep_mu,jdote_ep_v,jdote_ep,i_time, unsampling_rate=16)
#fig1, ax1=subplots(figsize=(7,6))
#heatmap2=ax1.pcolormesh(jdote_ep_v,jdote_ep_mu,jdote_ep_tloc, shading='auto' cmap='RdBu_r')

fig1, ax1=subplots(figsize=(7,6))
heatmap2=ax1.pcolormesh(jdote_ep_v,jdote_ep_mu,jdote_ep_tloc, shading='auto', cmap='RdBu_r', rasterized=True,vmin=vmin, vmax=vmax)
fig1.colorbar(heatmap2, ax=ax1)
ax1.set_xlabel(r'$V_\parallel/c_s$', fontsize=18)
ax1.set_ylabel(r'$\mu \cdot B_0/\,T_i$', fontsize=18)
#ax1.set_title(f'EP Power excahnge at t={jdote_ep_t[i_time]}, TH={TH}')
tmin=10000
tmax=30000
mu_res=res_curve(path,5,tmin,tmax)
ax1.plot(jdote_ep_v_init,mu_res, color='black')

ax1.set_xlim(-5,5)
ax1.set_ylim(jdote_ep_mu[0],10)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
fig1.tight_layout


#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/adhoc/maxwellian/MPR/pitagora/EP_MPR_TH10_adhoc_maxwellian.eps')
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/adhoc/maxwellian/MPR/pitagora/EP_MPR_TH10_adhoc_maxwellian.png')
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/adhoc/maxwellian/MPR/pitagora/EP_MPR_TH10_adhoc_maxwellian.pdf', dpi=300)

#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/adhoc/slowingdown/MPR/EP_MPR_TH05_TF09_adhoc_isoSD.png')
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/adhoc/slowingdown/MPR/EP_MPR_TH05_TF09_adhoc_anisoSD.pdf', dpi=300)

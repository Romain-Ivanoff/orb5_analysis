import os
import re
import sys
sys.path.append('/media/test-Samsung-SSD/roma/Work/orb5_analysis/scripts/')
from omega import *

path_ES_EP_adele='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/maxwellian-EP/T_prof/ES/nH01_dt20/orb5_res.h5'
path_ES_noEP_adele='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_adiabatic/dt20_4species/orb5_res.h5'
path_ES_noEP_kinele='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_kinetic/dt20_4species/orb5_res.h5'

path_EM_noEP='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/EM_kinetic/dt10_4species/orb5_res.h5'
path_EM_EP='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/maxwellian-EP/T_prof/EM/nH01_dt20/orb5_res.h5'

tmin=40000
tmax=90000
tmin_EM=40000
tmax_EM=100000
i_s_ITG1=100
i_s_ITG2=46
i_s_TEM=297

path=path_EM_EP
phi_sc, phi_t,phi_s,phi_theta=phi_extraction(path)

dt = phi_t[1]-phi_t[0]         
i_tmin=np.where((phi_t-tmin)==0)[0][0]
i_tmax=np.where((phi_t-tmax)==0)[0][0]
phi_sc=phi_sc[i_tmin:i_tmax]


phi_time_series = np.mean(phi_sc, axis=1)   
phi_sc=phi_time_series

Nt = phi_sc.shape[0]

Ns = phi_sc.shape[1]

freqs = np.fft.rfftfreq(Nt, d=dt)
nf = len(freqs)

fft_map = np.zeros((Ns, nf))
s_grid=linspace(0,385,385)

for i_s in range(Ns):
    fft_vals = np.fft.rfft(phi_sc[:,i_s])
    fft_map[i_s, :] = np.abs(fft_vals)

fig, ax=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))
ax.yaxis.set_major_formatter(formatter)
ax.pcolormesh(phi_s,freqs,fft_map.T,shading="auto")
ax.set_ylabel("$\omega$", size=14)
ax.set_xlabel("s", size=14)
#ax.set_ylim(0,0.0001)
rc('xtick', labelsize=14)
rc('ytick', labelsize=14)
fig.tight_layout


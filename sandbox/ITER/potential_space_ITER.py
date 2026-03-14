from h5py import *
from numpy import *
from numpy.matlib import *
from matplotlib.pyplot import *
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from scipy.signal import find_peaks
import sys



path_TH00='ITER/Relevant/TH00-dt50/orb5_res.h5'
path_TH100_nH01='ITER/Relevant/nH10/TH100-dt50/orb5_res.h5'

path=path_TH00
r_sc, z_sc=shape_extraction(path)
phi_sc, phi_t,phi_s,phi_theta=phi_extraction(path)
figure(figsize=(7,6))

norm=292.6
r_sc =r_sc/norm 
z_sc=z_sc/norm
#plot(r_sc, z_sc, linewidth=0.1)  # vessel outline in black

  # keep aspect ratio correct

t_index = 30   # choose time snapshot
phi_snapshot = phi_sc[t_index,:, : ]
plot(r_sc[:,0], z_sc[:,0], 'k', linewidth=1, label="Vessel boundary")
plot(r_sc[:,-1], z_sc[:,-1], 'k', linewidth=1, label="Vessel boundary")

pcm = pcolormesh(r_sc, z_sc, phi_snapshot, cmap="viridis", shading="auto")

#plot(r_sc[-1, :], z_sc[-1, :], 'k', linewidth=1.0)  # vessel outline
cbar=colorbar(pcm, label=r"$\phi$")
cbar.set_label(r"$\phi$", fontsize=16)
xlabel("R, m", fontsize=18)
ylabel("z, m", fontsize=18)
axis("equal")

rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
tight_layout()
#savefig('../ITER/Pictures/ITER-phi-space.pdf')
#savefig('../ITER/Pictures/ITER-phi-space.png')

s,q=q_extraction(path)
fig,ax1=subplots(figsize=(7,6))

ax1.plot(s,q, label=r'q')
ax1.set_xlabel("s", fontsize=18)
ax1.set_ylabel("q", fontsize=18)
ax1.grid()
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
#savefig('../ITER/Pictures/ITER-q.pdf')



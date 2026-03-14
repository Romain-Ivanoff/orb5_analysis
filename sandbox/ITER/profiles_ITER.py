from h5py import *
from numpy import *
from numpy.matlib import *
from matplotlib.pyplot import *
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from scipy.signal import find_peaks
import sys
sys.path.append('/media/test-Samsung-SSD/roma/ITG_from_Alexey/Scripts/')
from Space_profiles import *




path_full='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/maxwellian-EP/T_prof/ES/nH01_dt20/orb5_res.h5'
struct=File(path_full,'r')
nf=array(struct["/equil/profiles/fast/n_pic"])
ni=array(struct["/equil/profiles/hydrogen/n_pic"])
nb=array(struct["/equil/profiles/beryllium/n_pic"])
ne=array(struct["/equil/profiles/electrons/n_pic"])
nn=array(struct["/equil/profiles/neon/n_pic"])

Tf=array(struct["/equil/profiles/fast/t_pic"])
Ti=array(struct["/equil/profiles/hydrogen/t_pic"])
Tb=array(struct["/equil/profiles/beryllium/t_pic"])
Tn=array(struct["/equil/profiles/neon/t_pic"])
Te=array(struct["/equil/profiles/electrons/t_pic"])
s=array(struct["/equil/profiles/hydrogen/s_prof"]) 

Bc=array(struct["/equil/sc/B_c"]) 	
r_sc=array(struct["/equil/sc/r_c"])
z_sc=array(struct["/equil/sc/z_c"])
struct.close()
#__________________
figure(figsize=(7,6))

norm=292.6
B_norm=0.3680
r_sc =r_sc/norm 
z_sc=z_sc/norm
#plot(r_sc, z_sc, linewidth=0.1)  # vessel outline in black

  # keep aspect ratio correct

t_index = -10   # choose time snapshot
phi_snapshot = phi_sc[t_index,:, : ]

#plot(r_sc[:,0], z_sc[:,0], 'k', linewidth=1, label="Vessel boundary")
plot(r_sc[:,-1], z_sc[:,-1], 'k', linewidth=1, label="Vessel boundary")

for i in range (9):    
    #print(i)
    idx=(-i)*20
    #print(idx)
    plot(r_sc[:,idx], z_sc[:,idx], 'k', linewidth=0.5, label="Vessel boundary")
plot(r_sc[:,-180], z_sc[:,-180], 'k', linewidth=1, label="Vessel boundary")
#plot(r_sc[-45,:], z_sc[-45,:], 'k', linewidth=1, label="Vessel boundary")

pcm = pcolormesh(r_sc, z_sc, Bc/B_norm, cmap="viridis", shading="auto", rasterized=True)

#plot(r_sc[-1, :], z_sc[-1, :], 'k', linewidth=1.0)  # vessel outline
cbar=colorbar(pcm, label=r"$B$")
cbar.set_label(r"$B, T$", fontsize=16)
xlabel("R, m", fontsize=18)
ylabel("z, m", fontsize=18)
axis("equal")

rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/ITER/maxwellian/eq_profiles/B_map_ITER.pdf', dpi=300)

#______________________
n_speak_i = 3.546110000000000000e+19
T_speak_i = 7.846000000000000000e+03

n_speak_e = 4.258000000000000000e+19
T_speak_e = 8.006000000000000000e+03

n_speak_b = 8.516000000000000000e+17
T_speak_b = 7.846000000000000000e+03

n_speak_n = 3.286700000000000000e+17
T_speak_n = 7.846000000000000000e+03

n_speak_f = 4.258000000000000000e+17 
T_speak_f = 240.0000000000000000e+03

fig2,ax2=subplots(figsize=(7,6))

ax2.plot(s, Te*T_speak_e/1000,linestyle='--', label=r'$T_e$')
ax2.plot(s, Ti*T_speak_i/1000,linestyle='--', label=r'$T_i$')

ax2.plot(s, Tn*T_speak_n/1000,linestyle='--', label=r'$T_n$')
ax2.plot(s, Tb*T_speak_b/1000,linestyle='--', label=r'$T_b$')
#ax2.plot(s, Tf*T_speak_f/1000/100,linestyle='--', label=r'$T_f\,/100$')
#ax2.plot(s, Tf*T_speak_f/100000,color='k', label=r'$T_f\,/100$')
ax3=ax2.twinx()
ax3.plot(s, ne*n_speak_e, label=r'$n_e$')
ax3.plot(s, ni*n_speak_i, label=r'$n_i$')
#ax3.plot(s, nf*n_speak_f, label=r'$n_f$')
ax3.plot(s, nn*n_speak_n, label=r'$n_n$')
ax3.plot(s, nb*n_speak_b, label=r'$n_b$')

ax2.set_xlabel("s", fontsize=18)
ax2.set_ylabel(r"$T, keV$", fontsize=18)
ax3.set_ylabel(r"$n, m^{-3}$", fontsize=18)
ax2.grid()
ax2.legend(fontsize=16, loc=6)
ax3.legend(fontsize=16, loc=5)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
fig2.tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/ITER/maxwellian/eq_profiles/ITER-nT.pdf')


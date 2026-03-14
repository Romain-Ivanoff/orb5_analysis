from h5py import *
from numpy import *
from numpy.matlib import *
from matplotlib.pyplot import *
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from scipy.signal import find_peaks
import sys
sys.path.append('/media/test-Samsung-SSD/roma/ITG_from_Alexey/Scripts/')




path='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/shaped/test/n100_dt10_ntot6/orb5_res.h5'

struct=File(path,'r') 

Bc=array(struct["/equil/sc/B_c"]) 	
r_sc=array(struct["/equil/sc/r_c"])
z_sc=array(struct["/equil/sc/z_c"])
B_norm=array(struct["/equil/scalars/generic/b_norm"])
L_norm=array(struct["/equil/scalars/generic/d_norm"])
struct.close()


r_sc =r_sc/L_norm 
z_sc=z_sc/L_norm

figure(figsize=(7,6))
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
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/supra/B_space.pdf')

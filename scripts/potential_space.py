from h5py import *
from numpy import *
from numpy.matlib import *
from matplotlib.pyplot import *
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from scipy.signal import find_peaks
import os
import re
import sys
sys.path.append('/media/test-Samsung-SSD/roma/Work/orb5_analysis/scripts/')


def phi_extraction(path):
    if path[0:6]=='/media':
        pathITG=path
    else:
        pathITG='/media/test-Samsung-SSD/roma/Work/simulations/'+path
    #pathITG='/media/test-Samsung-SSD/roma/ITG_from_Alexey/Simulations/'+path
    struct=File(pathITG,'r')
    phi_sc=array(struct["/data/var2d/generic/potsc/data"])
    phi_t=array(struct["/data/var2d/generic/potsc/time"])
    phi_s=array(struct["/data/var2d/generic/potsc/coord1"])
    phi_theta=array(struct["/data/var2d/generic/potsc/coord2"])
    #dt=array(struct['/parameters/basic/dt'])
    struct.close()
    #print(dt)
    return phi_sc, phi_t,phi_s,phi_theta


def shape_extraction(path):
    if path[0:6]=='/media':
        pathITG=path
    else:
        pathITG='/media/test-Samsung-SSD/roma/Work/simulations/'+path
    struct=File(pathITG,'r')
    r_sc=array(struct["/data/var2d/generic/potsc/rsc"])
    z_sc=array(struct["/data/var2d/generic/potsc/zsc"])
    struct.close()
    return r_sc, z_sc

def plot_2D(path,it=-1):
    struct=File(path,'r')
    norm=array(struct["/equil/scalars/generic/d_norm"])
    #dt=array(struct['/parameters/basic/dt'])
    struct.close()
    
    r_sc, z_sc=shape_extraction(path)
    r_sc =r_sc/norm 
    z_sc=z_sc/norm
    phi_sc, phi_t,phi_s,phi_theta=phi_extraction(path)


    figure(figsize=(7,6))

    phi_snapshot = phi_sc[it,:, : ]
    plot(r_sc[:,0], z_sc[:,0], 'k', linewidth=1, label="Vessel boundary")
    plot(r_sc[:,-1], z_sc[:,-1], 'k', linewidth=1, label="Vessel boundary")

    pcm = pcolormesh(r_sc, z_sc, phi_snapshot/np.max(phi_snapshot), cmap="viridis", shading="auto", rasterized=True)
    
    cbar=colorbar(pcm, label=r"$\phi$", location='right')
    cbar.set_label(r"$\~{\phi}$", fontsize=16)
    xlabel("R, m", fontsize=18)
    ylabel("z, m", fontsize=18)
    axis("equal")

    rc('xtick', labelsize=16)
    rc('ytick', labelsize=16)
    tight_layout()
    return
path='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/spectrum_scan/leonardo/TH00/n16/orb5_res.h5'

plot_2D(path,it=-1)
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/adhoc/maxwellian/potential/ITG_snapshot_norm.pdf')

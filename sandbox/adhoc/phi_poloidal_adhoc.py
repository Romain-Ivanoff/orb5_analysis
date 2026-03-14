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
import sys
sys.path.append('/media/test-Samsung-SSD/roma/Work/orb5_analysis/scripts/')


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

# phi_sc shape: (nt, ntheta, nr)
# theta array: length ntheta, uniformly spaced in [0, 2π)

def decompose_theta_fourier(phi_sc):
    """
    Returns Fourier coefficients phi_m with shape (nt, m_modes, nr)
    where m_modes = ntheta (FFT ordering: [0, 1, ..., ntheta/2, -(ntheta/2-1), ..., -1])
    """
    # FFT along theta axis = 1
    phi_m = np.fft.fft(phi_sc, axis=1) / phi_sc.shape[1]
    return phi_m


base_path_TH='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/temperature_scan/pitagora/MPR/lin-n20-nH10-TH04/orb5_res.h5'
path_maxw_TH04='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/temperature_scan/pitagora/MPR/lin-n20-nH10-TH04/orb5_res.h5'
path_maxw_TH10='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/temperature_scan/pitagora/MPR/lin-n20-nH10-TH10/orb5_res.h5'
path_maxw_TH100='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/maxwellian/ES/adiabatic_electrons/temperature_scan/pitagora/MPR/lin-n20-nH10-TH100/orb5_res.h5'
path_SDi_TH10='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/pitagora/isotropic/lin-n20-nH10-TH10/orb5_res.h5'
path_SDi_TH02='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/pitagora/isotropic/lin-n20-nH10-TH02/orb5_res.h5'

phi_sc, phi_t,phi_s,phi_theta=phi_extraction(base_path_TH)


# Example usage:
phi_m = decompose_theta_fourier(phi_sc)   # shape (nt, ntheta, nr)

# Build array of m-mode numbers
ntheta = phi_sc.shape[1]
m_modes = np.fft.fftfreq(ntheta, d=1./ntheta).astype(int)

t0 = -1   # pick time index
r = np.arange(phi_sc.shape[2])

fig1,ax1=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))
ax1.yaxis.set_major_formatter(formatter)
it_min,it_max=1, None
#ax.plot(phi_t,max_pos26_TH04_maxw,label='Maxw, m=-26, TH=04')
ax1.grid()


ax1.set_xlabel(r'$i_s$', fontsize=18)
ax1.set_ylabel(r"$\phi_m$", fontsize=18)

rc('xtick', labelsize=16)
rc('ytick', labelsize=16)


 

for m_target in [-26]:
    # find index in FFT ordering
    m_idx = np.where(m_modes == m_target)[0][0]

    # radial profile of this harmonic
    phi_radial = np.abs(phi_m[t0, m_idx, :])
    #print(np.where(phi_radial == max(abs(phi_radial)))[0][0])
    ax1.plot(r, phi_radial, label=f"m={m_target}")
    
ax1.legend(fontsize=14)
fig1.tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/adhoc/maxwellian/phi_decomposition/phi_m_profiles.pdf')

#set.xlabel("Radius index")
#set.ylabel("|phi_m(r)|")

#set.title("Poloidal Fourier Harmonics of φ at time index t₀")
#set.show()

phi_radial_26 = np.abs(phi_m[:, 26, :])
max_pos=np.zeros(len(phi_t))
for i_t in range (len(phi_t)):
    max_pos[i_t]=np.where(phi_radial_26[i_t]==max(phi_radial_26[i_t]))[0][0]

#plot(phi_t,max_pos)

phi_radial_25 = np.abs(phi_m[:, 25, :])
max_pos=np.zeros(len(phi_t))
for i_t in range (len(phi_t)):
    max_pos[i_t]=np.where(phi_radial_25[i_t]==max(phi_radial_25[i_t]))[0][0]

#plot(phi_t,max_pos)




#______________________________
def max_phi_m(path,m):
    phi_sc, phi_t,phi_s,phi_theta=phi_extraction(path)
    phi_m = decompose_theta_fourier(phi_sc)
    ntheta = phi_sc.shape[1]
    m_modes = np.fft.fftfreq(ntheta, d=1./ntheta).astype(int)
    r = np.arange(phi_sc.shape[2])

    phi_radial_m = np.abs(phi_m[:, m, :])
    max_pos=np.zeros(len(phi_t))
    for i_t in range (len(phi_t)):
        max_pos[i_t]=np.where(phi_radial_m[i_t]==max(phi_radial_m[i_t]))[0][0]
    return max_pos

max_pos26_TH10_maxw=max_phi_m(path_maxw_TH10,26)
max_pos26_TH04_maxw=max_phi_m(path_maxw_TH04,26)
max_pos26_TH100_maxw=max_phi_m(path_maxw_TH100,26)

max_pos26_TH10_SDi=max_phi_m(path_SDi_TH10,26)



fig,ax=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))
ax.yaxis.set_major_formatter(formatter)
it_min,it_max=1, None
#ax.plot(phi_t,max_pos26_TH04_maxw,label='Maxw, m=-26, TH=04')
ax.plot(phi_t,max_pos26_TH10_maxw,label='Maxw, m=-26, TH=10')
ax.plot(phi_t,max_pos26_TH100_maxw,label='Maxw, m=-26, TH=100')
ax.plot(phi_t,max_pos26_TH10_SDi,label='SD iso, m=-26, TH=10')
ax.grid()
ax.legend(fontsize=14)

ax.set_xlabel(r'$t$', fontsize=18)
ax.set_ylabel(r"$i_s$", fontsize=18)

rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
fig.tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/adhoc/maxwellian/phi_decomposition/phi_mode_peak_evol.pdf')


#__________________

fig2,ax2=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))
ax2.yaxis.set_major_formatter(formatter)


for t_target in np.arange(-150, 0,10):
    # find index in FFT ordering
    

    # radial profile of this harmonic
    phi_radial = np.abs(phi_m[t_target, -26, :])
    #print(np.where(phi_radial == max(abs(phi_radial)))[0][0])
    ax2.plot(r, phi_radial/max(phi_radial), label=f"i_t={t_target}")


ax2.grid()
ax2.legend(fontsize=14)

ax2.set_xlabel(r'$t$', fontsize=18)
ax2.set_ylabel(r"$i_s$", fontsize=18)

rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
fig2.tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/adhoc/maxwellian/phi_decomposition/phi_mode_peak_evol_all.pdf')


def m_TH(path_arr):
    i=0
    fig3,ax3=subplots(figsize=(7,6))
    formatter = ScalarFormatter(useMathText=True)
    formatter.set_powerlimits((-3, 3))
    ax3.yaxis.set_major_formatter(formatter)
    arr=['Maxwellian, TH04','Maxwellian, TH10','Maxwellian, TH100','SD, iso TH10','SD, iso TH02']
    ax3.plot(0,0, color='white', label=r"$m=-26$")
    for path in path_arr:
        phi_sc, phi_t,phi_s,phi_theta=phi_extraction(path)
        #print(path)

        # Example usage:
        phi_m = decompose_theta_fourier(phi_sc)   # shape (nt, ntheta, nr)
        phi_radial = np.abs(phi_m[-1, -26, :])
        # Build array of m-mode numbers
        ntheta = phi_sc.shape[1]
        m_modes = np.fft.fftfreq(ntheta, d=1./ntheta).astype(int)

        t0 = -10   # pick time index
        r = np.arange(phi_sc.shape[2])

        
        ax3.plot(r, phi_radial/max(phi_radial),label=arr[i])
        i+=1
    ax3.grid()
    ax3.set_xlabel(r'$i_s$', fontsize=18)
    ax3.set_ylabel(r"$\phi_m$", fontsize=18)

    rc('xtick', labelsize=16)
    rc('ytick', labelsize=16)
    ax3.legend(fontsize=14, loc=2)
    fig3.tight_layout()
    #savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/adhoc/maxwellian/phi_decomposition/phi_mode_peak_evol_all_df.pdf')

    return
m_TH([path_maxw_TH04,path_maxw_TH10,path_maxw_TH100,path_SDi_TH10,path_SDi_TH02])

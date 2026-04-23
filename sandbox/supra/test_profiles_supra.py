from h5py import *
from numpy import *
from numpy.matlib import *
from matplotlib.pyplot import *
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from scipy.signal import find_peaks
from matplotlib.ticker import ScalarFormatter
import glob
import os
'''
# Load two columns: column 0 and column 1
rho, Te = np.loadtxt(
    "/media/test-Samsung-SSD/roma/Work/orb5_analysis/sandbox/suprafusion/temperature_profile_normalized.dat",
    usecols=(0, 1),
    unpack=True
)
kappan=0.235
kappat=2.35
width=0.385
speak=0.8
ne=(1-rho**2)**0.1
T_hyp=exp(-kappat*width*tanh((rho-speak)/width))
T_hyp=T_hyp/max(T_hyp)
n_hyp=exp(-kappan*width*tanh((rho-speak)/width))
n_hyp=n_hyp/max(n_hyp)

fig,ax=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))
ax.yaxis.set_major_formatter(formatter)


ax.plot(rho,Te*28,label=r'polynomial, $\nu_T=1$')
ax.plot(rho,T_hyp*28, label=r'tanh, $\kappa_T=2.35$, $w=0.385$')

ax.grid()
ax.legend(fontsize=16)
ax.set_xlabel(r'$s$', fontsize=18)
ax.set_ylabel(r"$T_e$", fontsize=18)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/adhoc_suprafusion/Te_fit.pdf')

'''
path_n110='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/noEP/ES_kin/res_test/n110_dt5_ntot7/orb5_res.h5'

struct=File(path_n110,'r')
s_q=array(struct["equil/profiles/generic/sgrid_eq"])
q=array(struct["equil/profiles/generic/q"])
n_norm=array(struct["equil/scalars/electrons/nbar"])

struct.close()

fig,ax=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))
ax.yaxis.set_major_formatter(formatter)

ax.plot(s_q,q,label=r'q')

ax.grid()
ax.legend(fontsize=16,loc=1)
ax.set_xlabel(r'$s$', fontsize=18)
ax.set_ylabel(r"$q$", fontsize=18)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/supra/q.pdf')

"plots form .dat files resulted from CHEASE equilibrium"

folder_path = '/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/inputs/equilibrium_2761_5000/' 



# --- SET YOUR FOLDER PATH HERE ---
folder_path = '/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/inputs/equilibrium_2761_5000/' 

# Define styles to cycle through so overlapping lines are visible
# Solid, dashed, dotted, dash-dot
styles = ['-', '--', ':']
widths = [3, 2.5, 2,1.5, 1.0] # Thicker lines in the back, thinner in front

# Initialize the figures
fig_t, ax_t = subplots(figsize=(7, 6))
fig_d, ax_d = subplots(figsize=(7, 6))

def format_axis(ax, title, ylabel):
    formatter = ScalarFormatter(useMathText=True)
    formatter.set_powerlimits((-2, 2))
    ax.yaxis.set_major_formatter(formatter)
    ax.set_title(title)
    ax.set_xlabel('s', fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.grid(True, linestyle='--', alpha=0.7)

search_pattern = os.path.join(folder_path, "*_profiles.dat")
files = sorted(glob.glob(search_pattern))

if not files:
    print(f"No files found in: {folder_path}")
else:
    for i, file in enumerate(files):
        base_name = os.path.basename(file)
        element = base_name.split('_')[0]
        
        # Cycle through styles and widths based on the index i
        current_style = styles[i % len(styles)]
        current_width = widths[i % len(widths)]
        
        try:
            data = np.genfromtxt(file, skip_header=1, invalid_raise=False)
            
            if data.size == 0:
                continue

            s = data[:, 0]
            temp = data[:, 1]
            density = data[:, 2]
            
            if np.max(density) <= 0:
                continue
            
            # Use linestyle and linewidth to differentiate overlaps
            ax_t.plot(s, temp, label=f'{element}', 
                      linestyle=current_style, linewidth=current_width)
            
            ax_d.plot(s, density, label=f'{element}', 
                      linestyle=current_style, linewidth=current_width)
            
        except Exception as e:
            print(f"Could not read {file}: {e}")

    format_axis(ax_t, '', r'$T$, eV')
    format_axis(ax_d, '', r'$n,m^{-3}$')
    
    ax_t.legend()
    ax_d.legend()

    fig_t.tight_layout()
    fig_d.tight_layout()
    #fig_t.savefig('/media/test-Samsung-SSD/roma/Work/Pictures/linear_ITG/supra/noEP/eq_profiles/CHEASE_temp_profile.pdf')

    
    #fig_d.savefig('/media/test-Samsung-SSD/roma/Work/Pictures/linear_ITG/supra/noEP/eq_profiles/CHEASE_density_profile.pdf')
    
    show()
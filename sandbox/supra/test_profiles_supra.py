from h5py import *
from numpy import *
from numpy.matlib import *
from matplotlib.pyplot import *
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from scipy.signal import find_peaks
from matplotlib.ticker import ScalarFormatter

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
path_n100='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/shaped/n_scan/n100_dt10_ntot7/orb5_res.h5'

struct=File(path_n100,'r')
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
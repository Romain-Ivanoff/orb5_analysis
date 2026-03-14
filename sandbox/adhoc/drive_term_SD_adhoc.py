from scipy import fftpack
import pywt
from h5py import *
from numpy import *
from numpy.matlib import *
from matplotlib.pyplot import *
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from matplotlib.ticker import ScalarFormatter
from scipy.signal import find_peaks
import re
from scipy.ndimage import zoom  
import sys
sys.path.append('/media/test-Samsung-SSD/roma/Work/orb5_analysis/scripts/')
from temp_convertion import *

def drive_sign(tau,v,eta_inv=0.15,factor=5):
    Z1=0.9
    me=5.446e-4
    M=1
    VEP=sqrt(2*tau*factor/M)
    vc=(3/4*sqrt(pi)*Z1*me/M)**(1/3)*sqrt(2/me)
    #print(vc)
    a=(VEP/vc)**3
    b=(v/vc)**3
    term=1/((1+1/a)*log(1+a))-1/(1+b)
    drive = -(eta_inv+1.5*term)
    #print(b[0]/a[0])
    return drive
def test_func(tau):
    vc=3.7*sqrt(2)
    x=tau**(3/2)*(sqrt(10)/vc)**3
    coeff=(sqrt(10)/vc)**(-1)*sqrt(2)/vc
    print(coeff)
    res=-0.15-1.5*(1/((1+1/x)*log(1+x))-1/(1+coeff*x))
    return res


def criterion(tau, factor=5):
    Z1=0.9
    me=5.446e-4
    M=1
    VEP=sqrt(2*tau*factor/M)
    vc=(3/4*sqrt(pi)*Z1*me/M)**(1/3)*sqrt(2/me)
    #print(vc)
    a=(VEP/vc)**3
    inv_eta_crit=3/2*(1-1/((1+1/a)*log(1+a)))
    #print(b[0]/a[0])

    return inv_eta_crit

tau_scan=np.linspace(0.1,30,100)
tau_disc=np.array([1,2,3,5,10,20,30])
eta_inv=0.15
tau_scan_equiv=temperature_fin(1,tau_scan*5)

inv_eta_crit=criterion(tau_scan)

fig,ax=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))
ax.yaxis.set_major_formatter(formatter)
ax.grid()
ax.legend(fontsize=16)
ax.plot(tau_scan_equiv,inv_eta_crit)
ax.plot(temperature_fin(1,tau_disc*5),criterion(tau_disc), linewidth=0, marker='o')
#print(temperature_fin(1,tau_disc*5))
ax.set_xlabel(r'$T_{f}\,/T_i$', fontsize=18)
ax.set_ylabel("criterion", fontsize=18)
ax.hlines(0.15, 0, tau_scan_equiv[-1], linestyle='--', color='r')

rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
fig.tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/adhoc/slowingdown/growthrate/temperature_scan/gama_EP_maxw_temp_scan.pdf')


'''
v1=sqrt(2*tau_scan_equiv)
v2=sqrt(2*tau_scan_equiv/2)
v3=sqrt(2*tau_scan_equiv/3)
v4=sqrt(2*tau_scan_equiv/4)
v5=sqrt(2*tau_scan_equiv/100)
drive1=drive_sign(tau_scan,v1)
drive2=drive_sign(tau_scan,v2)
drive3=drive_sign(tau_scan,v3)
drive4=drive_sign(tau_scan,v4)
drive5=drive_sign(tau_scan,v5)
#v=sqrt(2*tau)

#ax.plot(tau_scan,test_func(tau_scan))
ax.plot(tau_scan,drive1)
ax.plot(tau_scan,drive2)
ax.plot(tau_scan,drive3)
ax.plot(tau_scan,drive4)
ax.plot(tau_scan,drive5)
'''
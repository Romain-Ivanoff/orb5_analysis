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


def I2(a):
    integral= (1/3)*log(1+a**(-3))
    return integral

def I4(a):
    integral= (1/2)-a**2*(1/6*log((1-a+a**2)/(1+a)**2)+sqrt(3)**(-1)*(arctan((2-a)/(a*sqrt(3)))+pi/6))    
    return integral

def temperature_fin(Te,E_birth, me=5.446e-4,M=1,frac_fast=0.1,Z=1):#case only with mi=mEP and Zi=ZEP
    #me=0.00027 
    Z1=(1/Z-frac_fast)*Z**2
    Vc=(3/4*sqrt(pi)*Z1*me/M)**(1/3)*sqrt(2*Te/me)
    VEP=sqrt(2*E_birth/M)
    a=Vc/VEP
    I4=(1/2)-a**2*(1/6*log((1-a+a**2)/(1+a)**2)+sqrt(3)**(-1)*(arctan((2-a)/(a*sqrt(3)))+pi/6))    
    I2=(1/3)*log(1+a**(-3))
    T=2/3*I4/I2*E_birth 
    return T

def T_AUG_Vanini_benchmark():#case only with mi=mEP and Zi=ZEP
    M=1
    me=M/3676
    Te=0.709
    E_birth=93
    Z=2 #both background ions and EPs are Deuterium
    frac_fast=0.0949 #concentration of EPs/concentration of electrons
    Z1=(1/Z-frac_fast)*Z**2 #effective charge, formula 6.1 Vanini thesis
    Vc=(3/4*sqrt(pi)*Z1*me/M)**(1/3)*sqrt(2*Te/me)
    VEP=sqrt(2*E_birth/M)
    a=Vc/VEP
    I4=(1/2)-a**2*(1/6*log((1-a+a**2)/(1+a)**2)+sqrt(3)**(-1)*(arctan((2-a)/(a*sqrt(3)))+pi/6))    
    I2=(1/3)*log(1+a**(-3))
    T=2/3*I4/I2*E_birth #formula 6.18 Vanini
    return T







'''
TEP_init_arr=[1,5,10,20,30,50,100,200]
TEP_fin_arr=np.zeros(len(TEP_init_arr))

for i in range (len(TEP_init_arr)):
    TEP_fin_arr[i]=temperature_fin(1,TEP_init_arr[i])
plot(TEP_init_arr,TEP_fin_arr, marker='o')
'''
#T_AUG_Vanini_benchmark()
# #temperature_fin(1,10)
#(3.97-3.91)/3.97*100

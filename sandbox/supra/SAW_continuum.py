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

def omega_gam_adiabatic():
    '''Function to extract Omega_GAM profile for the adiabatic case with elongation from Gao 2009 paper fro the suprafusion case'''
    #________________global constants:_________________
    mi=1.67*10**(-27)
    e=1.6*10**(-19)
    
    #_____________suprafusion case parameters:_________
    el=1.58 #elongation
    tau=1
    Z=1
    Ti0=27.910*1000*1.6022*10**(-19)
    R0=6
    B0=10.55
    #_____________suprafusion profiles:_______________
    path_sim='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/noEP/ES_kin/res_test/n110_dt5_ntot7/orb5_res.h5'
    struct=File(path_sim,'r') 
    Ti=array(struct["/equil/profiles/hydrogen/t_pic"])[0:-1]
    q=array(struct["/equil/profiles/generic/q"])[0:-1]  
    struct.close()

    Ti=Ti0*Ti/max(Ti)

    #_____________prefactor calculation_______________

    ft=7/4+tau
    fs1=23/8+2*tau+tau**2/2
    fs2=(1+tau)/16
    fs3=3/8+7*tau/16+5*tau**2/32
    factor=ft**0.5*((el**2+1)/2)**(-1/2)*(1+((el**2+1)/2)*1/2/q**2*fs1/ft**2)
    omega=factor*sqrt(2)*sqrt(Ti/mi)*mi/Z/e/B0/R0
    return omega

def BAE_shift2():

    path='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/inputs/ogyropsi.h5_Roman_shaped_zerobeta'
    path_sim='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/noEP/ES_kin/res_test/n110_dt5_ntot7/orb5_res.h5'
    struct=File(path_sim,'r') 
    
    Ti=array(struct["/equil/profiles/hydrogen/t_pic"]) 
    struct.close()
    mi=1.67*10**(-27)
    e=1.6*10**(-19)
    B0=10.55
    R0=6
    Ti0=27.910*1000*1.6022*10**(-19)
    Ti=Ti0*Ti[0:-1]/max(Ti[0:-1])
    tau=1
    d_omega2=1/R0**2*2*Ti/mi*(7/4+tau)*(mi/e/B0)**2

    return d_omega2

def omega_squared(m1,m2,n):
    '''Function to calculate the toroidicity SAW continuum from the quadratic eq.'''

    path_sim='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/noEP/ES_kin/res_test/n110_dt5_ntot7/orb5_res.h5'
    struct=File(path_sim,'r') 
    q=array(struct["/equil/profiles/generic/q"])[0:-1]  
    ne=array(struct["/equil/profiles/electrons/n_pic"])[0:-1]  
    rho=array(struct["/equil/profiles/hydrogen/rho_prof"])[0:-1] 
    struct.close()
    
    #____________________constants:____________________
    e=1.6*10**(-19)
    mi=1.67*10**(-27)
    mu0=4*pi*10**(-7)

    #_____________suprafusion case parameters:_________
    a,R0,n0=1.6,6,1.66*10**(20)

    #____Benchmark, 2016 Biancalani POP case  parameters:_____
    #a,R0,n0= 0.01667,1.67,4.7*10**(19)
    
    #r_norm=(R[0]-R[0,0])/(R[0,-1]-R[0,0])
    r=rho*a
    #r=a
    
    k12=(m1-n*q)**2/R0**2/q**2
    k22=(m2-n*q)**2/R0**2/q**2
    eps2=(3*r/2/R0)**2
    n=n0*ne/max(ne)
    norm=(mi/mu0/n)*(1/e)**2
    
    omega2p=norm*((k12+k22)+sqrt((k12-k22)**2+4*eps2*k12*k22))/2/(1-eps2)   
    omega2m=norm*((k12+k22)-sqrt((k12-k22)**2+4*eps2*k12*k22))/2/(1-eps2)   
    
    return omega2p, omega2m, q,rho


fig,ax=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-2, 2))
ax.yaxis.set_major_formatter(formatter)

n_tor = 2  # Toroidal mode number
for i in range(2, 30):
    omega2p, omega2m, q, rho_tor = omega_squared(i, i+1, n_tor)
    
    # Mathematical resonance center
    q_res = (i + 0.5) / n_tor
    
    # Automated delta based on n
    delta = 0.5 / n_tor
    
    # Masking
    mask = (q > q_res - delta) & (q < q_res + delta)
    dw=(BAE_shift2())[mask]
    dw=omega_gam_adiabatic()[mask]**2
    '''
    path_sim='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/simplified_equil/noEP/ES_kin/res_test/n110_dt5_ntot7/orb5_res.h5'
    struct=File(path_sim,'r') 
        
    Ti=array(struct["/equil/profiles/hydrogen/t_pic"]) 
    struct.close()
    plot(rho_tor[mask],Ti[0:-1][mask])
    '''
    # Plotting
    ax.plot(rho_tor[mask], sqrt(omega2m[mask]+dw), color='black', linewidth=1)
    ax.plot(rho_tor[mask], sqrt(omega2p[mask]+dw), color='black', linewidth=1)
ax.plot(rho_tor[mask], sqrt(omega2p[mask]+dw), color='w',label=r'$n = $'+str(n_tor))

ax.grid()
ax.legend(fontsize=15)
ax.set_xlabel(r'$\rho$', fontsize=18)
ax.set_ylabel(r"$\omega\cdot\Omega_{ci}^{-1}$", fontsize=18)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)

#ax.set_xlim(1.9,2.6)

ax.set_ylim(0,0.003)


fig.tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/Pictures/linear_ITG/general/SAW_continuum_bench_biancalani.pdf')
#savefig('/media/test-Samsung-SSD/roma/Work/Pictures/linear_ITG/supra/noEP/SAW/SAW_continuum_supra_n'+str(n_tor)+'.pdf')
#savefig('/media/test-Samsung-SSD/roma/Work/Pictures/linear_ITG/supra/noEP/SAW/SAW_continuum_supra_n'+str(n_tor)+'.png', dpi=300, bbox_inches='tight')

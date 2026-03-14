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
from temp_convertion import temperature_fin
from gamma import ITG_peak_finder, process_temperature_folders

#function to extract jdote and Ef:
def jdote_extraction_single(path, specie):
    if path[0:6]=='/media':
        pathITG=path
    else:
        pathITG='/media/test-Samsung-SSD/roma/Work/simulations/'+path
    
    struct=File(pathITG,'r')

    jdote = array(struct['data/var2d/'+specie+'/mpr_jdote_es/data'])
    jdote_t = array(struct['data/var2d/'+specie+'/mpr_jdote_es/time'])
    jdote_v = array(struct['data/var2d/'+specie+'/mpr_jdote_es/coord1'])
    jdote_mu = array(struct['data/var2d/'+specie+'/mpr_jdote_es/coord2'])
    
    #Field energy Ef in specie:
    ef = array(struct['data/var0d/'+specie+'/efield'])
    ef_time=array(struct["/data/var0d/generic/time"])

    struct.close()
    return jdote,jdote_t,jdote_v,jdote_mu, ef,ef_time 

#Function to integrate jdote in the velovity space:
def tot_P(path,specie):
    jdote,jdote_t,jdote_v,jdote_mu, ef,ef_time=jdote_extraction_single(path,specie)
    P_tot=np.zeros(len(jdote_t))     
    
    #integration in velosity space:
    for it in range(len(jdote_t)):
        for iv in range(len(jdote_v)):
            for imu in range(len(jdote_mu)):           
                P_tot[it]+=jdote[it,imu,iv]

    return P_tot

#function to summ all the Ef_sp:
def tot_ef(path, species):
    jdote,jdote_t,jdote_v,jdote_mu, ef,ef_time=jdote_extraction_single(path,species[0])
    Ef_total_species=np.zeros(len(ef_time))

    #summing up all the contributions of Ef_sp:
    for specie in species:
        jdote,jdote_t,jdote_v,jdote_mu, ef,ef_time=jdote_extraction_single(path,specie)
        Ef_total_species+=ef
    
    #adjusting the size of ef array to the size of jdote array:
    ef_field_red=np.zeros(len(jdote_t))
    for it in range(len(jdote_t)):
        ef_field_red[it]=Ef_total_species[(np.where(abs(jdote_t[it]-ef_time)<10**(-10)))[0][0]]

    return ef_field_red

#function to calculate all the gammas:
def gamma_MPR(path, species, tstart,tfin): #list all the species in an array
    #total ef:
    ef_field_red=tot_ef(path, species)
    #array with a list of names of species, gamma and error:
    gamma_arr=np.empty((len(species),3),dtype='object')
    
    isp=0

    for specie in species:
        #integrand P/Ef calculation: 
        jdote,jdote_t,jdote_v,jdote_mu, ef,ef_time=jdote_extraction_single(path,specie)
        P_tot=tot_P(path,specie)
        p_ov_ef=P_tot/ef_field_red
        #plot(jdote_t,p_ov_ef)
        #cutting the P/Ef for a linear part of the potential growth:
        istart=np.argmin(np.abs(jdote_t-tstart))
        ifin=np.argmin(np.abs(jdote_t-tfin))
        
        p_ov_cut=p_ov_ef[istart:ifin]
        gamma_arr[isp][0]=specie
        gamma_arr[isp][1]=-mean(p_ov_cut)/2
        gamma_arr[isp][2]=std(p_ov_cut, ddof=1)/2/sqrt(len(p_ov_cut))
        isp+=1
        #axhline(y=mean(p_ov_cut), linestyle=':')
    return gamma_arr
 
def estimate_period_fft(signal, dt):
    signal_detrended = signal - np.mean(signal)
    N = len(signal_detrended)
    fft_vals = np.abs(rfft(signal_detrended))
    freqs = rfftfreq(N, dt)

    # Ignore zero freq
    fft_vals[0] = 0  
    peak_index = np.argmax(fft_vals)
    dominant_freq = freqs[peak_index]
    plot(fft_vals)
    if dominant_freq == 0:
        return None  # No periodicity detected

    period = 1.0 / dominant_freq
    
    return period

def block_average(signal, block_size):
    N = len(signal)
    n_blocks = N // block_size
    if n_blocks < 2:
        raise ValueError("Not enough blocks. Try smaller block size or longer signal.")
    trimmed = signal[:n_blocks * block_size]
    blocks = trimmed.reshape((n_blocks, block_size))
    block_means = blocks.mean(axis=1)

    avg = block_means.mean()
    err = block_means.std(ddof=1) / np.sqrt(n_blocks)
    return avg, err

'''
def gamma_MPR_EGAM(path, species, tstart,tfin):
    #total ef:
    ef_field_red=tot_ef(path, species)
    #array with a list of names of species, gamma and error:
    gamma_arr=np.empty((len(species),3),dtype='object')
    
    isp=0
    for specie in species:   
        #integrand P/Ef calculation: 
        jdote,jdote_t,jdote_v,jdote_mu, ef,ef_time=jdote_extraction_single(path,specie)
        P_tot=tot_P(path,specie)
        p_ov_ef=P_tot/ef_field_red
        #plot(jdote_t,p_ov_ef)
        #cutting the P/Ef for a linear part of the potential growth:
        istart=np.where(abs(jdote_t-tstart)<10**(-10))[0][0]
        ifin=np.where(abs(jdote_t-tfin)<10**(-10))[0][0]
        p_ov_cut=p_ov_ef[istart:ifin]
        dt=jdote_t[1]-jdote_t[0]
        period = estimate_period_fft(p_ov_cut, dt)
        if period is None:
            print("No clear period found. Using default block size.")
            block_size = 10
        else:
            print(f"Estimated period: {period:.3f} (in time units)")
            block_size = int(period / dt*3)
            print(block_size)
        mean, error = block_average(p_ov_cut, block_size)

        gamma_arr[isp][0]=specie
        gamma_arr[isp][1]=-mean/2
        gamma_arr[isp][2]=error/2
        isp+=1
        
        #axhline(y=mean(p_ov_cut), linestyle=':')
        
    return gamma_arr
'''

#____________________________________________________
#Repeating the same thing but with already averaged diagnostics jdote_tot:
#you can change it in the gamma_MPR_temp_scan:

def jdote_av_extraction(path,specie):
    if path[0:6]=='/media':
        pathITG=path
    else:
        pathITG='/media/test-Samsung-SSD/roma/Work/simulations/'+path
    struct=File(pathITG,'r')
    jdote=array(struct["/data/var0d/"+specie+"/jdote_tot"])
    time=array(struct["/data/var0d/generic/time"])

    #Field energy Ef in specie:
    ef = array(struct['data/var0d/'+specie+'/efield'])
    ef_time=array(struct["/data/var0d/generic/time"])


    struct.close()
    
    return time, jdote, ef,ef_time 

def tot_P_av(path,specie):
    jdote_t_av,jdote_av, ef,ef_time =jdote_av_extraction(path,specie)
    P_tot=jdote_av 

    return P_tot

def tot_ef_av(path, species):
    #jdote,jdote_t,jdote_v,jdote_mu, ef,ef_time=jdote_extraction_single(path,species[0])
    jdote_t_av,jdote_av, ef,ef_time =jdote_av_extraction(path,species[0])
    Ef_total_species=np.zeros(len(ef_time))

    #summing up all the contributions of Ef_sp:
    for specie in species:
        #jdote,jdote_t,jdote_v,jdote_mu, ef,ef_time=jdote_extraction_single(path,specie)
        jdote_t_av,jdote_av, ef,ef_time=jdote_av_extraction(path,specie)
        Ef_total_species+=ef
    
    #adjusting the size of ef array to the size of jdote array:
    ef_field_red=np.zeros(len(jdote_t_av))
    for it in range(len(jdote_t_av)):
        ef_field_red[it]=Ef_total_species[(np.where(abs(jdote_t_av[it]-ef_time)<10**(-10)))[0][0]]

    return ef_field_red

def gamma_MPR_av(path, species, tmin,tmax): #list all the species in an array
    #total ef:
    ef_field_red=tot_ef_av(path, species)
    #array with a list of names of species, gamma and error:
    gamma_arr=np.empty((len(species),3),dtype='object')
    
    isp=0

    for specie in species:
        #integrand P/Ef calculation: 
        jdote_t_av,jdote_av, ef,ef_time=jdote_av_extraction(path,specie)
        #P_tot=tot_P(path,specie)#correct!!!!!!!!!
        #print(P_tot)
        P_tot=tot_P_av(path,specie)
        #print(P_tot)
        p_ov_ef=P_tot/ef_field_red
        
        #cutting the P/Ef for a linear part of the potential growth:
        istart=np.argmin(np.abs(jdote_t_av-tmin))
        ifin=np.argmin(np.abs(jdote_t_av-tmax))
        
        p_ov_cut=p_ov_ef[istart:ifin]
        
        #plot(jdote_t_av[istart:ifin],p_ov_cut)
        #plot(P_tot[istart:ifin])
        gamma_arr[isp][0]=specie
        gamma_arr[isp][1]=-mean(p_ov_cut)/2
        gamma_arr[isp][2]=std(p_ov_cut, ddof=1)/2/sqrt(len(p_ov_cut))
        #print(gamma_arr[isp][1])
        isp+=1
        
        #axhline(y=mean(p_ov_cut), linestyle=':')
    return gamma_arr

#func for the temperature scan: you can choose between gamma_MPR_av and gamma_MPR inside
def gamma_MPR_temp_scan(base_path,species, tmin=None, tmax=None, nl_slowingdown=False):
    arr=process_temperature_folders(base_path)
    gamma_scan=np.zeros((len(arr),len(species),3),dtype='object')
    TH=np.zeros(len(arr))
    it=0
    for temps in arr:
        gamma_scan[it]=gamma_MPR_av(arr[temps]+'/orb5_res.h5', species, tmin,tmax)

        TH[it]=temps
        it+=1
    if nl_slowingdown == True:
        E_birth=5
        for i in range(len(TH)):
            TH[i]=temperature_fin(1,TH[i]*E_birth) ###TO CORRECT
    
        
    return TH, gamma_scan


#path_iso_test1='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/pitagora/isotropic/resolution_test/lin-n20-nH10-TH30/orb5_res.h5' 
#path_iso_test2='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/pitagora/isotropic/resolution_test/lin-n20-nH10-TH30-kap7/orb5_res.h5' 
#tmin, tmax=10000,30000
#species=['deuterium','fast']
#gamma_MPR_av(path_iso_test1, species, tmin,tmax)

#gamma_MPR_av(path_iso_test2, species, tmin,tmax)

from h5py import *
from numpy import *
from numpy.matlib import *
from matplotlib.pyplot import *
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from scipy.signal import find_peaks
from matplotlib.ticker import ScalarFormatter

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

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

def ampltude_phi(path):#Extract the growth evolution of the scalar potential
    phi_sc, phi_t,phi_s,phi_theta=phi_extraction(path)
    s=120
    #s=101 #ITER
    # max_pol_av_s: evolution in time by taking maximum value of the phi in poloidal direction and averaging it in radial scan
    max_pol_av_s=np.zeros(len(phi_t))
    #max_pol_130: evolution in time by taking maximum value of phi in poloidal direction at the s[130]
    max_pol_130=np.zeros(len(phi_t))
    #av_pol_130: evolution in time by taking average in theta at the s[130]
    av_pol_130=np.zeros(len(phi_t))

    for i in range(len(phi_t)):
        for j in range (len(phi_s)):
            max_pol_av_s[i]+=np.max(phi_sc[i,:,j])
        max_pol_130[i]=np.max(phi_sc[i,:,s])

        for j in range (len(phi_theta)):
            av_pol_130[i]+=phi_sc[i,j,s]
    
    av_pol_130=av_pol_130/len(phi_theta)
    
    max_pol_av_s=max_pol_av_s/len(phi_s)
   
   
    semilogy(phi_t,max_pol_130)
    xlabel(r'$t\cdot\Omega_{ci}$', fontsize=18)
    ylabel(r'$log\phi$', fontsize=18)
    rc('xtick', labelsize=16)
    rc('ytick', labelsize=16)

    formatter1 = ScalarFormatter(useMathText=True)
    formatter1.set_powerlimits((-3, 3))
    


    return phi_t, max_pol_av_s, max_pol_130

def ampltude_phi_legend(path, legend,i_s):#Extract the growth evolution of the scalar potential
    phi_sc, phi_t,phi_s,phi_theta=phi_extraction(path)
    #s=120
    #s=100 #ITER
    #s=372 #ITER outmost initial pert
    #s=140
    # max_pol_av_s: evolution in time by taking maximum value of the phi in poloidal direction and averaging it in radial scan
    max_pol_av_s=np.zeros(len(phi_t))
    #max_pol_130: evolution in time by taking maximum value of phi in poloidal direction at the s[130]
    max_pol_130=np.zeros(len(phi_t))
    #av_pol_130: evolution in time by taking average in theta at the s[130]
    av_pol_130=np.zeros(len(phi_t))
    #print(phi_s[i_s])
    for i in range(len(phi_t)):
        for j in range (len(phi_s)):
            max_pol_av_s[i]+=np.max(phi_sc[i,:,j])
        max_pol_130[i]=np.max(phi_sc[i,:,i_s])

        for j in range (len(phi_theta)):
            av_pol_130[i]+=phi_sc[i,j,i_s]
    
    av_pol_130=av_pol_130/len(phi_theta)
    
    max_pol_av_s=max_pol_av_s/len(phi_s)
   
    
    semilogy(phi_t/10000,max_pol_130, label=legend)
    xlabel(r'$t\cdot10^4\,\Omega_{ci}$', fontsize=18)
    ylabel(r'$log\phi$', fontsize=18)
    
    rc('xtick', labelsize=16)
    rc('ytick', labelsize=16)

    formatter1 = ScalarFormatter(useMathText=True)
    formatter1.set_powerlimits((-3, 3))
    
    return phi_t, max_pol_av_s, max_pol_130
"""
def ITG_peak_finder(path,i_time=-1):
    #Function to find the peak of the ITG by takinfg the average in poloidal plane 
    #By default it is suited for linear simulations, as it uses last time moment, but i_time can be used any
    phi_sc, phi_t,phi_s,phi_theta = phi_extraction(path)
    '''
    aver_phi=np.zeros((len(phi_t),len(phi_s)))
    for i_t in range (len(phi_t)):
        for i_s in range (len(phi_s)):
            aver_phi[i_t,i_s]=sum(phi_sc[i_t,:,i_s])
    i_s_max=(np.where(aver_phi[i_time]==max(aver_phi[i_time])))[0][0]
    '''
    phi_at_t=phi_sc[i_time]
    phi_at_t_theta0=phi_at_t[0]
    phi_av=np.zeros(len(phi_s))
    for i_s in range (len(phi_s)):
        phi_av[i_s]=sum(abs(phi_at_t[:,i_s]))

    i_s_max=(np.where(phi_av==max(phi_av)))[0][0]
    #print(len(phi_s))
    return i_s_max
"""
def phi_space_plot(path, i_t=-1):
    phi_sc, phi_t,phi_s,phi_theta=phi_extraction(path)
    fig,ax=subplots(figsize=(10,5))
    heatmap = ax.pcolormesh(phi_s,phi_theta, phi_sc[i_t], shading='auto', cmap='RdBu_r')
    rc('xtick', labelsize=16)
    rc('ytick', labelsize=16)
    ax.set_xlabel(r"s", fontsize=18)
    ax.set_ylabel(r"$\theta$", fontsize=18)
    i_s_max=ITG_peak_finder(path,i_t)
    s_max=phi_s[i_s_max]
    print('Mode i_s=',i_s_max,'s=',s_max)
    return 1

#adhoc_path='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/noEP/toroidal_scans/lx540/n30/orb5_res.h5'

#phi_space_plot(adhoc_path)
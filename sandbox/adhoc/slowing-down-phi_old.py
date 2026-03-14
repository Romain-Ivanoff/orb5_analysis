
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
sys.path.append('/media/test-Samsung-SSD/roma/ITG_from_Alexey/Scripts/')
#sys.path.append('/media/test-Samsung-SSD/roma/Work/orb5_analysis/scripts/')
from gamma import *
#from gamma import gamma_E
#from amplitude_phi import ampltude_phi
from temp_convertion import temperature_fin
ta=10000
tb=20000
arr_ksi_path=['0','-01','-02','-02','-03','-04','-05','-06','-07','-08','-09']
arr_ksi_int=[0,-0.1,-0.2,-0.2,-0.3,-0.4,-0.5,-0.6,-0.7,-0.8,-0.9]
arr_sigma_path=['01','02','03','05','075','1','2']
arr_sigma_int=[0.1,0.2,0.3,0.5,0.75,1,2]


#phi evolution plots_______________________________________________________________
'''
for ipath in arr_ksi_path:
    ampltude_phi('slowingdown/anisotropic/ksi-scan-sigma02/ksi-'+ipath+'/orb5_res.h5')

for ipath in arr_sigma_path:
    ampltude_phi('slowingdown/anisotropic/sigma-scan/sigma-'+ipath+'/orb5_res.h5')
'''

#Temperature scan___________________________________________________________
def temp_scan():
    TH=[5,10,20,30,100]#,200]
    TH_str=['05','10','20','30','100']#,'200']
    TH_SD_fin=np.zeros(len(TH))
    for i in range(len(TH)):
        TH_SD_fin[i]=temperature_fin(1,TH[i]*5) ###TO CORRECT
    TH_old=TH
    TH=TH_SD_fin
    
    
    
    gamma_TH_scan_ksi08=np.zeros(len(TH))
    err_TH_scan_ksi08=np.zeros(len(TH))

    gamma_TH_scan_ksi03=np.zeros(len(TH))
    err_TH_scan_ksi03=np.zeros(len(TH))

    gamma_TH_scan_iso=np.zeros(len(TH))
    err_TH_scan_iso=np.zeros(len(TH))

    gamma_TH_max=np.zeros(len(TH))
    err_TH_max=np.zeros(len(TH))

    gamma_TH_scan_sigma01=np.zeros(len(TH))
    err_TH_scan_sigma01=np.zeros(len(TH))

    a,b,gamma_nH0,err_nH0=gamma_averaged('Alexey-case/lin-n20-nH10-TH00/orb5_res.h5', ta, tb)

    #a,b,gamma_nH1_TH100,err_nH1_TH100=gamma_averaged('Alexey-case/const-beta/leonardo/lin-n20-nH1-TH100/orb5_res.h5', ta, tb)

    #a,b,gamma_nH5_TH20,err_nH5_TH20=gamma_averaged('Alexey-case/const-beta/leonardo/lin-n20-nH5-TH20/orb5_res.h5', ta, tb)

    #a,b,gamma_nH20_TH5,err_nH20_TH5=gamma_averaged('Alexey-case/const-beta/leonardo/lin-n20-nH20-TH05/orb5_res.h5', ta, tb)


    for i in range(len(gamma_TH_scan_ksi08)):
        a,b,gamma_TH_scan_ksi08[i],err_TH_scan_ksi08[i]=gamma_averaged('Alexey-case/slowingdown/anisotropic/TH-ksi-08-sigma02/lin-n20-nH10-TH'+TH_str[i]+'/orb5_res.h5', ta, tb)
        a,b,gamma_TH_scan_ksi03[i],err_TH_scan_ksi03[i]=gamma_averaged('Alexey-case/slowingdown/anisotropic/TH-ksi-03-sigma02/lin-n20-nH10-TH'+TH_str[i]+'/orb5_res.h5', ta, tb)
        a,b,gamma_TH_scan_iso[i],err_TH_scan_iso[i]=gamma_averaged('Alexey-case/slowingdown/isotropic/lin-n20-nH10-TH'+TH_str[i]+'/orb5_res.h5', ta, tb)
        a,b,gamma_TH_max[i],err_TH_max[i]=gamma_averaged('Alexey-case/gamma-comparison-SD/lin-n20-nH10-TH'+TH_str[i]+'/orb5_res.h5', ta, tb)
        a,b,gamma_TH_scan_sigma01[i],err_TH_scan_sigma01[i]=gamma_averaged('Alexey-case/slowingdown/anisotropic/TH-ksi-08-sigma01/lin-n20-nH10-TH'+TH_str[i]+'/orb5_res.h5', ta, tb)

    fig2, ax2= subplots(figsize=(7,6))
    formatter2 = ScalarFormatter(useMathText=True)
    formatter2.set_powerlimits((-3, 3))
    ax2.yaxis.set_major_formatter(formatter2)
    ax2.errorbar(TH,gamma_TH_scan_ksi03,err_TH_scan_ksi03, marker='o',linestyle='-.', capsize=5,label=r'$\xi=-0.3,\, \sigma=0.2$')
    ax2.errorbar(TH,gamma_TH_scan_ksi08,err_TH_scan_ksi08, marker='o',linestyle='-.', capsize=5,label=r'$\xi=-0.8,\, \sigma=0.2$')
    ax2.errorbar(TH,gamma_TH_scan_sigma01,err_TH_scan_sigma01, marker='o',linestyle='-.', capsize=5,label=r'$\xi=-0.8,\, \sigma=0.1$')

    ax2.errorbar(TH,gamma_TH_scan_iso,err_TH_scan_iso, marker='o',linestyle='-', capsize=5,label=r'isotropic')

    ax2.errorbar(TH_old,gamma_TH_max,err_TH_max, marker='o',linestyle='-',color='black', capsize=5,label=r'$Maxwellian$')

    #ax2.errorbar(0,gamma_nH0,err_nH0, marker='o', capsize=5,label=r'$n_f=0$')
    '''
    ax2.errorbar(100,gamma_nH1_TH100,err_nH1_TH100, marker='o', capsize=5,label=r'$n_f=1\%$')

    ax2.errorbar(20,gamma_nH5_TH20,err_nH5_TH20, marker='o', capsize=5,label=r'$n_f=5\%$')

    ax2.errorbar(5,gamma_nH20_TH5,err_nH20_TH5, marker='o', capsize=5,label=r'$n_f=20\%$')
    '''
    #ax2.set_xlim(-2,45) ###TO CORRECT
    ax2.grid(True)
    ax2.set_xlabel(r'$T_{EP}/T_i$', fontsize=18)
    ax2.set_ylabel(r"$\gamma/\Omega_{ci}$", fontsize=18)
    ax2.legend(fontsize=16)
    rc('xtick', labelsize=16)
    rc('ytick', labelsize=16)
    fig2.tight_layout()
    #savefig('Pictures/gamma_all_TH_profile.pdf')
#____________________________________________________________________________________

#Ksi-scan____________________________________________________________________________
def ksi_scan():
    fig, ax= subplots(figsize=(7,6))
    formatter = ScalarFormatter(useMathText=True)
    formatter.set_powerlimits((-3, 3))
    ax.yaxis.set_major_formatter(formatter)

    gamma_ksi_sigma01, err_ksi_sigma01,gamma_ksi_sigma02,err_ksi_sigma02=np.zeros(len(arr_ksi_path)),np.zeros(len(arr_ksi_path)),np.zeros(len(arr_ksi_path)),np.zeros(len(arr_ksi_path))
    gamma_ksi_sigma03, err_ksi_sigma03,gamma_ksi_sigma04,err_ksi_sigma04=np.zeros(len(arr_ksi_path)),np.zeros(len(arr_ksi_path)),np.zeros(len(arr_ksi_path)),np.zeros(len(arr_ksi_path))
    #__________________________FOR TH=10:___________________________
    i=0
    path_ksi_start='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/ksi-scan/leonardo/'
    for ipath in arr_ksi_path:    
        path=path_ksi_start+'ksi-scan-sigma01/ksi-'+ipath+'/orb5_res.h5'
        a,b, gamma_ksi_sigma01[i], err_ksi_sigma01[i]=gamma_averaged(path, ta, tb)
        path=path_ksi_start+'/ksi-scan-sigma02/ksi-'+ipath+'/orb5_res.h5'
        a,b, gamma_ksi_sigma02[i], err_ksi_sigma02[i]=gamma_averaged(path, ta, tb)
        path=path_ksi_start+'/ksi-scan-sigma03/ksi-'+ipath+'/orb5_res.h5'
        a,b, gamma_ksi_sigma03[i], err_ksi_sigma03[i]=gamma_averaged(path, ta, tb)
        path=path_ksi_start+'/ksi-scan-sigma04/ksi-'+ipath+'/orb5_res.h5'
        a,b, gamma_ksi_sigma04[i], err_ksi_sigma04[i]=gamma_averaged(path, ta, tb)
        i+=1
   
    a,b,gamma_TH_scan_iso,err_TH_scan_iso=gamma_averaged('/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/temperature_scan/leonardo/isotropic/lin-n20-nH10-TH10/orb5_res.h5', ta, tb)
    
    ax.axhline(gamma_TH_scan_iso, color='white',label=r'$T_f=10\,T_i$:')
    ax.axhline(gamma_TH_scan_iso, color='black',label=r'isotropic')  
    ax.errorbar(arr_ksi_int,gamma_ksi_sigma01,err_ksi_sigma01, marker='o',capsize=5,linewidth=0.8, label=r'$\sigma=0.1,\,T_f=10\,T_i$')
    ax.errorbar(arr_ksi_int,gamma_ksi_sigma02,err_ksi_sigma02, marker='o',capsize=5,linewidth=0.8, label=r'$\sigma=0.2$')
    ax.errorbar(arr_ksi_int,gamma_ksi_sigma03,err_ksi_sigma03, marker='o',capsize=5,linewidth=0.8, label=r'$\sigma=0.3$')
    ax.errorbar(arr_ksi_int,gamma_ksi_sigma04,err_ksi_sigma04, marker='o',capsize=5,linewidth=0.8, label=r'$\sigma=0.4$')
    

    #____________________________SAME_FOR_TH=100_________________________:
    i=0
    path_ksi_start='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/adhoc/slowingdown/ES/adiabatic_electrons/ksi-scan-TH100/leonardo/'
    for ipath in arr_ksi_path:
        path=path_ksi_start+'ksi-scan-sigma01/ksi-'+ipath+'/orb5_res.h5'
        a,b, gamma_ksi_sigma01[i], err_ksi_sigma01[i]=gamma_averaged(path, ta, tb)
        path=path_ksi_start+'ksi-scan-sigma03/ksi-'+ipath+'/orb5_res.h5'
        a,b, gamma_ksi_sigma03[i], err_ksi_sigma03[i]=gamma_averaged(path, ta, tb)
        path=path_ksi_start+'ksi-scan-sigma04/ksi-'+ipath+'/orb5_res.h5'
        a,b, gamma_ksi_sigma04[i], err_ksi_sigma04[i]=gamma_averaged(path, ta, tb)
        i+=1
    

    #ax.axhline(gamma_TH_scan_iso, color='white',label=r'$T_f=100\,T_i$:')
    #ax.errorbar(arr_ksi_int,gamma_ksi_sigma01,err_ksi_sigma01, marker='o',capsize=5,linewidth=0.8, label=r'$\sigma=0.1,\,T_f=100\,T_i$')
    #ax.errorbar(arr_ksi_int,gamma_ksi_sigma03,err_ksi_sigma03, marker='o',capsize=5,linewidth=0.8, label=r'$\sigma=0.3,\,T_f=100\,T_i$')
    #ax.errorbar(arr_ksi_int,gamma_ksi_sigma04,err_ksi_sigma04, marker='o',capsize=5,linewidth=0.8, label=r'$\sigma=0.4,\,T_f=100\,T_i$')
    

    ax.grid(True)
    ax.set_xlabel(r'$\xi$', fontsize=18)
    ax.set_ylabel(r"$\gamma/\Omega_{ci}$", fontsize=18)
    ax.legend(fontsize=16)
    rc('xtick', labelsize=16)
    rc('ytick', labelsize=16)
    ax.set_ylim(0.00039,0.00041)
    #ax.set_ylim(0.0003945,0.0003985)
    fig.tight_layout()
    savefig('Pictures/gama_ksi_profile_all.pdf')
    #savefig('Pictures/gama_ksi_profile_all_TH100.pdf')
#____________________________________________________________________________________

#Sigma-scan__________________________________________________________________________
def sigma_scan():
    fig1, ax1= subplots(figsize=(7,6))
    formatter1 = ScalarFormatter(useMathText=True)
    formatter1.set_powerlimits((-3, 3))
    ax1.yaxis.set_major_formatter(formatter1)
    gamma_sigma_av, err_sigma_av, gamma_sigma_130, err_sigma_130=np.zeros(len(arr_sigma_path)),np.zeros(len(arr_sigma_path)),np.zeros(len(arr_sigma_path)),np.zeros(len(arr_sigma_path))
    j=0
    for jpath in arr_sigma_path:
        path='Alexey-case/slowingdown/anisotropic/sigma-scan/sigma-'+jpath+'/orb5_res.h5'
        gamma_sigma_av[j], err_sigma_av[j], gamma_sigma_130[j], err_sigma_130[j]=gamma_averaged(path, ta, tb)
        j+=1

    
    ax1.errorbar(0.2,gamma_TH_scan_ksi08[4],err_TH_scan_ksi08[4], color='white',label=r'$\xi=-0.8$') 
    ax1.errorbar(0.2,gamma_TH_scan_ksi08[0],err_TH_scan_ksi08[0],marker='o',capsize=5, color='black',label=r'$T_f=5\,T_i$') 
    ax1.errorbar(arr_sigma_int,gamma_sigma_130,err_sigma_130, marker='o',capsize=5, label=r'$T_f=10\,T_i$')
    ax1.errorbar(0.2,gamma_TH_scan_ksi08[2],err_TH_scan_ksi08[2], marker='o', capsize=5, label=r'$T_f=20\,T_i$') 
    ax1.errorbar(0.2,gamma_TH_scan_ksi08[3],err_TH_scan_ksi08[3], marker='o', capsize=5, label=r'$T_f=30\,T_i$') 
    ax1.errorbar(0.2,gamma_TH_scan_ksi08[4],err_TH_scan_ksi08[4], marker='o', capsize=5, label=r'$T_f=100\,T_i$') 
    ax1.errorbar(0.2,gamma_TH_scan_ksi08[5],err_TH_scan_ksi08[5], marker='o', capsize=5, label=r'$T_f=200\,T_i$') 
    #ax1.errorbar(0.2,gamma_10_iso,err_10_iso, marker='o', capsize=5, label=r'$T_f=10\,T_i$, iso') 
    #ax1.errorbar(0.2,gamma_100_iso,err_100_iso, marker='o', capsize=5, label=r'$T_f=100\,T_i$, iso') 

    ax1.grid(True)
    ax1.set_xlabel(r'$\sigma$', fontsize=18)
    ax1.set_ylabel(r"$\gamma/\Omega_{ci}$", fontsize=18)
    ax1.legend(fontsize=16)
    rc('xtick', labelsize=16)
    rc('ytick', labelsize=16)
    fig1.tight_layout()
    #savefig('Pictures/gama_sigma_profile.pdf')
    return
#____________________________________________________________________________________
#ksi-heatmap
def ksi_heatmap():
    gamma_ksi_sigma01, err_ksi_sigma01,gamma_ksi_sigma02,err_ksi_sigma02=np.zeros(len(arr_ksi_path)),np.zeros(len(arr_ksi_path)),np.zeros(len(arr_ksi_path)),np.zeros(len(arr_ksi_path))
    gamma_ksi_sigma03, err_ksi_sigma03,gamma_ksi_sigma04,err_ksi_sigma04=np.zeros(len(arr_ksi_path)),np.zeros(len(arr_ksi_path)),np.zeros(len(arr_ksi_path)),np.zeros(len(arr_ksi_path))

    i=0
    for ipath in arr_ksi_path:
        path='Alexey-case/slowingdown/anisotropic/ksi-scan/ksi-scan-sigma01/ksi-'+ipath+'/orb5_res.h5'
        a,b, gamma_ksi_sigma01[i], err_ksi_sigma01[i]=gamma_averaged(path, ta, tb)
        path='Alexey-case/slowingdown/anisotropic/ksi-scan/ksi-scan-sigma02/ksi-'+ipath+'/orb5_res.h5'
        a,b, gamma_ksi_sigma02[i], err_ksi_sigma02[i]=gamma_averaged(path, ta, tb)
        path='Alexey-case/slowingdown/anisotropic/ksi-scan/ksi-scan-sigma03/ksi-'+ipath+'/orb5_res.h5'
        a,b, gamma_ksi_sigma03[i], err_ksi_sigma03[i]=gamma_averaged(path, ta, tb)
        path='Alexey-case/slowingdown/anisotropic/ksi-scan/ksi-scan-sigma04/ksi-'+ipath+'/orb5_res.h5'
        a,b, gamma_ksi_sigma04[i], err_ksi_sigma04[i]=gamma_averaged(path, ta, tb)
        i+=1

    from matplotlib.ticker import ScalarFormatter

    fig2, ax2 = subplots(figsize=(7, 6))

    # Axis formatter for y-axis
    formatter2 = ScalarFormatter(useMathText=True)
    formatter2.set_powerlimits((-3, 3))
    ax2.yaxis.set_major_formatter(formatter2)

    # Data preparation
    sigma_ksi_data = [gamma_ksi_sigma01, gamma_ksi_sigma02, gamma_ksi_sigma03, gamma_ksi_sigma04]
    sigma = [0.1, 0.2, 0.3, 0.4]
    ksi = arr_ksi_int
    KSI, SIGMA = meshgrid(ksi, sigma)

    #Optional smoothing (commented by default)
    '''
    from scipy.ndimage import zoom
    data_smooth = zoom(sigma_ksi_data, (4, 4))  # 4x upsampling in both axes
    x_smooth = linspace(ksi[0], ksi[-1], data_smooth.shape[1])
    y_smooth = linspace(sigma[0], sigma[-1], data_smooth.shape[0])
    heatmap2 = ax2.pcolormesh(x_smooth, y_smooth, data_smooth, shading='auto', cmap='RdBu_r')
    '''
    # Plot heatmap without smoothing
    heatmap2 = ax2.pcolormesh(KSI, SIGMA, sigma_ksi_data, shading='auto', cmap='RdBu_r')

    # Add colorbar and format ticks
    cbar = fig2.colorbar(heatmap2, ax=ax2)
    cbar_formatter = ScalarFormatter(useMathText=True)
    cbar_formatter.set_powerlimits((-3, 3))
    cbar.ax.yaxis.set_major_formatter(cbar_formatter)

    # Labels and layout
    ax2.set_xlabel(r'$\xi$', fontsize=18)
    ax2.set_ylabel(r'$\sigma$', fontsize=18)
    rc('xtick', labelsize=16)
    rc('ytick', labelsize=16)
    fig2.tight_layout()

    #savefig('Pictures/gamma_heatmap_smooth.pdf')
    #savefig('Pictures/gamma_heatmap_smooth.png')

    #savefig('Pictures/gamma_heatmap.pdf')
    #savefig('Pictures/gamma_heatmap.png')
    return

def temp_scan_maxw():
    TH=[5,10,20,30,100]#,200]
    TH_str=['05','10','20','30','100']#,'200']
    gamma_TH_max=np.zeros(len(TH))
    err_TH_max=np.zeros(len(TH))
    
    a,b,gamma_nH0,err_nH0=gamma_averaged('Alexey-case/const-beta/new/lin-n20-nH10-TH00/orb5_res.h5', ta, tb)
    #a,b,gamma_nH0,err_nH0=gamma_averaged('Alexey-case/lin-n20-nH10-TH00/orb5_res.h5', ta, tb)

    a,b,gamma_nH1_TH100,err_nH1_TH100=gamma_averaged('Alexey-case/const-beta/new/lin-n20-nH1-TH100/orb5_res.h5', ta, tb)

    a,b,gamma_nH5_TH20,err_nH5_TH20=gamma_averaged('Alexey-case/const-beta/new/lin-n20-nH5-TH20/orb5_res.h5', ta, tb)

    a,b,gamma_nH20_TH5,err_nH20_TH5=gamma_averaged('Alexey-case/const-beta/new/lin-n20-nH20-TH05/orb5_res.h5', ta, tb)

    a,b,gamma_nH25_TH4,err_nH25_TH4=gamma_averaged('Alexey-case/const-beta/new/lin-n20-nH25-TH04/orb5_res.h5', ta, tb)

    a,b,gamma_nH50_TH2,err_nH50_TH2=gamma_averaged('Alexey-case/const-beta/new/lin-n20-nH50-TH02/orb5_res.h5', ta, tb)

    a,b,gamma_nH100_TH1,err_nH100_TH1=gamma_averaged('Alexey-case/const-beta/new/lin-n20-nH100-TH01/orb5_res.h5', ta, tb)
    
    a,b,gamma_nH0_TH10,err_nH10_TH10=gamma_averaged('Alexey-case/const-beta/new/lin-n20-nH10-TH10/orb5_res.h5', ta, tb)
    err_const_beta=[err_nH100_TH1,err_nH50_TH2,err_nH25_TH4,err_nH20_TH5,err_nH10_TH10,err_nH5_TH20,err_nH1_TH100]
    TH_const_beta=[1,2,4,5,10,20,100]
    TH_str=['02','04','05','10','20','100']
    TH=TH_const_beta[1:]
    gamma_TH_max=np.zeros(len(TH))
    err_TH_max=np.zeros(len(TH))
    for i in range(len(gamma_TH_max)):
        a,b,gamma_TH_max[i],err_TH_max[i]=gamma_averaged('Alexey-case/TH-scan/lin-n20-nH10-TH'+TH_str[i]+'/orb5_res.h5', ta, tb)
    
    gamma_const_beta=[gamma_nH100_TH1,gamma_nH50_TH2,gamma_nH25_TH4,gamma_nH20_TH5,gamma_nH0_TH10,gamma_nH5_TH20,gamma_nH1_TH100]
    
    

    fig2, ax2= subplots(figsize=(7,6))
    formatter2 = ScalarFormatter(useMathText=True)
    formatter2.set_powerlimits((-3, 3))
    ax2.yaxis.set_major_formatter(formatter2)
    ax2.errorbar(TH,gamma_TH_max,err_TH_max, marker='o', capsize=5,label=r'$n_f=10\%$')
    
    ax2.errorbar(0,gamma_nH0,err_nH0, marker='o', capsize=5,label=r'$n_f=0$', color='black')

    '''
    ax2.errorbar(100,gamma_nH1_TH100,err_nH1_TH100, marker='o', capsize=5,label=r'$n_f=1\%$')

    ax2.errorbar(20,gamma_nH5_TH20,err_nH5_TH20, marker='o', capsize=5,label=r'$n_f=5\%$')

    ax2.errorbar(5,gamma_nH20_TH5,err_nH20_TH5, marker='o', capsize=5,label=r'$n_f=20\%$', color='black')
    '''
    ax2.errorbar(TH_const_beta,gamma_const_beta,err_const_beta, marker='o', capsize=5, linestyle='--',color='r',label=r'$\beta_f=const$')
    
    #print((gamma_nH0-gamma_nH1_TH100)/gamma_nH0)
    #print((gamma_nH0-gamma_TH_max[-2])/gamma_nH0)

    ax2.grid(True)
    ax2.set_xlabel(r'$T_{EP}/T_i$', fontsize=18)
    #ax2.set_ylim(0.00035,0.0004)
    #ax2.set_xlim(-2,40)
    ax2.set_ylabel(r"$\gamma/\Omega_{ci}$", fontsize=18)
    ax2.legend(fontsize=16)
    rc('xtick', labelsize=16)
    rc('ytick', labelsize=16)
    fig2.tight_layout()
    #savefig('Pictures/gamma_Maxwellian_TH_profile.pdf')
    return


def beta_scan():
    s=120
    a,b,gamma_nH0,err_nH0=gamma_E('Alexey-case/const-beta/new/lin-n20-nH10-TH00/orb5_res.h5', ta, tb,s)
    #a,b,gamma_nH0,err_nH0=gamma_averaged('Alexey-case/lin-n20-nH10-TH00/orb5_res.h5', ta, tb)

    a,b,gamma_nH1_TH100,err_nH1_TH100=gamma_E('Alexey-case/const-beta/new/lin-n20-nH1-TH100/orb5_res.h5', ta, tb,s)

    a,b,gamma_nH5_TH20,err_nH5_TH20=gamma_E('Alexey-case/const-beta/new/lin-n20-nH5-TH20/orb5_res.h5', ta, tb,s)

    a,b,gamma_nH20_TH5,err_nH20_TH5=gamma_E('Alexey-case/const-beta/new/lin-n20-nH20-TH05/orb5_res.h5', ta, tb,s)

    a,b,gamma_nH25_TH4,err_nH25_TH4=gamma_E('Alexey-case/const-beta/new/lin-n20-nH25-TH04/orb5_res.h5', ta, tb,s)

    a,b,gamma_nH50_TH2,err_nH50_TH2=gamma_E('Alexey-case/const-beta/new/lin-n20-nH50-TH02/orb5_res.h5', ta, tb,s)

    a,b,gamma_nH100_TH1,err_nH100_TH1=gamma_E('Alexey-case/const-beta/new/lin-n20-nH100-TH01/orb5_res.h5', ta, tb,s)
    
    a,b,gamma_nH0_TH10,err_nH10_TH10=gamma_E('Alexey-case/const-beta/new/lin-n20-nH10-TH10/orb5_res.h5', ta, tb,s)
    err_const_beta=[err_nH100_TH1,err_nH50_TH2,err_nH25_TH4,err_nH20_TH5,err_nH10_TH10,err_nH5_TH20,err_nH1_TH100]
    TH_const_beta=[1,2,4,5,10,20,100]
    TH_str=['02','04','05','10','20','100']
    TH=TH_const_beta[1:]
    gamma_TH_max=np.zeros(len(TH))
    err_TH_max=np.zeros(len(TH))
    for i in range(len(gamma_TH_max)):
        a,b,gamma_TH_max[i],err_TH_max[i]=gamma_E('Alexey-case/TH-scan/lin-n20-nH10-TH'+TH_str[i]+'/orb5_res.h5', ta, tb,s)
    
    gamma_const_beta=[gamma_nH100_TH1,gamma_nH50_TH2,gamma_nH25_TH4,gamma_nH20_TH5,gamma_nH0_TH10,gamma_nH5_TH20,gamma_nH1_TH100]
    
    print((gamma_nH0-gamma_nH1_TH100)/gamma_nH0*100)
    print((gamma_nH0-gamma_TH_max[-1])/gamma_nH0*100)

    fig2, ax2= subplots(figsize=(7,6))
    formatter2 = ScalarFormatter(useMathText=True)
    formatter2.set_powerlimits((-3, 3))
    ax2.yaxis.set_major_formatter(formatter2)
    ax2.errorbar(TH,gamma_TH_max,err_TH_max, marker='o', capsize=5,label=r'$n_f=10\%$')
    
    ax2.errorbar(0,gamma_nH0,err_nH0, marker='o', capsize=5,label=r'$n_f=0$', color='black')

    '''
    ax2.errorbar(100,gamma_nH1_TH100,err_nH1_TH100, marker='o', capsize=5,label=r'$n_f=1\%$')

    ax2.errorbar(20,gamma_nH5_TH20,err_nH5_TH20, marker='o', capsize=5,label=r'$n_f=5\%$')

    ax2.errorbar(5,gamma_nH20_TH5,err_nH20_TH5, marker='o', capsize=5,label=r'$n_f=20\%$', color='black')
    '''
    ax2.errorbar(TH_const_beta,gamma_const_beta,err_const_beta, marker='o', capsize=5, linestyle='--',color='r',label=r'$\beta_f=const$')
    
    #print((gamma_nH0-gamma_nH1_TH100)/gamma_nH0)
    #print((gamma_nH0-gamma_TH_max[-2])/gamma_nH0)

    ax2.grid(True)
    ax2.set_xlabel(r'$T_{EP}/T_i$', fontsize=18)
    #ax2.set_ylim(0.00035,0.0004)
    #ax2.set_xlim(-2,40)
    ax2.set_ylabel(r"$\gamma/\Omega_{ci}$", fontsize=18)
    ax2.legend(fontsize=16)
    rc('xtick', labelsize=16)
    rc('ytick', labelsize=16)
    fig2.tight_layout()
    #savefig('Pictures/gamma_Maxwellian_TH_profile.pdf')
    
    return


#beta_scan()
#ksi_scan()
#ksi_heatmap()
temp_scan()





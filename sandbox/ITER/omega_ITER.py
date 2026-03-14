import os
import re
import sys
sys.path.append('/media/test-Samsung-SSD/roma/Work/orb5_analysis/scripts/')
from omega import *



path_ES_EP_adele='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/maxwellian-EP/T_prof/ES/nH01_dt20/orb5_res.h5'
path_ES_noEP_adele='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_adiabatic/dt20_4species/orb5_res.h5'
path_ES_noEP_kinele='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/ES_kinetic/dt20_4species/orb5_res.h5'

path_EM_noEP='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/no-EP/EM_kinetic/dt20_4species/orb5_res.h5'
path_EM_EP='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/ITER/maxwellian-EP/T_prof/EM/nH01_dt20/orb5_res.h5'

 
tmin=40000
tmax=90000
tmin_EM=40000
tmax_EM=90000

w_ITG_ES_adele_EP=omega(path_ES_EP_adele, 100,tmin,tmax)
w_ITG_ES_adele_noEP=omega(path_ES_noEP_adele, 100,tmin,tmax)
w_ITG_ES_kinele_noEP=omega(path_ES_noEP_kinele, 100,tmin,tmax)
w_ITG_EM_EP=omega(path_EM_EP, 100,tmin_EM,tmax_EM)
w_ITG_EM_noEP=omega(path_EM_noEP, 100,tmin_EM,tmax_EM)

'''
w_2ITG_ES_adele_EP=omega(path_ES_EP_adele, 46)
w_2ITG_ES_adele_noEP=omega(path_ES_noEP_adele, 46)
w_2ITG_ES_kinele_noEP=omega(path_ES_noEP_kinele, 46)
w_2ITG_EM_EP=omega(path_EM_EP, 46)
w_2ITG_EM_noEP=omega(path_EM_noEP, 46)
'''
w_TEM_ES_kinele_noEP=omega(path_ES_noEP_kinele, 297,tmin_EM,tmax_EM)
w_TEM_EM_EP=omega(path_EM_EP, 297,tmin_EM,tmax_EM)
w_TEM_EM_noEP=omega(path_EM_noEP, 297,tmin_EM,tmax_EM)


#MAIN ITG___________________________________________________________________
fig,ax=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))
ax.yaxis.set_major_formatter(formatter)

ax.plot(0,w_ITG_ES_adele_noEP, marker='o',markersize=15, label=r'$n_f=0\%$ ES adiabatic')
ax.plot(1,w_ITG_ES_adele_EP, marker='s',markersize=15, label=r'$n_f=1\%$ ES adiabatic')
ax.plot(0,w_ITG_ES_kinele_noEP, marker='o',markersize=15,mfc ='w', label=r'$n_f=0\%$ ES kinetic')
ax.plot(0,w_ITG_EM_noEP, marker='o',markersize=15,mfc ='w', label=r'$n_f=0\%$ EM')
ax.plot(1,w_ITG_EM_EP, marker='s',markersize=15,mfc ='w', label=r'$n_f=1\%$ EM')
#ax.plot(0,, marker='o',capsize=5, label=r'$n_f=0\%$ ES adiabatic')
#ax.plot(0,, marker='o',capsize=5, label=r'$n_f=0\%$ ES adiabatic')


ax.grid()
ax.legend(fontsize=16)
ax.set_xlabel(r'$\tilde{n}_f, \%$', fontsize=18)
ax.set_ylabel(r"$\omega/\Omega_{ci}$", fontsize=18)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/ITER/slowingdown/growthrate/ITER_omega_ITG.pdf')
'''
#WEAK ITG__________________________________________________________________
fig,ax1=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))
ax1.yaxis.set_major_formatter(formatter)

ax1.plot(0,w_2ITG_ES_adele_noEP, marker='o',markersize=15, label=r'$n_f=0\%$ ES adiabatic')
ax1.plot(1,w_2ITG_ES_adele_EP, marker='s',markersize=15, label=r'$n_f=1\%$ ES adiabatic')
ax1.plot(0,w_2ITG_ES_kinele_noEP, marker='o',markersize=15,mfc ='w', label=r'$n_f=0\%$ ES kinetic')
ax1.plot(0,w_2ITG_EM_noEP, marker='o',markersize=15,mfc ='w', label=r'$n_f=0\%$ EM')
ax1.plot(1,w_2ITG_EM_EP, marker='s',markersize=15,mfc ='w', label=r'$n_f=1\%$ EM')

ax1.grid()
ax1.legend(fontsize=16)
ax1.set_xlabel(r'$\tilde{n}_f, \%$', fontsize=18)
ax1.set_ylabel(r"$\omega/\Omega_{ci}$", fontsize=18)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/ITER/slowingdown/growthrate/ITER_omega_ITG_harmonics.pdf')


#TEM________________________________________________________________________

'''
fig,ax2=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))
ax2.yaxis.set_major_formatter(formatter)

ax2.plot(0,w_TEM_ES_kinele_noEP, marker='o',markersize=15,mfc ='w', label=r'$n_f=0\%$ ES kinetic')
ax2.plot(0,w_TEM_EM_noEP, marker='o',markersize=15,mfc ='w', label=r'$n_f=0\%$ EM')
ax2.plot(1,w_TEM_EM_EP, marker='s',markersize=15,mfc ='w', label=r'$n_f=1\%$ EM')

ax2.grid()
ax2.legend(fontsize=16, loc=5)
ax2.set_xlabel(r'$\tilde{n}_f, \%$', fontsize=18)
ax2.set_ylabel(r"$\omega/\Omega_{ci}$", fontsize=18)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/ITER/slowingdown/growthrate/ITER_omega_ITG_harmonics.pdf')

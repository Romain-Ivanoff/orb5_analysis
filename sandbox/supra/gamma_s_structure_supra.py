#path='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/shaped/n_scan/n180_dt10_ntot7/orb5_res.h5'
#phi_s, gamma_arr=gamma_profile(path=path, tmin=20000, tmax=60000, n_boxes=4,min_pts_per_box=8, nsel_box_err=True)
#plot(phi_s, gamma_arr)

#[60,70,80,90,100,110,120,130,140,150,160,170,180,190,200]
fig,ax=subplots(figsize=(7,6))
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))
ax.yaxis.set_major_formatter(formatter)
#ax.plot(phi_s, gamma_arr)
for n in [60,80,100,120,140,160,180,190,200]:
    path='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/shaped/n_scan/n'+str(n)+'_dt10_ntot7/orb5_res.h5'
    phi_s, gamma_arr=gamma_profile(path=path, tmin=20000, tmax=60000, n_boxes=4,min_pts_per_box=8, nsel_box_err=True)
    ax.plot(phi_s, gamma_arr, label=r'$n=$'+str(n))

ax.grid()
ax.legend(fontsize=15)
ax.set_xlabel(r's', fontsize=18)
ax.set_ylabel(r"$\gamma\cdot\Omega_{ci}^{-1}$", fontsize=18)
rc('xtick', labelsize=16)
rc('ytick', labelsize=16)
ax.set_ylim(0,9.5*10**(-5))
ax.xaxis.set_major_locator(MaxNLocator(5)) 
fig.tight_layout()
#savefig('/media/test-Samsung-SSD/roma/Work/orb5_analysis/Pictures/linear_ITG/supra/gamma_scan2.pdf')

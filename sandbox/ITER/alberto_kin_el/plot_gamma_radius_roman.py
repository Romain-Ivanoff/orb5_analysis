from numpy import *
from numpy.matlib import *
from matplotlib.pyplot import *
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from scipy.signal import find_peaks
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter
import os
import re
import sys
import os
os.chdir('/media/test-Samsung-SSD/roma/Work/orb5_analysis/sandbox/ITER/alberto_kin_el/')

# Load the radial coordinate and both datasets
radius = np.load('sgrid_ad.npy')         # Shape: (385,)
data8 = np.load('fits2_ad_3.npy')          # Shape: (385, 2) → first column is what you want
data10 = np.load('fits2_fkdt10_3.npy')          # Shape: (385, 2) → first column is what you want
data13 = np.load('fits2_fkdt5_mHo2_3.npy')          # Shape: (385, 2) → first column is what you want
data7 = np.load('fits2_fkdt2p5_mH_3.npy')          # Shape: (385, 2) → first column is what you want
data6 = np.load('fits2_fkdt20_m200_3.npy')          # Shape: (385, 2) → first column is what you wan

# Extract the first column (first array) from each dataset
gamma6 = data6[:, 0]  # First column of fits2
gamma7 = data7[:, 0]  # First column of fits2
gamma8 = data8[:, 0]  # First column of fits2
gamma10 = data10[:, 0]  # First column of fits2
gamma13 = data13[:, 0]  # First column of fits2
print(gamma10[100]*10**5)
print((gamma10[100]-gamma7[100])/gamma10[100])

# Create the plot
fig,ax=subplots(figsize=(12,6))

# Plot both datasets
ax.plot(radius, gamma8*10**5, 'r-', linewidth=2, label=r'$\gamma$ (adiab. el., dt=10)')
ax.plot(radius, gamma6*10**5, 'k-.', linewidth=2, label=r'$\gamma$ (kin. el., $m_i/m_e=200$, dt=20)')
ax.plot(radius, gamma10*10**5, 'r-.', linewidth=2, label=r'$\gamma$ (kin. el., $m_i/m_e=400$, dt=10)')
ax.plot(radius, gamma13*10**5, 'b--', linewidth=2, label=r'$\gamma$ (kin. el., $m_i/m_e=m_p/2=918$, dt=5)')
ax.plot(radius, gamma7*10**5, 'm-', linewidth=2, label=r'$\gamma$ (kin. el., $m_i/m_e=m_p=1836$, dt=2.5)')

# Labels and formatting
ax.set_xlabel('s', fontsize=16)
ax.set_ylabel(r"$\gamma\cdot\Omega_{ci}^{-1}\cdot10^{-5}$", fontsize=16)
#ax.title('Growth rate, $\gamma$, at different radius', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=14)

# Adjust layout
rc('xtick', labelsize=14)
rc('ytick', labelsize=14)
fig.tight_layout()

# Save the figure (high resolution PNG)
#savefig('gamma_comparison_ab_hy.pdf')

# Display the plot



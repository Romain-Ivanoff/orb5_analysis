from h5py import *
from numpy import *
from numpy.matlib import *
from matplotlib.pyplot import *
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from scipy.signal import find_peaks
from matplotlib.ticker import ScalarFormatter
import re
import numpy as np
base_path='/media/test-Samsung-SSD/roma/Work/simulations/lin_ITG_EP/supra/shaped/n_scan/res_test/'
def extract_efield(filename):
    efields = []
    
    # regex to capture the number after "Efield ::"
    pattern = re.compile(r"Efield\s*::\s*([+-]?\d+\.\d+E[+-]?\d+)")
    
    with open(filename, "r") as f:
        for line in f:
            m = pattern.search(line)
            if m:
                efields.append(float(m.group(1)))
    
    return np.array(efields)


# --- use it on your two files ---
low = extract_efield(base_path+"output_low_res")
high = extract_efield(base_path+"output_high res")


plot(log(low[900:]))
plot(log(high[900:]))

def slope(arr):
    x = np.arange(len(arr))
    m, _ = np.polyfit(x, arr, 1)
    return m

low  = extract_efield(base_path+"output_low_res")
high = extract_efield(base_path+"output_high res")


a=slope(log(low[900:]))
b=slope(log(high[900:]))
print("low slope =", a)
print("high slope =", b)
print((b-a)/b)
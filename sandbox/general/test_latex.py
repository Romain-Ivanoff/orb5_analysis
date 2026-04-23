import matplotlib
matplotlib.use("pgf") # Must be called before importing pyplot
from numpy import *
from matplotlib.pyplot import *

# Configure to output raw LaTeX
rcParams.update({
    "font.family": "serif",
    "text.usetex": True,
    "pgf.rcfonts": False,   # Crucial: Let the main LaTeX document handle the fonts!
    "font.size": 10,        
    "axes.labelsize": 10,
    "legend.fontsize": 9,
})

# Generate test data
x = linspace(0, 10, 100)
y = sin(x) * exp(-0.2 * x)

# Sized for half-page column
fig, ax = subplots(figsize=(3.5, 3.0))

ax.plot(x, y, color='black', label=r'$y = \sin(x) e^{-0.2x}$')

ax.set_xlabel(r'Time $t$ (s)')
ax.set_ylabel(r'Amplitude $\mathcal{A}$')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)

# Save as .pgf instead of .pdf
#savefig('paper_ready_plot.pgf', bbox_inches='tight')

print("Success: paper_ready_plot.pgf has been generated!")

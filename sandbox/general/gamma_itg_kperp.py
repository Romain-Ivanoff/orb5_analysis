import numpy as np
import matplotlib.pyplot as plt
from scipy.special import wofz, iv
from scipy.optimize import root
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

# ----------------------------
# Plasma dispersion functions
# ----------------------------

def Z(z):
    return 1j*np.sqrt(np.pi)*wofz(z)

def W(z):
    zeta = z/np.sqrt(2)
    return 1 + zeta*Z(zeta)

# ----------------------------
# FLR terms
# ----------------------------

def Lambda(p, xi):
    return iv(p, xi)*np.exp(-xi)

# ----------------------------
# Dispersion relation
# ----------------------------

def dispersion(omega, kpar, kperp, params):

    tau = params["tau"]
    eta = params["eta_i"]

    if abs(omega) < 1e-10:
        omega = 1e-10 + 1e-10j

    xi = kperp**2
    z = omega/kpar

    Wz = W(z)

    L0 = Lambda(0, xi)
    L1 = Lambda(1, xi)

    term1 = 1/tau + 1
    term2 = (1 + kperp/omega*(1 - eta/2))*(Wz - 1)*L0
    term3 = (kperp/omega)*eta*(z**2/2*Wz*L0 + (Wz-1)*kperp**2*(L1-L0))

    return omega*(term1 + term2 + term3)

# ----------------------------
# Root solver
# ----------------------------

def solve_dispersion(kpar, kperp, params, guess):

    def F(x):
        omega = x[0] + 1j*x[1]
        D = dispersion(omega, kpar, kperp, params)

        if np.isnan(D) or np.isinf(D):
            return [1e6,1e6]

        return [D.real, D.imag]

    sol = root(F, guess, method='hybr')

    if not sol.success:
        return np.nan + 1j*np.nan

    return sol.x[0] + 1j*sol.x[1]

# ----------------------------
# Parameters
# ----------------------------

params = {
    "tau":1.0,
    "eta_i":13.2
}

kperp_vals = np.linspace(0.01,1.5,70)
kpar_vals  = np.linspace(0.01,1.5,30)

gamma_map = np.full((len(kpar_vals),len(kperp_vals)),np.nan)

gamma_kperp = np.zeros(len(kperp_vals))
omega_kperp = np.zeros(len(kperp_vals))
kpar_best   = np.zeros(len(kperp_vals))

global_guess = [0.02,0.3]

# ----------------------------
# Main scan
# ----------------------------

for j,kperp in enumerate(kperp_vals):

    guess = global_guess
    gamma_local = np.full(len(kpar_vals),np.nan)
    omega_local = np.full(len(kpar_vals),np.nan)

    for i,kpar in enumerate(kpar_vals):

        w = solve_dispersion(kpar,kperp,params,guess)

        if not np.isnan(w):

            gamma = np.imag(w)
            omega = np.real(w)

            gamma_map[i,j] = gamma
            gamma_local[i] = gamma
            omega_local[i] = omega

            guess = [omega,gamma]

    # keep only unstable solutions
    gamma_local[gamma_local < 0] = np.nan

    if np.all(np.isnan(gamma_local)):
        continue

    idx = np.nanargmax(gamma_local)

    gamma_kperp[j] = gamma_local[idx]
    omega_kperp[j] = omega_local[idx]
    kpar_best[j]   = kpar_vals[idx]

    global_guess = [omega_local[idx],gamma_local[idx]]

# ----------------------------
# global maximum
# ----------------------------

imax = np.nanargmax(gamma_kperp)

print("Most unstable mode")
print("k_perp =",kperp_vals[imax])
print("k_par  =",kpar_best[imax])
print("gamma  =",gamma_kperp[imax])

# ----------------------------
# instability map
# ----------------------------

plt.figure(figsize=(6,5))

plt.contourf(kperp_vals,kpar_vals,gamma_map,50)
plt.colorbar(label="growth rate")

plt.scatter(kperp_vals[imax],kpar_best[imax],color="red")

plt.xlabel(r"$k_\perp \rho_i$")
plt.ylabel(r"$k_\parallel$")
plt.title("ITG growth rate map")

plt.tight_layout()
plt.show()

# ----------------------------
# gamma(k_perp)
# ----------------------------

plt.figure(figsize=(6,4))

plt.plot(kperp_vals,gamma_kperp,linewidth=2)

plt.xlabel(r"$k_\perp \rho_i$")
plt.ylabel(r"$\gamma$")
plt.title(r"Maximum growth rate $\gamma(k_\perp)$")

plt.tight_layout()
plt.show()

# ----------------------------
# k_par(k_perp)
# ----------------------------

plt.figure(figsize=(6,4))

plt.plot(kperp_vals,kpar_best,linewidth=2)

plt.xlabel(r"$k_\perp \rho_i$")
plt.ylabel(r"$k_\parallel$")
plt.title(r"Most unstable $k_\parallel(k_\perp)$")

plt.tight_layout()
plt.show()

# stack columns: kperp, gamma, kpar
output = np.column_stack((kperp_vals, gamma_kperp, kpar_best))

np.savetxt("itg_scan_eta_13.2.txt",
           output,
           header="kperp   gamma   kpar",
           fmt="%.6e")
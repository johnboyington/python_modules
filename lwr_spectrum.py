import numpy as np
import matplotlib.pyplot as plt
from scipy import constants
from scipy.integrate import quad
from scipy.optimize import minimize
from spectrum import Spectrum  # located in my python_modules repo: https://github.com/johnboyington/python_modules


# Boltzmann constant in eV/K
k = constants.value('Boltzmann constant in eV/K')




class FluxTypical(Spectrum):
    """
    This class evaluate neutron flux at energy e. 
    At thermal energy range (e < 1eV), the flux is approximated by Maxwellian 
    distribution (D&H book Eq.(9-6)). 
    At fast energy range (0.1MeV < e < 20MeV), the flux is approximated by U-235 
    chi-spectrum (D&H book Eq.(2-112)).
    At epithermal energies (1eV < e < 0.1MeV), flux = 1/e
    
    
    r : thermal-to-fast flux ratio
    """
    def __init__(self, bins, s=1, r=2, thermal_t=600.0):
        self.bins = bins
        self.scaling = s
        self.e2 = 1e6
        self.thermal_t = thermal_t

        # Maxwellian distribution, Eq.(9-6)
        self.m = lambda x: x ** 0.5 * np.exp(-x / (k * self.thermal_t))

        # U235 chi distribution, Eq.(2-112)
        self.chi = lambda x: np.exp(-1.036e-6 * x) * np.sinh((2.29e-6 * x) ** 0.5)

        # Middle energy range
        self.f = lambda x: 1 / x
        self.r = 0
        E = np.logspace(-5, 1, 1000)
        R = np.array([self.balance(e) for e in E])
        self.e1 = np.interp(r, R, E)
        self.r = r
        self.c1 = 1.0
        self.c2 = self.m(self.e1) / self.f(self.e1)
        self.c3 = self.c2 * self.f(self.e2) / self.chi(self.e2)
        vals = self.make_discrete(self.bins, self.scaling)
        Spectrum.__init__(self, self.bins, vals, False, dfde=True)

    def balance(self, x):
        A = quad(self.m, 0, x)[0]
        B = self.m(x) / self.f(x) * quad(self.f, x, self.e2)[0]
        C = self.m(x) / self.f(x) * self.f(self.e2) / self.chi(self.e2) * quad(self.chi, self.e2, 2e7)[0]
        Q = A / (B + C) - self.r
        return abs(Q)

    def compute_flux(self, e):
        """
        Evaluate flux at Energy e.
        e : neutron energy in eV
        """
        # thermal
        if e <= self.e1:
            return self.c1 * self.m(e)
        # epithermal
        elif self.e1 < e <= self.e2:
            return self.c2 / e
        elif e >= self.e2:
            return self.c3 * self.chi(e)

    def make_discrete(self, bins, scaling=1):
        '''
        Makes discrete energy groups from continuous function above.
        '''
        bin_values = []
        for i in range(len(bins) - 1):
            area, err = quad(self.compute_flux, bins[i], bins[i+1])
            height = area / (bins[i+1] - bins[i])
            bin_values.append(height * scaling)
        return bin_values


if __name__ == '__main__':
    # ratio of thermal flux to fast flux = 1e-5
    # neutron temperature = 600K
    e = np.logspace(-8.5, 1.1, 100) * 10**6
    f = FluxTypical(e, 1, 1./7., 600.0)
    plt.plot(f.step_x, f.step_y)
    plt.xscale('log')
    plt.yscale('log')
    plt.show()

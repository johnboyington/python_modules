import numpy as np
import matplotlib.pyplot as plt
from spectrum import Spectrum  # located in my python_modules repo: https://github.com/johnboyington/python_modules


class FluxNEBP(Spectrum):
    """
    This class contains information on the nebp obtained from an mcnp analysis
    of the ksu triga mark II north east beam port.

    Input reactor power in W(th)
    """

    def __init__(self, P):

        self.power = P
        data = self.get_data()
        S = self.calc_scaling_factor()
        bins = data[:, 0]
        vals = data[:, 1][1:]
        Spectrum.__init__(self, bins, vals, False, S)

    def get_data(self):
        '''Loads in neutron flux data from a text file'''
        data = np.loadtxt('/home/john/workspace/python_modules/nebp_data.txt')
        return data

    def calc_scaling_factor(self):
        '''Given input power level, normalizes the flux values to reactor power'''
        tally_area = tally_area = np.pi * (1.27 ** 2)
        C = 2.54 / (200 * 1.60218e-13 * tally_area)
        return C * self.power


if __name__ == '__main__':
    f = FluxNEBP(250)
    new_bins = np.logspace(-11, 2, 100)
    f.change_bins(new_bins)
    plt.plot(f.step_x, f.step_y)
    plt.xscale('log')
    plt.yscale('log')
    plt.show()

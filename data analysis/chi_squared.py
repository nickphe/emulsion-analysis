import numpy as np

def reduced_chi_squared(observed, expected, sigma, dof):
    chi_2 = np.sum(np.square(observed - expected) / np.square(sigma))
    rchi_2 = chi_2 / dof
    return rchi_2
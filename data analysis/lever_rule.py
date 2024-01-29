import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

from chi_squared import reduced_chi_squared

lin_model = lambda x, m, b: m * x + b

class LeverRule:
    def __init__(self,conc, vf, vf_uncertainty):
        
        popt, pcov = curve_fit(lin_model,
                               conc, 
                               vf, 
                               sigma = vf_uncertainty, 
                               absolute_sigma = True)
        m = popt[0]
        b =  popt[1]
        self.m = m
        self.b = b
        sigma_m = np.sqrt(np.diag(pcov)[0])
        sigma_b = np.sqrt(np.diag(pcov)[1])
        self.sigma_m = sigma_m
        self.sigma_b = sigma_b
        self.ns_den = (1-b)/m
        self.ns_dil = (-b)/m
        self.ns_den_uncertainty = np.sqrt( np.square(sigma_b/m) + (np.square(1-b)*np.square(sigma_m)) / (m ** 4) )
        self.ns_dil_uncertainty = np.sqrt( np.square(sigma_b/m) + (np.square(b) * np.square(sigma_m)) / (m ** 4) )
        
        rchi_2 = reduced_chi_squared(observed = np.array(vf_list), 
                                         expected = lin_model(np.array(conc_list),m,b), 
                                         sigma = np.array(vf_u_list), 
                                         dof = (len(vf_list) - 3))
        self.lr_rchi_2 = rchi_2
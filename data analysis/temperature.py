import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scienceplots

import re
import os

import settings
settings.init()

from output import create_directory
from capillary import Capillary
from scipy.optimize import curve_fit
from get_cap_number import get_cap_number
from chi_squared import reduced_chi_squared
from mode import FWHM_uncertainty
from rich.console import Console
from linear_odr import linear_odr, lin_model_odr
console = Console()



class Temperature:
    def __init__(self, name: str, value: float, associated_capillaries):
        
        self.name = name
        self.value = value
        self.capillary_names = associated_capillaries
        self.capillaries = []
        # list(obj): list of capillary objects
        
    # initiate directory that will hold temperature data
        self.folder_path = os.path.join(settings.output_path, self.name)
        create_directory(self.folder_path)
    
    # create list of capillaries associated with temperature, excluding capillaries we would like to exclude from the experiment
        for cap_name in self.capillary_names:
            if get_cap_number(cap_name) in settings.considered_capillaries:
                cap = Capillary(cap_name, self.name)
                self.capillaries.append(cap)
            else:
                console.print(f"[yellow] Skipped[/yellow]: [cyan]{cap_name}[/cyan]")
    # create lever rules
        try:
        # create lever rule dataset  
            lin_model = lambda x, m, b: m * x + b
            vf_list = []
            vf_std_list = []
            conc_list = []
            conc_u_list = []
            num_list = []
            vf_u_list = []
            
            f = open(f"{self.folder_path}/lever_rule_data.txt", "w")
            f.write(f"T = {self.value}˚C lever-rule data \n")
        # create lever rule dataset 
        
            method_vf = settings.method_vf
            
            for i, capillary in enumerate(self.capillaries):
                vf = capillary.stats[f"{method_vf} fit vf"]
                vf_list.append(vf)
                vf_std = np.std(capillary.fit_vf)
                vf_std_list.append(vf_std)
                vf_u = capillary.stats["fit vf FWHM"] #/ np.sqrt(len(capillary.fit_vf)) # should we include / sqrt(N)??
                vf_u_list.append(vf_u)
                conc = capillary.concentration
                conc_list.append(conc)
                conc_u = capillary.concentration * 0.10  # temporary 3% pipetting uncertainty
                conc_u_list.append(conc_u)
                num = capillary.cap_number
                num_list.append(num)
                f.write(f"capillary name: {capillary.name}, capillary concentration: {conc}; vf = {vf}, FWHM = {capillary.stats['fit vf FWHM']}, std = {vf_std}.\n")
            
            conc_ref = pd.DataFrame({"Capillary #": num_list, "Concentration (uM)": conc_list})
            conc_ref.to_csv(f"{self.folder_path}/capillary-concentration_reference.csv")
            
            # #force a 0,0 point in concentration / vf
            # conc_list.append(0.5)
            # conc_u_list.append(0.5)
            # vf_list.append(0)
            # vf_u_list.append(0.005)
            
        # fit line                 function,      x,        y
            # popt, pcov = curve_fit(lin_model, conc_list, vf_list, 
            #                        sigma = vf_u_list, absolute_sigma = True) # weights fits based on uncertainty
            popt, pcov, psd = linear_odr(conc_list, vf_list, conc_u_list, vf_u_list, 0, 0) # use orthogonal distance regression to fit line
            #print(popt, pcov, psd)
            m = popt[0]
            #b = -1.0 * popt[1] ** 2 #because of current b^2 to ensure negative intercept
            b = popt[1]
            sigma_m = psd[0]
            sigma_b = psd[1]
            #sigma_b = np.sqrt((-2 * b * psd[1] ) ** 2) #because of current b^2 to ensure negative intercept
            ns_den = (1-b)/m
            ns_dil = (-b)/m
            ns_den_uncertainty = np.sqrt( np.square(sigma_b/m) + (np.square(1-b)*np.square(sigma_m)) / (m ** 4) )
            ns_dil_uncertainty = np.sqrt( np.square(sigma_b/m) + (np.square(b) * np.square(sigma_m)) / (m ** 4) )
            #print(ns_den_uncertainty, ns_dil_uncertainty)
            self.ns_den = ns_den
            self.ns_dil = ns_dil
            self.ns_den_uncertainty = ns_den_uncertainty
            self.ns_dil_uncertainty = ns_dil_uncertainty
            rchi_2 = reduced_chi_squared(observed = np.array(vf_list), 
                                         expected = lin_model(np.array(conc_list),m,b), 
                                         sigma = np.array(vf_u_list), 
                                         dof = (len(vf_list) - 3))
            self.lr_rchi_2 = rchi_2
       
        # save fit data
            f.write(f"\nFit data \n")
            f.write(f"vf data taken from {method_vf} of vf distribution.\n")
            f.write(f"slope = {m}, y-intercept = {b}")
            f.write(f"[NS]_den = {ns_den} +/- {ns_den_uncertainty}, [NS]_dil = {ns_dil} +/- {ns_dil_uncertainty}\n")
            f.write(f"Fit reduced chi^2: {self.lr_rchi_2}")
            f.close()

        # create individual lever rule plot
            with plt.style.context(["science","nature"]):
                fig, ax = plt.subplots(dpi = 500)
                ax.errorbar(conc_list, vf_list, xerr = conc_u_list, yerr = vf_u_list, linestyle = "", marker = "o", label = f"T = {self.value} $^\\circ$C", capsize = 3)
                x = np.linspace(0, np.max(np.array([conc_list])) + 30, 100)
                ax.plot(x, lin_model(x, m, b), linestyle = "-", label = "[NS]$_{\\mathrm{den}}=$" + 
                        f"{round(ns_den,2)}$\\pm${round(ns_den_uncertainty,2)}($\\mu$M)\n"+ "[NS]$_{\\mathrm{dil}}=$" + f"{round(ns_dil,2)}$\\pm${round(ns_dil_uncertainty,2)}($\\mu$M)")
                ax.legend()
                ax.set_xlabel(settings.plot_settings["lr x label"])
                ax.set_ylabel(settings.plot_settings["lr y label"])
                plt.savefig(f"{self.folder_path}/lever_rule_plot_T{self.value}C.png")
                
        except RuntimeError as re:
            console.print(f"[bold red]Failed to create lever rule for T = {self.value}", re)
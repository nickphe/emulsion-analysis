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

from rich.console import Console
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
                vf_u = vf_std #/ np.sqrt(len(capillary.fit_vf)) # should we include / sqrt(N)??
                vf_u_list.append(vf_u)
                conc = capillary.concentration
                conc_list.append(conc)
                f.write(f"capillary name: {capillary.name}, capillary concentration: {conc}; vf = {vf}, std = {vf_std}.\n")
        
        # fit line                 function,      x,        y
            popt, pcov = curve_fit(lin_model, conc_list, vf_list, 
                                   sigma = vf_u_list, absolute_sigma = True) # weights fits based on uncertainty
            m = popt[0]
            b = popt[1]
            sigma_m = np.sqrt(np.diag(pcov)[0])
            sigma_b = np.sqrt(np.diag(pcov)[1])
            ns_den = (1-b)/m
            ns_dil = (-b)/m
            ns_den_uncertainty = np.sqrt( np.square(sigma_b/m) + (np.square(1-b)*np.square(sigma_m)) / (m ** 4) )
            ns_dil_uncertainty = np.sqrt( np.square(sigma_b/m) + (np.square(b) * np.square(sigma_m)) / (m ** 4) )
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
            f.write(f"[NS]_den = {ns_den}, [NS]_dil = {ns_dil}\n")
            f.write(f"Fit reduced chi^2: {self.lr_rchi_2}")
            f.close()

        # create individual lever rule plot
            with plt.style.context(["science","nature"]):
                fig, ax = plt.subplots(dpi = 500)
                ax.errorbar(conc_list, vf_list, yerr = vf_u_list, linestyle = "", marker = "o", label = f"T = {self.value} $^\\circ$C", capsize = 3)
                x = np.linspace(0, np.max(np.array([conc_list])) + 30, 100)
                ax.plot(x, lin_model(x, m, b), linestyle = "-", label = "[NS]$_{\\mathrm{den}}=$" + 
                        f"{round(ns_den,2)} ($\\mu$M)\n"+ "[NS]$_{\\mathrm{dil}}=$" + f"{round(ns_dil,2)} ($\\mu$M)")
                ax.legend()
                ax.set_xlabel(settings.plot_settings["lr x label"])
                ax.set_ylabel(settings.plot_settings["lr y label"])
                plt.savefig(f"{self.folder_path}/lever_rule_plot_T{self.value}C.png")
                
        except:
            console.print(f"[bold red]Failed to create lever rule for T = {self.value}")
import numpy as np
import matplotlib.pyplot as plt
import scienceplots
import pandas as pd

import settings
settings.init()

def save_phase_diagram(list_of_temperatures, melting_points, conc_list):
    
    f = open(f"{settings.output_path}/phase_diagram_info.txt", "w")
    
    ns_dil_list = []
    ns_den_list = []
    ns_den_uncertainty_list = []
    ns_dil_uncertainty_list = []
    temp_list = []
    
    for temp in list_of_temperatures:
        temp_list.append(temp.value)
        ns_den_list.append(temp.ns_den)
        ns_dil_list.append(temp.ns_dil)
        ns_den_uncertainty_list.append(temp.ns_den_uncertainty)
        ns_dil_uncertainty_list.append(temp.ns_dil_uncertainty)
# save csv files of phase diagram data
    dt = pd.DataFrame({
        "temp" : temp_list, 
        "ns_den" : ns_den_list, 
        "ns_den_uncertainty" : ns_den_uncertainty_list, 
        "ns_dil_uncertainty" : ns_dil_uncertainty_list,
        "ns_dil" : ns_dil_list})
    dt.to_csv(f"{settings.output_path}/phase_diagram_dendil_data.csv")
    
    mp = pd.DataFrame({"conc": conc_list, "melting point": melting_points})
    mp.to_csv(f"{settings.output_path}/phase_diagram_melting_data.csv")
    
    with plt.style.context(["science","nature"]):
        
        fig, ax = plt.subplots(dpi = 1000)
        ax.errorbar(ns_den_list, temp_list, yerr = np.ones(len(ns_den_list))*0.5, xerr = ns_den_uncertainty_list, linestyle = "", marker = "o", capsize = 3)
        ax.errorbar(ns_dil_list, temp_list, yerr = np.ones(len(ns_den_list))*0.5, xerr = ns_dil_uncertainty_list, linestyle = "", marker = "o", capsize = 3)
        ax.plot(conc_list, melting_points, linestyle = "", marker = "o")
        ax.set_xlabel(settings.plot_settings["pd x label"])
        ax.set_ylabel(settings.plot_settings["pd y label"])
        plt.savefig(f"{settings.output_path}/phase_diagram.png")
        
        
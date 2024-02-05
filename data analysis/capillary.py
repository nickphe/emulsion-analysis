import numpy as np
import pandas as pd
from skimage.io import imread
import os
import matplotlib.pyplot as plt

import settings
settings.init()

from mode import mode, FWHM
bin_count = settings.mode_bins

from rich.console import Console
console = Console()

from get_cap_number import get_cap_number
from parse_parent import extract_numeric_part

from filter_data import filter_data
from output import create_directory

from math import floor

class Capillary:
    def __init__(self, capillary_name, temperature_name: str):
     
    # define attributes of capillary
        self.name = capillary_name
        self.temp_name = temperature_name
        self.temp_value = extract_numeric_part(temperature_name)
        self.cap_number = get_cap_number(capillary_name)
        self.concentration = settings.conc_dict[self.cap_number]
        #console.log(f"{self.name}", self.cap_number, self.concentration, sep = "\t")
        
    # initiate directory that will hold this capillaries data
        self.folder_path = os.path.join(f"{settings.output_path}/{self.temp_name}", self.name)
        create_directory(self.folder_path)
        
    # import ilastik feature table and object identites
        self.feature_table_path = f"{settings.parent_folder}/{self.temp_name}/ilastik/{self.name}{settings.ft_file_pattern}.csv"
        self.object_identities_path = f"{settings.parent_folder}/{self.temp_name}/ilastik/{self.name}{settings.oi_file_pattern}.tif"
        self.feature_table = pd.read_csv(self.feature_table_path)
        self.object_identities = imread(self.object_identities_path)
   
    # import analysis log associated with capillary
        analysis_log_path = f"{settings.parent_folder}/{self.temp_name}/{self.temp_name} analysis logs/{self.name}_analysis_log.csv"
        self.raw_data = pd.read_csv(analysis_log_path)
        rd = self.raw_data
    
    # filter analysis log
        self.filtered_data = filter_data(self.raw_data)
        fd = self.filtered_data
        
    # save filtered analysis log to capillary folder
        f = open(f"{self.folder_path}/filter_params.txt", "w")
        f.write(f"Filter criteria: \n {settings.filter_criteria}")
        f.close()
        rd.to_csv(f"{self.folder_path}/raw_fit_data.csv") 
        fd.to_csv(f"{self.folder_path}/filtered_fit_data.csv")
        
        f = open(f"{self.folder_path}/information.txt", "w")
        f.write(f"Name: {self.name}\n Concentration: {self.concentration} uM \n Temperature: {self.temp_value} C")
        f.close()
    
    
    # arrays from filtered data table
        self.fit_vf = fd["fit params vf"].to_numpy()
        self.fit_rmse = fd["RMSE"].to_numpy()
        self.fit_rden = fd["fit rDen"].to_numpy()
        self.fit_rden_u = fd["fit rDen uncertainty"].to_numpy()
        self.fit_rdil = fd["fit rDil"].to_numpy()
        self.fit_rdil_u = fd["fit rDil uncertainty"].to_numpy()
        self.fit_a = fd["fit a"].to_numpy()
        self.fit_b = fd["fit b"].to_numpy()
        self.fit_c = fd["fit c"].to_numpy()
        self.fit_xcen = fd["fit xCen"].to_numpy()
        self.fit_ycen = fd["fit yCen"].to_numpy()
        
    # droplet identities corresponding to fits
        # # self.drop_identities = {}
        # # for i, y in enumerate(self.fit_ycen):
        # #     for x in self.fit_xcen:
        # #         self.drop_identities[f"{i}"] = self.object_identities[floor(y),floor(x)]
                
        # obj_id_df = pd.DataFrame(self.drop_identities)
        # obj_id_df.to_csv(f"{self.folder_path}/filtered_identity_index.csv")
        
        self.voronoi_rdil = fd["voronoi rDil"].to_numpy()
        self.signal_rden = fd["signal rDen"].to_numpy()
        
        NBINS_fwhm = 70
        vf_count, vf_bins = np.histogram(self.fit_vf, NBINS_fwhm)
        vf_FWHM = FWHM(np.argmax(vf_count), vf_bins, vf_count)
        
    # stats from filtered data table
        self.stats = {
            "mean fit vf" : np.mean(self.fit_vf),
            "median fit vf" : np.median(self.fit_vf),
            "mode fit vf": mode(self.fit_vf, bin_count),
            "mean fit rden" : np.mean(self.fit_rden),
            "median fit rden" : np.median(self.fit_rden),
            "mode fit rden": mode(self.fit_rden, bin_count),
            "mean fit rdil" : np.mean(self.fit_rdil),
            "median fit rdil" : np.median(self.fit_rdil),
            "mode fit rdil": mode(self.fit_rdil, bin_count),
            "fit vf FWHM": vf_FWHM
        }
        
        columns = list(self.stats.keys())
        values = [list(self.stats.values())]
        stats_table = pd.DataFrame(values, columns=columns)
        stats_table.to_csv(f"{self.folder_path}/capillary_stats.csv")
        
        # Generate capillary histograms - rd: raw data, fd: filtered data
        NBINS = 200
      
        rd_vf = rd[np.isfinite(rd["fit params vf"])]["fit params vf"].to_numpy()
        fd_vf = fd[np.isfinite(fd["fit params vf"])]["fit params vf"].to_numpy()
        bins_vf = np.histogram(np.hstack((rd_vf,fd_vf)), bins = NBINS)[1] #get the bin edges
      
        with plt.style.context(["science","nature"]):
            fig, ax = plt.subplots(dpi = 500)
            ax.hist(rd_vf, bins_vf, fill = False, histtype = "step", label = "Raw Data", color = "coral", alpha = 0.7)
            ax.hist(fd_vf, bins_vf, fill = False, histtype = "step", label = "Filtered Data", color = "lightseagreen", alpha = 0.7)
            ax.vlines(self.stats["mode fit vf"], 0, 20, label = "Mode", color = "firebrick", linestyle = "-")
            ax.vlines(self.stats["mean fit vf"], 0, 20,label = "Mean", color = "darkslategray", linestyle = "--")
            ax.vlines(self.stats["median fit vf"], 0, 20,  label = "Median", color = "navy", linestyle = "-.")
            ax.legend()
            ax.set_xlabel("$\\phi$")
            ax.set_ylabel("Droplets")
            ax.set_xlim([0,1])
            plt.savefig(f"{self.folder_path}/vf_histogram.png")
            plt.close()
        
            fig, ax = plt.subplots(dpi = 500)
            count, bins = np.histogram(rd_vf, floor(len(rd_vf)/2))
            ax.stairs(count, bins, fill = False)
            ax.vlines(self.stats["mode fit vf"], 0, 20, label = "Mode", color = "firebrick", linestyle = "-")
            ax.vlines(self.stats["mean fit vf"], 0, 20,label = "Mean", color = "darkslategray", linestyle = "--")
            ax.vlines(self.stats["median fit vf"], 0, 20,  label = "Median", color = "navy", linestyle = "-.")
            ax.legend()
            ax.set_xlabel("$\\phi$")
            ax.set_ylabel("Droplets")
            plt.savefig(f"{self.folder_path}/raw_data_vf_histogram.png")
            plt.close()
            
            fig, ax = plt.subplots(dpi = 500)
            count, bins = np.histogram(fd_vf, floor(len(rd_vf)/2))
            ax.stairs(count, bins, fill = False)
            ax.vlines(self.stats["mode fit vf"], 0, 20, label = "Mode", color = "firebrick", linestyle = "-")
            ax.vlines(self.stats["mean fit vf"], 0, 20,label = "Mean", color = "darkslategray", linestyle = "--")
            ax.vlines(self.stats["median fit vf"], 0, 20,  label = "Median", color = "navy", linestyle = "-.")
            ax.legend()
            ax.set_xlabel("$\\phi$")
            ax.set_ylabel("Droplets")
            plt.savefig(f"{self.folder_path}/filtered_data_vf_histogram.png")
            plt.close()
        
        
        
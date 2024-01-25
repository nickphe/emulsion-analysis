import numpy as np
import pandas as pd
from skimage.io import imread
import os

import settings
settings.init()

from mode import mode
bin_count = settings.mode_bins

from rich.console import Console
console = Console()

from get_cap_number import get_cap_number
from parse_parent import extract_numeric_part

from filter_data import filter_data
from output import create_directory

class Capillary:
    def __init__(self, capillary_name, temperature_name: str):
     
    # define attributes of capillary
        self.name = capillary_name
        self.temp_name = temperature_name
        self.temp_value = extract_numeric_part(temperature_name)
        self.cap_number = get_cap_number(capillary_name)
        self.concentration = settings.conc_dict[self.cap_number]
        console.log(f"{self.name}", self.cap_number, self.concentration, sep = "\t")
        
    # initiate directory that will hold this capillaries data
        self.folder_path = os.path.join(f"{settings.output_path}/{self.temp_name}", self.name)
        create_directory(self.folder_path)
        
    # import ilastik feature table and object identites
        self.feature_table_path = f"{settings.parent_folder}/{self.temp_name}/ilastik/{self.name}_table.csv"
        self.object_identities_path = f"{settings.parent_folder}/{self.temp_name}/ilastik/{self.name}_Object Identities.tif"
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
        
        self.voronoi_rdil = fd["voronoi rDil"].to_numpy()
        self.signal_rden = fd["signal rDen"].to_numpy()
        
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
            "mode fit rdil": mode(self.fit_rdil, bin_count)
        }
        
        columns = list(self.stats.keys())
        values = [list(self.stats.values())]
        stats_table = pd.DataFrame(values, columns=columns)
        stats_table.to_csv(f"{self.folder_path}/capillary_stats.csv")
        
        
        
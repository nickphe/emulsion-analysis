import os

def init():

    global parent_folder
    parent_folder = "/Users/nanostars/Desktop/a3a4/Levers"

    global output_path
    output_path = "/Users/nanostars/Desktop/a3a4/analysis output"
    
    global ft_file_pattern
    ft_file_pattern = "_table"
    
    global oi_file_pattern
    oi_file_pattern = "_Object Identities_{slice_index}"
    
    global method_vf
    method_vf = "mode"
    
    global conc_dict
              #cap : #concentration
    conc_dict = {1 : 102,
                 2 : 66.0,
                 3 : 8.3,
                 4 : 48.4, 
                 5 : 12.8, 
                 6 : 73.4, 
                 7 : 26.9, 
                 8 : 115.8, 
                 9 : 56.9}
                 #10 : 32.0}
    
    global melting_points
                    #cap  :  #melting point (˚C)
    melting_points =   {
                        1 : 37.75,
                        2 : 37.75,
                        3 : 36.75,
                        4 : 38.4, 
                        5 : 37.35, 
                        6 : 37.75, 
                        7 : 37.75, 
                        8 : 36, 
                        9 : 37.75}
    
    global mode_bins
    mode_bins = 100
   
    global filter_criteria
    filter_criteria = {"min vf" : 0,
                       "max vf": 1,
                       "max RMSE": 90}
    
    global plot_settings
    plot_settings = {
        "pd x label": "$\\alpha_{\\langle 3.5 \\rangle}$",
        "pd y label": "T ($^\\circ$C)",
        "lr x label": "$\\alpha_{\\langle 3.5 \\rangle}$",
        "lr y label": "$\\phi_{\\mathrm{den}}$", 
    }
    
import os

def init():
    global parent_folder
    parent_folder = "/Users/nanostars/Desktop/2024 01 19/Levers"

    global output_path
    output_path = os.path.join(parent_folder, "analysis output")
    
    global conc_dict
              #cap : #concentration
    conc_dict = {1 : 13,
                 2 : 47.4,
                 3 : 92.6,
                 4 : 6.0, 
                 5 : 37.9, 
                 6 : 115.8, 
                 7 : 30.4, 
                 8 : 74.1, 
                 9 : 24.3, 
                 10 : 59.3}
    
    global mode_bins
    mode_bins = 100
   
    global filter_criteria
    filter_criteria = {"min vf" : 0,
                       "max vf": 1,
                       "max RMSE": 90}
    
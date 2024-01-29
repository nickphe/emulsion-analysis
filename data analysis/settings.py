import os
import toml
from rich.console import Console
console = Console()
import sys

config = toml.load("/Users/nickphelps/Desktop/emulsion-analysis-main/settings/analysis_config.toml")

def dict_from_lists(keys, values):
    result_dict = dict.fromkeys(keys)
    for key, v in zip(result_dict.keys(), values):
        result_dict[key] = v
    return result_dict

def init():

    global parent_folder
    parent_folder = config['parent_folder']

    global output_path
    output_path = config['output_path']
    
    global ft_file_pattern
    ft_file_pattern = config['ft_file_pattern']
    
    global oi_file_pattern
    oi_file_pattern = config['oi_file_pattern']
    
    global method_vf
    if (config['method_vf'] == 'median'
        or config['method_vf'] == 'mode'
        or config['method_vf'] == 'mean'):
        method_vf = config['method_vf']
    else:
        console.print("[bold red]ERROR: [/bold red][cyan](analysis_config.toml)[/cyan] 'method_vf' setting must be one of the following: 'mode', 'median', 'mean'")
        sys.exit()
    
    global considered_capillaries
    considered_capillaries = config['considered_capillaries']
    
    global conc_dict
    conc_dict = dict_from_lists(config['capillary_info']['capillary'], config['capillary_info']['concentration'])
    
    global melting_points
    melting_points = dict_from_lists(config['capillary_info']['capillary'], config['capillary_info']['melting_points'])
    
    global mode_bins
    mode_bins = config['mode_bins']
   
    global filter_criteria
    filter_criteria = {
        "min vf" : config['filter_criteria']['min_volume_fraction'],
        "max vf": config['filter_criteria']['max_volume_fraction'],
        "max RMSE": config['filter_criteria']['max_RMSE']
                       }
    
    
    
    global plot_settings
    plot_settings = {
        "pd x label": config['figure_captions']['pd_x_label'],
        "pd y label": config['figure_captions']['pd_y_label'],
        "lr x label": config['figure_captions']['lr_x_label'],
        "lr y label": config['figure_captions']['lr_y_label'], 
    }

init()

print(parent_folder)
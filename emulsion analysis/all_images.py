import numpy as np
from analyze3D import analyze_emulsion_image
from parse_parent import parse
import os 

def all_images(parent_folder, abc_guess, epsilon, guess_type):
    """
    all_images runs the image analysis program on every program in a provided directory
    ARGUMENTS:
    parent_folder (string): the full path to parent folder that contains all temperature subfolders
    abc_guess (list): the guesses for the a, b, c labelling intensities for the fit: list of form [a, b, c]
    epsilon (float): the flexibility on the bounds of the fit around the R_dil guess 
        the bounds on R_dil are the guess +/- epsilon
    guess_type (string): pass "signal" if want to base R_den guess on SG-filtered droplet signal,
        pass anything else if you want to guess based on the ilastik object classification area
    """

    img_dict, number_of_images, sorted_folders = parse(parent_folder)
        
    for folder_temp_index, temp_folder in enumerate(sorted_folders):

        cur_folder = img_dict[sorted_folders[folder_temp_index]]
        temp_folder = sorted_folders[folder_temp_index]
        
        print(f"Fetching {temp_folder}")
        
        print(f"\t --> {temp_folder} : {img_dict[sorted_folders[folder_temp_index]]}\n")
        
        log_path = f"{parent_folder}/{temp_folder}/{temp_folder} analysis logs/"
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        cur_folder = img_dict[sorted_folders[folder_temp_index]]
            
        for img_name in cur_folder:
            
            try:
                print(f"Analyzing {img_name} in {temp_folder}")

                ft_path = f"{parent_folder}/{temp_folder}/ilastik/{img_name}_table.csv"
                img_path = f"{parent_folder}/{temp_folder}/{img_name}.tif"

                img_fit_data = analyze_emulsion_image(img_path, ft_path, img_name, v_step = 0.001, abc_guess_list = abc_guess, min_r_dil = 6, EPSILON = epsilon, guess_type = guess_type)
                img_fit_data.write_csv(log_path, img_name)
            # Error "handling"    - might want to remove this, it might not be a great idea...
            
            except(FileNotFoundError) as fnfe:
                print(f"Critical error fitting {img_name}!")
                print(f"TEMPERATURE FOLDER: {cur_folder} SKIPPED!!! \n")
                print(f"TEMPERATURE FOLDER: {cur_folder} SKIPPED!!! \n")
                print(f"Train ilastik on {cur_folder}!") 
                print(fnfe)
            
            except(RuntimeError) as re:
                print(f"Critical error fitting {img_name}!")
                print(re)
                
import numpy as np
from analyze3D import analyzeEmulsionImage3D
from parse_parent import parse
import os 

def all_images(parentFolder, abc_guess, epsilon, guess_type):
    """
    all_images runs the image analysis program on every program in a provided directory
    ARGUMENTS:
    parentFolder (string): the full path to parent folder that contains all temperature subfolders
    abc_guess (list): the guesses for the a, b, c labelling intensities for the fit: list of form [a, b, c]
    epsilon (float): the flexibility on the bounds of the fit around the R_dil guess 
        the bounds on R_dil are the guess +/- epsilon
    guess_type (string): pass "signal" if want to base R_den guess on SG-filtered droplet signal,
        pass anything else if you want to guess based on the ilastik object classification area
    """


    img_dict, number_of_images, sorted_folders = parse(parentFolder)
        
    for folderTempIndex, tempFolder in enumerate(sorted_folders):

        curFolder = img_dict[sorted_folders[folderTempIndex]]
        tempFolder = sorted_folders[folderTempIndex]
        print(sorted_folders[folderTempIndex])
        print(img_dict[sorted_folders[folderTempIndex]])
        
        logPath = f"{parentFolder}/{tempFolder}/{tempFolder} analysis logs/"
        if not os.path.exists(logPath):
            os.makedirs(logPath)

        curFolder = img_dict[sorted_folders[folderTempIndex]]
            
        for imgName in curFolder:
        
            try:
                ftPath = f"{parentFolder}/{tempFolder}/ilastik/{imgName}_table.csv"
                imgPath = f"{parentFolder}/{tempFolder}/{imgName}.tif"

                imgFitData = analyzeEmulsionImage3D(imgPath, ftPath, imgName, vStep = 0.001, abcGuessLi = abc_guess, minDilRadius=6, EPSILON = epsilon, guess_type = guess_type)
                imgFitData.write_csv(logPath, imgName)
            # Error "handling"    - might want to remove this, it might not be a great idea...
            except(RuntimeError):
                print(f"Critical error fitting {imgName}!")
                
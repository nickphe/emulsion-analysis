import numpy as np
from analyze3D import analyzeEmulsionImage3D
from parse_parent import parse
import os 

parentFolder = "/Users/nickphelps/Desktop/2024 01 16"

img_dict, number_of_images, sorted_folders = parse(parentFolder)

abcGuess = [500, 20, 20]
    
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

        ftPath = f"{parentFolder}/{tempFolder}/ilastik/{imgName}_table.csv"
        imgPath = f"{parentFolder}/{tempFolder}/{imgName}.tif"

        imgFitData = analyzeEmulsionImage3D(imgPath, ftPath, imgName, vStep = 0.001, abcGuessLi = abcGuess, minDilRadius=6, EPSILON = 0.5)
        imgFitData.write_csv(logPath, imgName)
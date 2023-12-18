import numpy as np
from analyze3D import analyzeEmulsionImage3D
from parse_parent import parse
import os 

folderTempIndex = 0

parentFolder = "/Users/nickphelps/Desktop/2023 12 07"

img_dict, number_of_images, sorted_folders = parse(parentFolder)
curFolder = img_dict[sorted_folders[folderTempIndex]]
print(img_dict)
abcGuess = [20, 20, 20]
bounds = ([0,0,0,0,0,0,0],[np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf])

for tempFolder in sorted_folders:
    
    logPath = f"{parentFolder}/{tempFolder}/{tempFolder} analysis logs/"
    if not os.path.exists(logPath):
        os.makedirs(logPath)
    
    curFolder = img_dict[sorted_folders[folderTempIndex]]
        
    for imgName in curFolder:
        
        ftPath = f"{parentFolder}/{tempFolder}/ilastik/{imgName}_table.csv"
        imgPath = f"{parentFolder}/{tempFolder}/{imgName}.tif"
        
        imgFitData = analyzeEmulsionImage3D(imgPath, ftPath, imgName, vStep = 0.001, abcGuessLi = abcGuess, bounds = bounds, minDilRadius=10)
        imgFitData.write_csv(logPath, imgName)
    
    folderTempIndex += 1
            
        
import numpy as np
import pandas as pd
from skimage import io
import os
import matplotlib.pyplot as plt

import voronoi
import segment
import fit
import droplet_signal
from remove_suffix import remove_suffix

from tqdm import tqdm

# object: analyzeEmulsionImage3D
# arguments:
#   imgPath - path to the image to be analyzed, string
#   ftPath - path to the ilastik feature table that provides droplet center locations, string
#   outputFolderName - output folder name, string
#   vStep - step size of voronoi.py inflation (see voronoi.py), usually small ~0.005, the size of the iteration of the circle radius increase
#   abcGuessLi - list ([a, b, c]) of initial guesses for the labelling intensities of droplets 
#   bounds - list ([xy_tuple, x_cen, y_cen, a, b, c, R_den, R_dil]) of bounds on 3D fit parameters
#   minDilRadius - reject droplets with a dilute phase radius smaller than this parameter
emptyDict = {'xData': "", 
             'yData': "",
             'values': "",
             'guesses': "",
             'bounds': "",
             'popt': "",
             'pcov': "",
             'uncertainties': "",
             'voronoi rDil': "",
             'rDen guess': "",
             'signal rDen': "",
             'fit xCen': "",
             'fit xCen uncertainty': "",
             'fit yCen': "",
             'fit yCen uncertainty': "",
             'fit a': "",
             'fit a uncertainty': "",
             'fit b': "",
             'fit b uncertainty': "",
             'fit c': "",
             'fit c uncertainty': "",
             'fit rDen': "",
             'fit rDen uncertainty': "",
             'fit rDil': "",
             'fit rDil uncertainty': "",
             'RMSE': "",
             'fit params vf': "",
             'fit den, voronoi dil vf': "",
             'signal den, voronoi dil vf': ""}

class analyzeEmulsionImage3D:
    def __init__(self, imgPath: str, ftPath: str, outputFolderName: str, vStep, abcGuessLi, minDilRadius, EPSILON, guess_type):
        
        self.EPSILON = EPSILON # used to restrict bounds on dilute phase radius guess (cheese method of locking parameter)
        
        self.log = []
        
        self.imgPath = imgPath
        self.ftPath = ftPath
        
        self.parentPath = remove_suffix(self.imgPath, ".tif")
        self.outputFolder = os.path.join(self.parentPath, f"{outputFolderName}")
        self.signalOutputFolder = os.path.join(self.outputFolder, "droplet signals")
        
        if not os.path.exists(self.outputFolder):
                os.makedirs(self.outputFolder)  # Use makedirs to create parent directories if they don't exist
                os.mkdir(self.signalOutputFolder)
        
        self.stepSize = vStep
        
        self.sg_polyOrder = 2
        self.minDilRadius = minDilRadius
        
        self.aGuess = abcGuessLi[0]
        self.bGuess = abcGuessLi[1]
        self.cGuess = abcGuessLi[2]
        
        self.ft = pd.read_csv(ftPath)
        self.img = io.imread(imgPath)
        
        self.xPoints = self.ft["Center of the object_0"].to_numpy()
        self.yPoints = self.ft["Center of the object_1"].to_numpy()
        
        self.object_area = self.ft["Size in pixels"].to_numpy()
        
        # Generate voronoi
        print("\t --> Guessing R_dil / Segmenting...")
        self.circles = voronoi.circles(self.xPoints, self.yPoints)
        self.circles.generateVoronoi(self.stepSize)
        print("\t --> R_dil guesses and segmentation complete.")
        
        fig, ax = plt.subplots(dpi = 200)
        ax.imshow(self.img)
        for point in self.circles.pointList:
            xArr, yArr = point.getCircle(360)
            ax.plot(xArr, yArr)
        plt.savefig(self.outputFolder + "_segmentation_plot.png")
        plt.close()
        
        if guess_type == "signal":
            #self.rDen_guess = self.denseRadii.rDen # guess dense radii based on signal
            signal_flag = True
            #print("Guessing off signals!")
        else:
            signal_flag = False
            self.rDen_guess = np.sqrt(self.object_area / np.pi) # guess dense radii based on object area
        
            
        
        for k, point in tqdm(enumerate(self.circles.pointList)):
            
            if point.radius >= self.minDilRadius:
                
                try:
                    drop = segment.dropletFromImg(self.img, point.x,point.y,point.radius)
                    sg_window = int(point.radius ** 2 * np.pi / 6)
                    self.denseRadii = droplet_signal.dropletSignal(drop.rPositions, drop.values, sg_window, self.sg_polyOrder)
                    extra_data = self.denseRadii.rDen
                    if signal_flag:
                        guessLi = [drop.x,drop.y,self.aGuess,self.bGuess,self.cGuess, self.denseRadii.rDen, drop.radius]
                    else:
                        guessLi = [drop.x,drop.y,self.aGuess,self.bGuess,self.cGuess, self.rDen_guess[k], drop.radius]
                    bounds = ([0,0,0,0,0,0,drop.radius - self.EPSILON],[np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,drop.radius + self.EPSILON])
                    fitData = fit.dropletFit3D(drop.xPositions, drop.yPositions, drop.values, guessLi, bounds, extra = extra_data)
                    #print(fitData)
                    #print(f"{round(k / len(self.circles.pointList), 3) * 100}% complete.")
                    self.log.append(fitData.fitDict)
                    #self.denseRadii.saveFig(self.signalOutputFolder, str(point)) #save droplet signal figures
                    plt.close()
                    
                except RuntimeError:
                    self.log.append(emptyDict)
                    print("RuntimeError encountered in fitting step!")
                    continue
                
    def write_csv(self, path, name):
        print("Writing analysis log.")
        df = pd.DataFrame(self.log)
        csvPath = path + name + "_analysis_log.csv"
        df.to_csv(csvPath)
        print("Analysis log complete.")
        del (df)

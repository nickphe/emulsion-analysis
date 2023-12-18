import numpy as np
import pandas as pd
from skimage import io

import voronoi
import segment
import fit
import radii

class analyzeSignals:
    def __init__(self, imgPath: str, ftPath: str, vStep, sg_polyorder, minDilRadius):
        
        self.imgPath = imgPath
        self.ftPath = ftPath
        
        self.stepSize = vStep
    
        self.sg_polyorder = sg_polyorder
        
        self.minDilRadius = minDilRadius
        
        self.ft = pd.read_csv(ftPath)
        self.img = io.imread(imgPath)
        
        self.xPoints = self.ft["Center of the object_0"].to_numpy()
        self.yPoints = self.ft["Center of the object_1"].to_numpy()
        
        self.log = []
        
        print("Generating Voronoi...")
        self.circles = voronoi.circles(self.xPoints, self.yPoints)
        self.circles.generateVoronoi(self.stepSize)
        print("Voronoi Complete.")
        
        counter = 0
        for point in self.circles.pointList:
            counter += 1
            if point.radius >= self.minDilRadius:
                sg_window = int(point.radius ** 2 * np.pi / 6)  
                drop = segment.dropletFromImg(self.img, point.x,point.y,point.radius)
                denseRadii = radii.dropletSignal(drop.rPositions, drop.values, sg_window, self.sg_polyorder)
                print(denseRadii)
                denseRadii.saveFig("/Users/nickphelps/Desktop/2023 12 07/18C/cap1 figs",str(counter))


ftPath = "/Users/nickphelps/Desktop/2023 12 07/18C/ilastik/cap1_40_4.0_table.csv"
imgPath = "/Users/nickphelps/Desktop/2023 12 07/18C/cap1_40_4.0.tif"
analyzeSignals(imgPath, ftPath, 0.005, 2, 5)
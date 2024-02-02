import numpy as np
import pandas as pd
from skimage import io
import os
import matplotlib.pyplot as plt

import inflate
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
#   vStep - step size of inflate.py inflation (see inflate.py), usually small ~0.005, the size of the iteration of the circle radius increase
#   abcGuessLi - list ([a, b, c]) of initial guesses for the labelling intensities of droplets 
#   bounds - list ([xy_tuple, x_cen, y_cen, a, b, c, R_den, R_dil]) of bounds on 3D fit parameters
#   minDilRadius - reject droplets with a dilute phase radius smaller than this parameter
empty_dict = {'xData': "", 
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

class analyze_emulsion_image:
    def __init__(self, imgPath: str, ftPath: str, outputFolderName: str, v_step, abc_guess_list, min_r_dil, EPSILON, guess_type):
        
        self.EPSILON = EPSILON # used to restrict bounds on dilute phase radius guess (cheese method of locking parameter)
        
        self.log = []
        
        self.img_path = imgPath
        self.ft_path = ftPath
        
        self.parent_path = remove_suffix(self.img_path, ".tif")
        self.output_folder = os.path.join(self.parent_path, f"{outputFolderName}")
        self.signal_output_folder = os.path.join(self.output_folder, "droplet signals")
        
        if not os.path.exists(self.output_folder):
                os.makedirs(self.output_folder)  # Use makedirs to create parent directories if they don't exist
                os.mkdir(self.signal_output_folder)
        
        self.step_size = v_step
        
        self.sg_polynomial_order = 2
        self.min_r_dil = min_r_dil
        
        self.a_guess = abc_guess_list[0]
        self.b_guess = abc_guess_list[1]
        self.c_guess = abc_guess_list[2]
        
        self.ft = pd.read_csv(ftPath)
        
        if self.ft.size > 1: # make sure that ilastik segmented something!
        
            self.img = io.imread(imgPath)
            
            self.x_points = self.ft["Center of the object_0"].to_numpy()
            self.y_points = self.ft["Center of the object_1"].to_numpy()
            
            self.object_area = self.ft["Size in pixels"].to_numpy()
            
            # Segment / Guess R_dil
            print("\t --> Guessing R_dil / Segmenting...")
            self.circles = inflate.Circles(self.x_points, self.y_points)
            self.circles.inflate(self.step_size)
            print("\t --> R_dil guesses and segmentation complete.")
            
            fig, ax = plt.subplots(dpi = 200)
            ax.imshow(self.img)
            for point in self.circles.point_list:
                x_arr, y_arr = point.get_circle(360)
                ax.plot(x_arr, y_arr)
            plt.savefig(self.output_folder + "_segmentation_plot.png")
            plt.close()
            
            if guess_type == "signal":
                #self.rDen_guess = self.denseRadii.rDen # guess dense radii based on signal
                signal_flag = True
                #print("Guessing off signals!")
            else:
                signal_flag = False
                self.rDen_guess = np.sqrt(self.object_area / np.pi) # guess dense radii based on object area
            
                
            
            for k, point in tqdm(enumerate(self.circles.point_list)):
                
                if point.radius >= self.min_r_dil:
                    
                    try:
                        drop = segment.droplet_from_img(self.img, point.x,point.y,point.radius)
                        sg_window = int(point.radius ** 2 * np.pi / 6)
                        self.dense_radii = droplet_signal.DropletSignal(drop.r_positions, drop.values, sg_window, self.sg_polynomial_order)
                        extra_data = self.dense_radii.r_den
                        if signal_flag:
                            guess_list = [drop.x,drop.y,self.a_guess,self.b_guess,self.c_guess, self.dense_radii.r_den, drop.radius]
                        else:
                            guess_list = [drop.x,drop.y,self.a_guess,self.b_guess,self.c_guess, self.rDen_guess[k], drop.radius]
                        bounds = ([0,0,0,0,0,0,drop.radius - self.EPSILON],[np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,drop.radius + self.EPSILON])
                        fit_data = fit.dropletFit3D(drop.x_positions, drop.y_positions, drop.values, guess_list, bounds, extra = extra_data)
                        #print(fitData)
                        #print(f"{round(k / len(self.circles.pointList), 3) * 100}% complete.")
                        self.log.append(fit_data.fit_dict)
                        #self.denseRadii.saveFig(self.signalOutputFolder, str(point)) #save droplet signal figures
                        plt.close()
                        
                    except RuntimeError:
                        self.log.append(empty_dict)
                        print("RuntimeError encountered in fitting step!")
                        continue
    
        else:
            print(f"==> ERROR: SKIPPING {self.img_path}. NO ILASTIK FEATURES IDENTIFIED!")
    
                
    def write_csv(self, path, name):
        print("Writing analysis log.")
        df = pd.DataFrame(self.log)
        csv_path = path + name + "_analysis_log.csv"
        df.to_csv(csv_path)
        print("Analysis log complete.")
        del (df)

import numpy as np
from scipy.signal import savgol_filter as SGfilter
import matplotlib.pyplot as plt
import scienceplots

# function: FWHM 
# takes finds a rough estimate of the full-width-half-max of a signal peak.
def FWHM(max_loc, x, y):
    amax = y[max_loc]
    stop = amax * 0.5
    indR = max_loc
    while indR < len(y) and y[indR] > stop:
        indR += 1
    indL = max_loc
    while indL >= 0 and y[indL] > stop:
        indL += -1
    indR = min(indR, len(x) - 1)
    indL = max(indL, 0)
    fw = x[indR] - x[indL]
    return fw

# object: dropletSignal 
#   droplet signal converts the intensity data in array form into a "signal" of intensity vs. radii
#   handles filtering of the data and its derivatives
class dropletSignal:
    def __init__(self, rInput, IInput, sg_window, sg_polyorder):
        self.rIn = rInput
        self.IIn = IInput
        self.sg_window = sg_window
        self.sg_polyorder = sg_polyorder
        
        newOrder = np.lexsort([self.IIn, self.rIn])
        self.r = self.rIn[newOrder]
        self.I = self.IIn[newOrder]
        
        self.filtered_I = SGfilter(self.I, self.sg_window, self.sg_polyorder)
        self.filtered_DI = SGfilter(np.gradient(self.filtered_I), self.sg_window, self.sg_polyorder)
        self.filtered_D2I = SGfilter(np.gradient(self.filtered_DI), self.sg_window, self.sg_polyorder)
        
        self.norm_I = self.filtered_I/np.max(np.abs(self.filtered_I))
        self.norm_DI = self.filtered_DI/np.max(np.abs(self.filtered_DI))
        self.norm_D2I = self.filtered_D2I/np.max(np.abs(self.filtered_D2I))
        
        self.rIndex = int(np.argmax(self.norm_D2I))
        self.rDen = self.r[self.rIndex]
        self.D2I_FWHM = FWHM(self.rIndex, self.r, self.norm_D2I)
    
    # function: makeFig, makes a figure of the signal data
    def makeFig(self):
        with plt.style.context(["science","nature"]):
            fig, ax = plt.subplots(figsize=(5,5), dpi = 150)
            ax.plot(self.r, self.norm_I, label = "$I$")
            ax.plot(self.r, self.norm_DI, label = "$\\frac{dI}{dr}$")
            ax.plot(self.r, self.norm_D2I, label = "$\\frac{d^2I}{dr^2}$")
            ax.scatter(self.r[self.rIndex], self.norm_I[self.rIndex], color = "red")
            ax.scatter(self.r[self.rIndex], self.norm_DI[self.rIndex], color = "red")
            ax.scatter(self.r[self.rIndex], self.norm_D2I[self.rIndex], color = "red")
            ax.set_xlabel("$r$ px")
            ax.set_ylabel("$I / I_{\\mathrm{|max|}}$ (a.u.)")
            ax.legend()
        return fig
    
    # function: saveFig
    # makes a figure at a specified path (make sure to not include ending /) with a specified name
    def saveFig(self, path, name):
        fig = self.makeFig()
        plt.savefig(f'{path}/{name}.png')
        plt.close()
        
    def __str__(self):
        return f"dense phase radius from signal: {self.rDen}, FWHM of peak: {self.D2I_FWHM} px"
        
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd

def RMSE(observed, expected, N):
    return np.sqrt(np.sum(np.square(observed-expected))/N)

def coordinatesToTuples(xCoords, yCoords):
    # Check if the lengths of xCoords and yCoords are the same
    if len(xCoords) != len(yCoords):
        raise ValueError("Arrays must have the same length")
    # Combine xCoords and yCoords into tuples
    coordinatesTuples = list(zip(xCoords, yCoords))
    return coordinatesTuples

def doubleSphere2D(r, rCen, a, b, c, rDen, rDil):
    
    # Ensure R_den is not greater than R_dil
    if rDen < rDil:
        rDen, rDil = rDil, rDen
        
    rSquared = np.square(r-rCen)
    rDenSquared = np.square(rDen)
    rDilSquared = np.square(rDil)
    
    result = np.ones(len(r))*a  # Initialize result array with 'a' (background) value
    
    # Define conditions for dense/dil regions
    denseRegimeCondition = rSquared <= rDenSquared 
    dilRegimeCondition = rSquared > rDenSquared
    
    # Calculate the term inside the dense regime sqrt and ensure it's non-negative
    denSqrtTerm = rDenSquared - rSquared
    denSqrtPositiveCondition = np.where(denSqrtTerm > 0, denSqrtTerm, 0)
    denTerm = np.sqrt(denSqrtPositiveCondition)
    
    # Calculate the term inside the dilute regime sqrt and ensure it's non-negative
    dilSqrtTerm = rDilSquared - rSquared
    dilSqrtPositiveCondition = np.where(dilSqrtTerm > 0, dilSqrtTerm, 0)
    dilTerm = np.sqrt(dilSqrtPositiveCondition)
    
    # When in dense regime, add dense regime term
    result += np.where(denseRegimeCondition, 2*b*denTerm + 2*c*dilTerm, 0)
    
    # When in dilute regime, add dilute regime term 
    result += np.where(dilRegimeCondition, 2*c*dilTerm, 0)
    
    return result

#droplet intensity profile function 
def doubleSphere3D(xy_tuple, x_cen, y_cen, a, b, c, R_den, R_dil):
    #vectorized just means it takes an entire array at a time as input and computes in parallel. thanks numpy :) 
    
    # Ensure R_den is not greater than R_dil
    if R_den < R_dil:
        R_den, R_dil = R_dil, R_den
        
    x, y = xy_tuple
    r_squared = np.square(x - x_cen) + np.square(y - y_cen)
    r_den_squared = R_den**2
    r_dil_squared = R_dil**2
    
    result = np.ones(len(x))*a  # Initialize result array with 'a' (background) value
    
    # Define conditions for dense/dil regions
    dense_regime_condition = r_squared <= r_den_squared 
    dil_regime_condition = r_squared > r_den_squared
    
    # Calculate the term inside the dense regime sqrt and ensure it's non-negative
    den_sqrt_term = r_den_squared - r_squared
    den_sqrt_positive_condition = np.where(den_sqrt_term > 0, den_sqrt_term, 0)
    den_term = np.sqrt(den_sqrt_positive_condition)
    
    # Calculate the term inside the dilute regime sqrt and ensure it's non-negative
    dil_sqrt_term = r_dil_squared - r_squared
    dil_sqrt_positive_condition = np.where(dil_sqrt_term > 0, dil_sqrt_term, 0)
    dil_term = np.sqrt(dil_sqrt_positive_condition)
    
    # When in dense regime, add dense regime term
    result += np.where(dense_regime_condition, 2*b*den_term + 2*c*dil_term, 0)
    
    # When in dilute regime, add dilute regime term 
    result += np.where(dil_regime_condition, 2*c*dil_term, 0)
    
    return result

class dropletFit3D:
    def __init__(self, xData, yData, values, guesses: list, bounds):
        #Arguments
            # data: [x data, y data]
            # values: an array of values to fit to corresponding to the coordinates
            # guesses: guesses in shape of [x_cen, y_cen, a, b, c, R_den, R_dil]
            # bounds: bounds in shape of [x_cen, y_cen, a, b, c, R_den, R_dil]
        self.xData = xData
        self.yData = yData
        self.values = values
        self.coordTupleArray = coordinatesToTuples(xData,yData)
        
        self.guessList = guesses
        self.boundsList = bounds
        
        self.popt, self.pcov, self.infodict, self.mesg, self.ier = curve_fit(doubleSphere3D, 
                                                                             [self.xData, self.yData], # input coordinates
                                                                             self.values, # data to fit to 
                                                                             p0 = self.guessList, # initial guesses
                                                                             bounds = self.boundsList, # bounds
                                                                             full_output=True)
        self.uncertainties = np.diag(self.pcov)**2
        
        self.xCen = self.popt[0]
        self.yCen = self.popt[1]
        self.a = self.popt[2]
        self.b = self.popt[3]
        self.c = self.popt[4]
        self.rDen = self.popt[5]
        self.rDil = self.popt[6]
        
        self.xCenU = self.uncertainties[0]
        self.yCenU = self.uncertainties[1]
        self.aU = self.uncertainties[2]
        self.bU = self.uncertainties[3]
        self.cU = self.uncertainties[4]
        self.rDenU = self.uncertainties[5]
        self.rDilU = self.uncertainties[6]
        self.RMSE = RMSE(self.values, doubleSphere3D([self.xData, self.yData], self.xCen, self.yCen, self.a, self.b, self.c, self.rDen, self.rDil), len(self.values))
        
        self.fitDict = {'xData': self.xData, 
             'yData': self.yData,
             'values': self.values,
             'guesses': self.guessList,
             'bounds': self.boundsList,
             'popt': self.popt,
             'pcov': self.pcov,
             'uncertainties': self.uncertainties,
             'fit xCen': self.xCen,
             'fit xCen uncertainty': self.xCenU,
             'fit yCen': self.yCen,
             'fit yCen uncertainty': self.yCenU,
             'fit a': self.a,
             'fit a uncertainty': self.aU,
             'fit b': self.b,
             'fit b uncertainty': self.bU,
             'fit c': self.c,
             'fit c uncertainty': self.cU,
             'fit rDen': self.rDen,
             'fit rDen uncertainty': self.rDenU,
             'fit rDil': self.rDil,
             'fit rDil uncertainty': self.rDilU,
             'RMSE': self.RMSE,
             'fit params vf': self.rDen**3 / self.rDil**3,
             'fit den, voronoi dil vf': self.rDen**3 / self.guessList[-1]**3,
             'signal den, voronoi dil vf': self.guessList[-2]**3 / self.guessList[-1]**3}
        
    def __str__(self):
        return f"rDen = {self.rDen}±{self.rDenU}, rDil = {self.rDil}±{self.rDilU}, location: ({self.xCen}, {self.yCen}), RMSE: {self.RMSE}"
    

        
        
        
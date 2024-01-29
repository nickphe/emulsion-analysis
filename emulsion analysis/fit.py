import numpy as np
from scipy.optimize import curve_fit
import pandas as pd

def RMSE(observed, expected, N):
    return np.sqrt(np.sum(np.square(observed-expected))/N)

def coords_to_tuples(x, y):
    # Check if the lengths of x and y are the same
    if len(x) != len(y):
        raise ValueError("Arrays must have the same length")
    # Combine xCoords and yCoords into tuples
    coords_tuples = list(zip(x, y))
    return coords_tuples

def double_sphere_radial(r, r_cen, a, b, c, r_den, r_dil):
    
    # Ensure R_den is not greater than R_dil
    if r_den < r_dil:
        r_den, r_dil = r_dil, r_den
        
    r_squared = np.square(r-r_cen)
    r_den_squared = np.square(r_den)
    r_dil_squared = np.square(r_dil)
    
    result = np.ones(len(r))*a  # Initialize result array with 'a' (background) value
    
    # Define conditions for dense/dil regions
    den_regime_condition = r_squared <= r_den_squared 
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
    result += np.where(den_regime_condition, 2*b*den_term + 2*c*dil_term, 0)
    
    # When in dilute regime, add dilute regime term 
    result += np.where(dil_regime_condition, 2*c*dil_term, 0)
    
    return result

#droplet intensity profile function 
def double_sphere_intensity_profile(xy_tuple, x_cen, y_cen, a, b, c, r_den, r_dil):
    #vectorized just means it takes an entire array at a time as input and computes in parallel. thanks numpy :) 
    
    # Ensure R_den is not greater than R_dil
    if r_den < r_dil:
        r_den, r_dil = r_dil, r_den
        
    x, y = xy_tuple
    r_squared = np.square(x - x_cen) + np.square(y - y_cen)
    r_den_squared = r_den**2
    r_dil_squared = r_dil**2
    
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
    def __init__(self, x_data, y_data, values, guesses: list, bounds, extra):
        #Arguments
            # data: [x data, y data]
            # values: an array of values to fit to corresponding to the coordinates
            # guesses: guesses in shape of [x_cen, y_cen, a, b, c, R_den, R_dil]
            # bounds: bounds in shape of [x_cen, y_cen, a, b, c, R_den, R_dil]
        self.x_data = x_data
        self.y_data = y_data
        self.values = values
        self.coord_tuple_arr = coords_to_tuples(x_data,y_data)
        
        self.guess_list = guesses
        self.bounds_list = bounds
        
        self.extra = extra
        
        self.r_dil_guess = self.guess_list[-1]
        self.r_den_guess = self.guess_list[-2]
        
        self.popt, self.pcov, self.infodict, self.mesg, self.ier = curve_fit(double_sphere_intensity_profile, 
                                                                             [self.x_data, self.y_data], # input coordinates
                                                                             self.values, # data to fit to 
                                                                             p0 = self.guess_list, # initial guesses
                                                                             bounds = self.bounds_list, # bounds
                                                                             full_output=True)
        self.uncertainties = np.diag(self.pcov)**2
        
        self.x_cen = self.popt[0]
        self.y_cen = self.popt[1]
        self.a = self.popt[2]
        self.b = self.popt[3]
        self.c = self.popt[4]
        self.r_den = self.popt[5]
        self.r_dil = self.popt[6]
        
        self.x_cen_uncert = self.uncertainties[0]
        self.y_cen_uncert = self.uncertainties[1]
        self.a_uncert = self.uncertainties[2]
        self.b_uncert = self.uncertainties[3]
        self.c_uncert = self.uncertainties[4]
        self.r_den_uncert = self.uncertainties[5]
        self.r_dil_uncert = self.uncertainties[6]
        self.rmse = RMSE(self.values, double_sphere_intensity_profile([self.x_data, self.y_data], self.x_cen, self.y_cen, self.a, self.b, self.c, self.r_den, self.r_dil), len(self.values))
        
        self.fit_dict = {'xData': self.x_data, 
             'yData': self.y_data,
             'values': self.values,
             'guesses': self.guess_list,
             'bounds': self.bounds_list,
             'popt': self.popt,
             'pcov': self.pcov,
             'uncertainties': self.uncertainties,
             'voronoi rDil': self.r_dil_guess,
             'rDen guess': self.r_den_guess,
             'signal rDen': self.extra,
             'fit xCen': self.x_cen,
             'fit xCen uncertainty': self.x_cen_uncert,
             'fit yCen': self.y_cen,
             'fit yCen uncertainty': self.y_cen_uncert,
             'fit a': self.a,
             'fit a uncertainty': self.a_uncert,
             'fit b': self.b,
             'fit b uncertainty': self.b_uncert,
             'fit c': self.c,
             'fit c uncertainty': self.c_uncert,
             'fit rDen': self.r_den,
             'fit rDen uncertainty': self.r_den_uncert,
             'fit rDil': self.r_dil,
             'fit rDil uncertainty': self.r_dil_uncert,
             'RMSE': self.rmse,
             'fit params vf': self.r_den**3 / self.r_dil**3,
             'fit den, voronoi dil vf': self.r_den**3 / self.guess_list[-1]**3,
             'signal den, voronoi dil vf': self.guess_list[-2]**3 / self.guess_list[-1]**3}
        
    def __str__(self):
        return f"rDen = {self.r_den}±{self.r_den_uncert}, rDil = {self.r_dil}±{self.r_dil_uncert}, location: ({self.x_cen}, {self.y_cen}), RMSE: {self.rmse}"
    

        
        
        
import numpy as np

def RMSE(observed, expected, N):
    return np.sqrt(np.sum(np.square(observed-expected))/N)

def RMSD(observed):
    return np.sqrt(np.sum(np.square(observed-np.mean(observed)))/len(observed))

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
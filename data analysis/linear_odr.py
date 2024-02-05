from scipy.odr import Model, Data, ODR
import numpy as np

def lin_model_odr(params, x):
    return params[0] * x + params[1]

def linear_odr(x, y, x_u, y_u, m_inguess, b_inguess):

    x = np.array(x)
    y = np.array(y)
    x_u = np.array(x_u)
    y_u = np.array(y_u)
    data = Data(x, y, wd=1.0/y_u**2, we=1.0/x_u**2)
    
    # ceate ODR Model object
    model = Model(lin_model_odr)

    # initialize ODR object with the data and model
    odr = ODR(data, model, beta0=[m_inguess, b_inguess])
    odr_result = odr.run()

    popt_odr = odr_result.beta
    pcov_odr = odr_result.cov_beta
    psd_odr = odr_result.sd_beta
    
    return popt_odr, pcov_odr, psd_odr

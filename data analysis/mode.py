import numpy as np

def mode(arr, bin_count: int):
    count, bins = np.histogram(arr, bin_count)
    #print(f"count: {count}, bins: {bins}")
    # np.histogram bins are half open except for last 
    # e.g. [1,2,3], bins would be [1,2), [2,3]
    tallest_bin_index = np.argmax(count)
   # print(f"tallest bin index: {tallest_bin_index}")
    a = bins[tallest_bin_index]
    b = bins[tallest_bin_index + 1]
    m = (a + b) / 2.0
    #print(f"mode: {m}")
    return m

def FWHM_uncertainty(max_loc, x, y):
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
    return fw/2
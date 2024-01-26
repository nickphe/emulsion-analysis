import numpy as np

def mode(arr, bin_count: int):
    count, bins = np.histogram(arr, bin_count)
    # np.histogram bins are half open except for last 
    # e.g. [1,2,3], bins would be [1,2), [2,3]
    tallest_bin_index = np.argmax(count)
    a = bins[tallest_bin_index]
    b = bins[tallest_bin_index + 1]
    m = (a + b) / 2.0
    return m
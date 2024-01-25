import numpy as np
import pandas as pd

import settings
settings.init()


filt = settings.filter_criteria

def filter_data(df):
    flt_df = df.loc[
        (df['RMSE'] < filt["max RMSE"]) &
        (df['fit params vf'] < filt["max vf"]) &
        (df['fit params vf'] > filt["min vf"])
    ]

    return flt_df

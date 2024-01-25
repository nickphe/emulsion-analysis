import numpy as np
import pandas as pd

import re
import os

import settings
settings.init()

from output import create_directory

from capillary import Capillary

class Temperature:
    def __init__(self, name: str, value: float, associated_capillaries):
        
        self.name = name
        self.value = value
        self.capillary_names = associated_capillaries
        
        self.capillaries = []
        # list(obj): list of capillary objects
        
    # initiate directory that will hold temperature data
        self.folder_path = os.path.join(settings.output_path, self.name)
        create_directory(self.folder_path)
        
        
        for cap_name in self.capillary_names:
            cap = Capillary(cap_name, self.name)
            self.capillaries.append(cap)
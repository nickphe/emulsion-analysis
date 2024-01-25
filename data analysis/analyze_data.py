import numpy as np
import pandas as pd

import re
import os

import settings
settings.init()

from temperature import Temperature
from parse_parent import parse, extract_numeric_part
from output import create_directory

parent_folder = settings.parent_folder
create_directory(settings.output_path)

# the parent foler containing all child temperature directories
parsed_folder = parse(parent_folder)

temp_name_list = list(parsed_folder[0].keys()) 
# list(str): list of temperature folder names e.g. '17.1C'

capillaries_list = list(parsed_folder[0].values())
# list(str): list(list(str)) list of list of capillaries associated with a given temperature

temp_value_list = [extract_numeric_part(temp) for temp in temp_name_list] 
# list(float): the list of numeric values of corresponding folder names

temp_obj_list = []

for i, name in enumerate(temp_name_list):
    
    value = temp_value_list[i]
    associated_capillaries = capillaries_list[i]
    temp = Temperature(name, value, associated_capillaries)
    temp_obj_list.append(temp)
    
print(temp_obj_list[1].capillaries[1].raw_data)
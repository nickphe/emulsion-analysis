import numpy as np
import pandas as pd

import re
import os

import settings
settings.init()
output_path = settings.output_path

from rich.console import Console
console = Console()

from temperature import Temperature
from parse_parent import parse, extract_numeric_part
from output import create_directory
from phase_diagram import save_phase_diagram

from tqdm import tqdm

# the parent foler containing all child temperature directories
parent_folder = settings.parent_folder
parsed_folder = parse(parent_folder)

temp_name_list = list(parsed_folder[0].keys()) 
# list(str): list of temperature folder names e.g. '17.1C'

capillaries_list = list(parsed_folder[0].values())
# list(str): list(list(str)) list of list of capillaries associated with a given temperature

temp_value_list = [extract_numeric_part(temp) for temp in temp_name_list] 
# list(float): the list of numeric values of corresponding folder names

temp_obj_list = []

create_directory(output_path)
console.print(f"[bold white]Parsing[/bold white] {parent_folder}")
with console.status("[bold green]Analyzing data...") as status:
    for i, name in enumerate(temp_name_list):
        
        value = temp_value_list[i]
        associated_capillaries = capillaries_list[i]
        temp = Temperature(name, value, associated_capillaries)
        temp_obj_list.append(temp)
        
        console.log(f"[bold red] Completed[/bold red]: [cyan]{name}[/cyan]")


with console.status("[bold green]Generating phase diagram...") as status:      
    save_phase_diagram(temp_obj_list, settings.melting_points.values(), settings.conc_dict.values())

console.print("[bold green]Analysis complete.")
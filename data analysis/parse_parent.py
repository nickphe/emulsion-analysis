import re
import os

# regex pattern to match the entire folder name up to "C" with an optional decimal part
# are defined within the functions to be called 

def extract_numeric_part(folder_name):
    pattern = r'(\d+(\.\d+)?)C?'
    match = re.match(pattern, folder_name)
    if match:
        return float(match.group(1))
    return 0.0  # Return 0.0 if no match is found

# extract capillary part
def extract_cap_part(file_name):
    pattern_cap = r'(?i)cap\d+'
    match = re.search(pattern_cap, file_name)
    if match:
        return match.group()
    return ""

# Define the folder path of the Parent folder containing all temperature subfolders
# make sure every subfolder in form of e.g. "23C" so, #C
def parse(folder_path):

    counter = 0

    # Get a list of all directory contents (files and folders)
    directory_contents = os.listdir(folder_path)

    # Filter and sort only folder names based on the numeric part
    folder_names = [name for name in directory_contents if os.path.isdir(os.path.join(folder_path, name))]
    sorted_folders = sorted(folder_names, key=extract_numeric_part)

    img_dict = {} # Define a dictionary to store folder names and their corresponding file names
    image_type = ".tif" # image type to remove from path

    # Sort and iterate through the folders
    for folder in sorted_folders:
        folder_contents = os.listdir(os.path.join(folder_path, folder))
        names = []

        for file in folder_contents:
            file_path = os.path.join(folder_path, folder, file)

            if os.path.isfile(file_path) and file != ".DS_Store" and file.endswith(image_type):
                name = file[:-len(image_type)]
                names.append(name)
                counter += 1

        names = sorted(names, key=extract_cap_part) #sort names within temperature folders by capillary #
        img_dict[folder] = names
        
    number_of_images = counter
    
    return img_dict, number_of_images, sorted_folders
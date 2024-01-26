import os

def create_directory(directory_path: str):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        #print(f"Directory '{directory_path}' created.")
    else:
        pass
        #print(f"Directory '{directory_path}' already exists.")

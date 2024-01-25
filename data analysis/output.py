import os

def create_directory(directory_path: str):
    if not os.path.exists(directory_path):
        os.mkdir(f"{directory_path}")
        print(f"Directory '{directory_path}' created.")
    else:
        print(f"Directory '{directory_path}' already exists.")

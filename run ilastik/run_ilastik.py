import subprocess, os, toml
from parse_parent import parse
from rich.console import Console
console = Console()
config = toml.load("/Users/nickphelps/Desktop/emulsion-analysis-main/settings/training_config.toml")

path_to_ilastik = config['path_to_ilastik']
parent_folder = config['parent_folder']
ilastik_project = config['ilastik_project']
file_extension = config['file_extension']
export_source = config['export_source']

parsed_path = parse(parent_folder)
folders = list(parsed_path[0].keys())

for i, folder in enumerate(folders):
    ims = list(parsed_path[0].values())[i]
    
    ilastik_input = []
    for im in ims:
        impath = f"{parent_folder}/{folder}/{im}.{file_extension}"
        ilastik_input.append(impath)
    console.print(ilastik_input)
    
    try:
        with console.status(f"[bold cyan]Processing folder: [/bold cyan][bold red]{folder}[/bold red] \n") as status:
            subprocess.run([
                            path_to_ilastik,
                            '--headless', # run ilastik in "headless mode" i.e. no gui
                           f'--project={ilastik_project}', # path to .ilp ilastik project
                           f'--output_format={file_extension}', # object identity output format 
                           f'--export_source={export_source}', # export object identities
                            '--table_filename={dataset_dir}/ilastik/{nickname}.csv', 
                            '--output_filename_format={dataset_dir}/ilastik/{nickname}_{result_type}.tif'] +
                            ilastik_input # raw data input
                        )
            
        # ilastik spits out a shit ton of warnings and info, this is an ilastik problem. 
    except:
        console.print(f"[bold red]ERROR: CRITICAL ERROR PROCESSING {folder}[/bold red]")

console.print("[bold green]ilastik processing complete!")
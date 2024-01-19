# Phase Diagram Analysis Protocol

Before you run the code, follow this: [ilastik protocol](ilastik_protocol.md)!
To analyze a dataset for a phase diagram we require a file structure like so:

    parent folder

        |
    
        temperature folder
    
            |
            
            capillary images

            ilastik

                |

                ilastik feature tables

                ilastik object identity images

The program will then create necessary directories as it goes.
The ilastik folder should already be created if the [ilastik protocol](ilastik_protocol.md) was followed correctly.

## Command Line Interface

To run the code, we will use the command line interface, [cli.py](cli.py). First, change directories to the "emulsion analysis" folder:

>cd /path/to/"Emulsion Analysis"

To run the program we run:

>python3 cli.py arg1 arg2 arg3 ...

Everything following cli.py is an argument, the specific argument structure required is:

>python3 cli.py _(path to parent folder)_ _(a guess)_ _(b guess)_ _(c guess)_ _(epsilon)_ _(guess type)_

- "a guess": guess for fitting parameter, the labelling intensity "a"

- "b guess": guess for fitting parameter, the labelling intensity "b"

- "c guess": guess for fitting parameter, the labelling intensity "c"

- "epsilon": provides the bounds on $R_\mathrm{dil}$ in fit. The bounds are:
$(R_\mathrm{dil}^\mathrm{guess} - \epsilon) < R_\mathrm{dil}^\mathrm{fit} < (R_\mathrm{dil}^\mathrm{guess} + \epsilon)$

- "guess type": can be either "signal" or "area". "signal" will provide $R_\mathrm{den}$ guesses based on a filtered, averaged,
radial intensity signal of the droplet (see [signal.py](signal.py)). "area" will provide $R_\mathrm{den}$ guesses based on the
_object area_ feature of the ilastik feature table.

#### Example usage:

> python3 cli.py "/Users/nanostars/Desktop/2024 01 16 HPLC 50_ a3x1 50_ a4" 500.0 20 20 0.5 area      

This would run the analysis with (a = 500, b = 20, c = 20, epsilon = 0.5) and using "area" type $R_\mathrm{den}$ guessing.

#### Notes:

You must provide the full path of the parent folder. 

If there are any spaces in your parent folder path, capture it in double-quotes. 




        
    

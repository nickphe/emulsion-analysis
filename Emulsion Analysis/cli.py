import argparse
from pathlib import Path

from all_images import all_images

parser = argparse.ArgumentParser()
parser.add_argument("path")
parser.add_argument("a")
parser.add_argument("b")
parser.add_argument("c")
parser.add_argument("epsilon")
parser.add_argument("guess_type")

args = parser.parse_args()
parent_folder = Path(args.path)

a = float(args.a)
b = float(args.b)
c = float(args.c)
abc_list = [a, b, c]

epsilon = float(args.epsilon)
guess_type = args.guess_type

if not parent_folder.exists():
    print("The target directory doesn't exist")
    raise SystemExit(1)

for entry in parent_folder.iterdir():
    print(entry.name)

#Error handling
if not isinstance(a, (int, float)):
    print("Please enter a valid number for 'a'")
    raise SystemExit(1)
if not isinstance(b, (int, float)):
    print("Please enter a valid number for 'b'")
    raise SystemExit(1)
if not isinstance(c, (int, float)):
    print("Please enter a valid number for 'c'")
    raise SystemExit(1)
    
if not isinstance(epsilon, (int, float)):
    print("Please enter a valid number for 'epsilon'")
    raise SystemExit(1)
    
if not isinstance(guess_type, str):
    print("Please enter a valid input for 'guess_type'")
    print("'signal' -> will provide fit guesses based on droplet signal")
    print("'area' -> will provide fit guesses based on ilastik object area")
    raise SystemExit(1)

all_images(parent_folder, abc_list, epsilon, guess_type)
    
    
    

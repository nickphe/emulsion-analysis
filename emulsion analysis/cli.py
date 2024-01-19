import argparse
from pathlib import Path

from all_images import all_images

import time

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

if guess_type != "signal" and guess_type != "area":
    print("Guess type not given by 'signal' or 'area'.")
    print("Defaulting to using area-based guesses.")
    guess_type = "area"

print(f"Analyzing folder: {parent_folder}")
print(f"with")
print(f"labeling intensity parameters: a = {a}, b = {b}, c = {c}")
print(f"R_dil bounds parameters: epsilon = {epsilon}")
print(f"R_den guesses provided by: {guess_type}\n")

start = time.time()
all_images(parent_folder, abc_list, epsilon, guess_type)
end = time.time()

print(f"Analysis completed in: {round(end-start, 3) / 60} minutes")
    
    

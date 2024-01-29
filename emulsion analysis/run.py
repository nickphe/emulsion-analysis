from all_images import all_images
import time
import toml

config = toml.load("/Users/nickphelps/Desktop/emulsion-analysis-main/settings/fitting_config.toml")

parent_folder = config['parent_folder']
a = config['a']
b = config['b']
c = config['c']
abc_list = [a, b, c]
epsilon = config['epsilon']
guess_type = config['dense_radius_guess_type']

start = time.time()
all_images(parent_folder, abc_list, epsilon, guess_type)
end = time.time()
print(f"Analysis completed in: {round(end-start, 3) / 60} minutes")

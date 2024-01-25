import re

def get_cap_number(filename):
    # Define the regex pattern
    pattern = re.compile(r'(?:cap|Cap)\s*(\d+)', re.IGNORECASE)

    # Search for the pattern in the filename
    match = re.search(pattern, filename)

    # If a match is found, return the extracted number, otherwise return None
    return int(match.group(1)) if match else None

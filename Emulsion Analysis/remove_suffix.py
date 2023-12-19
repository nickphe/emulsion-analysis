
def remove_suffix(input_string, suffix: str):
    if input_string.endswith(suffix):
        result_string = input_string[:-4]
        return result_string
    else:
        return input_string
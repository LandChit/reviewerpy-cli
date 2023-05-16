import os

# VARS
file_end = ".json"
version = "0.0.3"
saves_folder = "./saves"

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def list_saves(path:str) -> list:
    return [item for item in os.listdir(path)\
        if os.path.isfile(f"{path}/{item}") and item.endswith(f"{file_end}")]
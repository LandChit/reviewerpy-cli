import os

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def list_saves(path:str, file_type:str) -> list:
    if not os.path.exists(path):
        os.makedirs(path)
    listdir = os.listdir(path)
    listdir.sort()
    files = []
    for file in listdir:
        if not os.path.isfile(f"{path}/{file}"):
            continue
        if file.split(".", -1)[-1].lower() == file_type.lower():
            files.append(file)
    
    return files

def time_convert(time_s):
    mins = int(int(time_s) / 60)
    secs = int(time_s) % 60
    
    return f"{mins}:{secs:02d}"
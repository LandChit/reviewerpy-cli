#!/usr/bin/env python3

from time import time
from sys import argv
from json import dump


def readfile(path) -> list[str]:
    return open(path, "r").readlines()


def cleanup(strlist: list[str]) -> list[str]:
    final: list[str] = []
    for line in strlist:
        if line.startswith("#"):
            continue
        if line.startswith("\n"):
            continue
        line = line.replace("\n", "")
        final.append(line)

    return final


def convertion(strlist: list[str]) -> dict:
    data = {}
    enummode: bool = False
    key: str = ""
    value = ""

    for line in strlist:
        if not line.startswith('-'):
            # ENUMERATION SAVE
            if enummode == True:
                data[key] = value
                enummode = False

            line = line.split('=')
            key, value = line
            data[value.strip()] = key.strip()

        else:
            # ENUMERATION
            if line.startswith('--'):
                if enummode == True:  # SAVE ENUMERATION IF NEW ENUMERATION STARTED
                    data[key] = value
                enummode = True
                key = line.removeprefix('--').strip()
                value = []
            else:
                # leave the error be lol its fine
                value.append(line.removeprefix('-').strip())

        if type(value) == list:
            data[key] = value

    return data


if __name__ == "__main__":
    try:
        path = argv[1]
    except:
        path = input("file path: ")
        if path == "":
            print("ERROR: No Path was given")
            exit()

    try:
        if argv[2].endswith(".py"):
            print("ERROR: Using the default path because an invalid name was used")
            raise NameError
        if argv[2].endswith(".exe"):
            print("ERROR: Using the default path because an invalid name was used")
            raise NameError
        if argv[1] == argv[2]:
            print("ERROR: You cannot use the the file being translated as the output path. using the default path because an invalid name was used")
            raise NameError

        outputpath = open(argv[2], "w+")
        foutput = argv[2]
    except:
        output = path.split("/")
        output = output[-1].split(".")
        output.pop(-1)
        foutput = ""
        for s in output:
            foutput += s
        foutput += ".json"
        if foutput.split(".")[0] != "":
            outputpath = open(f"./notes/{foutput}", "w+")
            foutput = f"./notes/{foutput}"
        else:
            outputpath = open("")

    starttime = time()
    try:
        file = readfile(path)
    except FileNotFoundError:
        print("ERROR: Invalid file\nsuggestion: try check the spelling or try using its full path? with the file extension")
        exit()
    file = cleanup(file)

    dump(convertion(file), outputpath, indent=2)

    print('file outputted at:', foutput)
    print("generation time:", str(round(time()*1000-starttime*1000))+'ms')

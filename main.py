import tools
import os
import json
import datetime
import time
import pickle
from termcolor import colored
from random import shuffle as rshuffle


class Reviewer():
    def __init__(self, path) -> None:
        self.path = path

    def load(self) -> dict:
        return json.load(open("./notes/"+self.path))

    def shuffledkeys(self, dict: dict = None) -> list[str]:
        if dict == None:
            dict = self.load()
        keys = [key for key in dict]
        rshuffle(keys)
        return keys


def start():
    totalquestions = 0
    correctans = 0
    wrongans = ""
    wrongansG = []
    wrongansE = []

    data = app.load()
    start_time = time.time()
    for key in app.shuffledkeys():
        etype = type(data[key])
        if etype == str:
            answer = input(f"{key}\n: ").lower()
            if answer == data[key]:
                print("[/]")
                correctans += 1
            else:
                print("[X]")
                wrongans += f"{colored(data[key], 'green')}: {key}\n{colored('you answered:', 'grey')} {colored(answer, 'red')}\n"

            totalquestions += 1

        elif etype == dict:
            shuffled = app.shuffledkeys(data[key])
            print(f"0-{key}-0")
            _wrongans = []
            for q in shuffled:
                answer = input(f"{q}\n: ").lower()
                if answer == data[key][q].lower():
                    print("[/]")
                    correctans += 1
                else:
                    print("[X]")
                    _wrongans.append(
                        f"{colored(data[key][q], 'green')}: {q}\n{colored('you answered:', 'grey')} {colored(answer, 'red')}")

                totalquestions += 1

            if _wrongans != []:
                wrongansG.append([key, _wrongans])

            print("-END GROUP-")

        elif etype == list:
            enum: list = [str(q).lower() for q in data[key]]
            items = len(enum)
            print(f"-{key}-",f"{len(enum)} items")
            for q in range(items):
                answer = input("- ").lower()
                if answer in enum:
                    enum.remove(answer)
                    print("[/]")
                    correctans += 1
                else:
                    print("[X]")

                totalquestions += 1

            if enum != []:
                wrongansE.append([key, enum])
    endtime = time.time()

    wrongans += colored("\nGROUPED: ", "magenta")
    for q in wrongansG:
        wrongans += f"\n\n--{q[0]}--"
        for i in q[1]:
            wrongans += f"\n- {i}"

    wrongans += colored("\nENUMERATED: ", "magenta")
    for q in wrongansE:
        wrongans += f"\n--{q[0]}--\n{colored('you forgot about:', 'grey')}"
        for i in q[1]:
            wrongans += f"\n- {colored(i, 'red')}"

    print(colored(
        f"SCORE {correctans}/{totalquestions}, time: {datetime.timedelta(seconds=round(endtime-start_time))}\nWRONG ANSWERS:", "magenta"))
    print(wrongans)
    
    with open('./_last.pkl', 'wb') as f:
        pickle.dump(wrongans, f)
    
    input("Enter to continue: ")


def translate(path:str, name:str):
    file = tools.Translate(path)
    try:
        dictf = file.convert_todict(file.readbyline())
    except FileNotFoundError:
        print("ERROR: File not found")
        return
    with open(f"./notes/{name}.json", "w+") as f:
        json.dump(dictf,f, indent=2)
    

def listnotes():
    return os.listdir("./notes")

def clearscreen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
        
    print("""
    REVIEWERPY | REVIEWERPY | REVIEWERPY
    REVIEWERPY | REVIEWERPY | REVIEWERPY      
    REVIEWERPY | REVIEWERPY | REVIEWERPY        
    by: @LandChit                                   
    """)


while True:
    clearscreen()
    
    try:
        with open("./_last.pkl", "rb") as f:
            last_session = pickle.load(f)
    except FileNotFoundError:
        last_session = "No Session Found"

    try:
        print("What note should we start\nT: to translate your textfile ")
        pos = 1
        print("0: LAST SESSION WRONG ANSWERS")
        for note in listnotes():
            print(f"{pos}: {note[:-5]}")
            pos += 1

        pick = input("input(leave blank to cancel): ")
        if pick.lower() == "t":
            clearscreen()
            print("------TRANSLATE MODE------")
            filepath = input("path: ")
            savename = input("note name: ")
            translate(filepath, savename)
            input("Press enter to go back")
        if pick == "0":
            print(last_session)
            input("Press enter to go back")
            raise ValueError 
        
        if type(int(pick)) == int:
            app = Reviewer(listnotes()[int(pick)-1])
            start()
            
        
        
    except ValueError:
        pass
    except IndexError:
        pass

    

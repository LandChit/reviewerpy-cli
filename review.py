import os
import json
import pickle
import time
import datetime
from termcolor import colored
from random import shuffle as rshuffle


def listnotes():
    notes = os.listdir("./notes")
    try:
        notes.remove("./notes/lastsession.temp")
    except:
        pass
    return notes


def load():
    return json.load(open("./notes/"+filename))


def shuffledkeys():
    keys = [key for key in load()]
    rshuffle(keys)
    return keys


def start():
    total = 0
    correctans = 0
    wrongans = ""
    wrongansE = []

    starttime = time.time()
    for question in shuffledkeys():
        file = load()
        wtype = type(file[question])
        if wtype is str:  # basic functionality
            answer = input(f"{question}: ")
            if answer.lower() == load()[question].lower():
                correctans += 1
                print("[/]")
            else:
                wrongans += f"{colored(file[question], 'green')}: {question}\n{colored('you answered:', 'grey')} {colored(answer, 'red')}\n"
                print("[x]")

            total += 1

        elif wtype is list:  # enumeration mode
            tempwrong = []
            enum: list = [str(q).lower() for q in load()[question]]
            print(question)
            for item in range(len(enum)):
                answer = input("-").lower()
                if answer in enum:
                    correctans += 1
                    enum.remove(answer)
                    print("[/]")
                else:
                    print("[x]")

                total += 1

            if not enum == []:
                wrongansE.append([question, enum])
    endtime = time.time()

    wrongans += colored("\nENUMERATED: ", "magenta")
    for q in wrongansE:
        wrongans += f"\n{q[0]}\n{colored('you forgot about:', 'grey')}"
        for i in q[1]:
            wrongans += f"\n- {colored(i, 'red')}"

    print(colored(
        f"SCORE {correctans}/{total}, time: {datetime.timedelta(seconds=round(endtime-starttime))}\nWRONG ANSWERS:", "magenta"))
    print(wrongans)

    with open('./notes/lastsession.temp', 'wb') as f:
        pickle.dump(wrongans, f)

    input("press enter to continue")


filename = ""


def clearscreen():
    os.system("cls")
    print("""
    REVIEWERPY | REVIEWERPY | REVIEWERPY
    REVIEWERPY | REVIEWERPY | REVIEWERPY      
    REVIEWERPY | REVIEWERPY | REVIEWERPY        
    by: @LandChit                                   
    """)


while True:
    clearscreen()

    try:
        with open("./notes/lastsession.temp", "rb") as f:
            last_session = pickle.load(f)
    except FileNotFoundError:
        last_session = "No Session Found"

    try:
        print("What note should we start")
        pos = 1
        print("0: LAST SESSION WRONG ANSWERS")
        for note in listnotes():
            print(f"{pos}: {note[:-5]}")
            pos += 1

        pick = int(input("input(leave blank to cancel): "))
        if pick == "":
            pass
        elif pick == 0:
            print(last_session)
            input("Press enter to go back")
            raise ValueError

        filename = listnotes()[pick-1]
        start()
    except ValueError:
        pass
    except IndexError:
        pass

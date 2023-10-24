import reviewer as rr
from reviewer import translator as translator
from termcolor import colored
import random
import json
import pickle




def title():
    rr.clear_screen()
    print("█▀▀▄ █▀▀ ▐▌ ▐▌ ▀ █▀▀ █   █ █▀▀ █▀▀▄", end="")
    print(colored("   █▀▄ ▀▄▄▀", "green"))
    print("█▐█▀ █▀▀  ▀▄▀  █ █▀▀ █ █ █ █▀▀ █▐█▀", end="")
    print(colored("   █▀    █", "green"))
    print("▀ ▀▀ ▀▀▀   ▀   ▀ ▀▀▀  ▀ ▀  ▀▀▀ ▀ ▀▀", end="")
    print(colored("   ▀    ▀ ", "green"))
    print(colored("-----------By:@LandChit------------", on_color="on_green") +
          f"   V{rr.version}")


def translate(path: str):
    translation = translator.Translate(path)
    s = path.split("/")[-1]
    s = s.split("\\")[-1].split(".")
    s.pop(-1)

    f = open(f"{rr.saves_folder}/{'.'.join([str(w) for w in s])}{rr.file_end}", "w+")

    json.dump(translation.convert(), f, indent=4)


def start(path: str):
    title()
    print("path: ", path)
    save = json.load(open(path))
    keys:list[str] = [ge for ge in save]
    random.shuffle(keys)
    total = 0
    points = 0
    
    wrong_group = []
    wrong_enum = []
    
    for key in keys:
        print(colored(key.replace(translator.zero_width_space, "").replace(r";\n", "\n"), attrs=["underline"]))
        questions = save[key]
        
        if type(questions) is dict:
            wrong = []
            if key.startswith(translator.zero_width_space):
                for question in questions:
                    _question = question.replace(r";\n", "\n")
                    answer:str = input(f"{_question}\n:")
                    
                    
                    if answer.strip().lower() == questions[question].lower():
                        points += 1
                        print(colored("[/]", color="green"))
                    else:
                        wrong.append([questions[question], question.replace(r";\n", "\n"), answer]) # type: ignore
                        print(colored("[X]", color="red"))
                    
                    total += 1
                
                    
            else:
                shuffled_questions = [q for q in questions]
                random.shuffle(shuffled_questions)
                
                for question in shuffled_questions:
                    _question = question.replace(r";\n", "\n")
                    answer:str = input(f"{_question}\n:")
                    
                    
                    if answer.strip().lower() == questions[question].lower():
                        points += 1
                        print(colored("[/]", color="green"))
                    else:
                        wrong.append([questions[question], question.replace(r";\n", "\n"), answer]) # type: ignore
                        print(colored("[X]", color="red"))
                    
                    total += 1
                    
            if wrong != []:
                wrong_group.append([key.replace(translator.zero_width_space, "").replace(r";\n", "\n"), wrong])            
        
        
        elif type(questions) is list:
            questions = [q.strip().lower() for q in questions]
            
            if key.startswith(translator.zero_width_space):
                count = 1
                wrong:list[str] = []
                for __ in range(len(questions)):
                    _answer = input(f"{count} - ")
                    if _answer.strip().lower() == questions[0]:
                        points += 1
                        print(colored("[/]", color="green"))
                    else:
                        wrong.append(questions[0])
                        print(colored("[X]", color="red"))    
                    questions.pop(0)
                    count += 1
                    total += 1
                
                if wrong != []:
                    wrong_enum.append([key.replace(translator.zero_width_space, "").replace(r";\n", "\n"),wrong])
            
            else:
                for __ in range(len(questions)):
                    _answer = input("- ")
                    if _answer.strip().lower() in questions:
                        points += 1
                        questions.remove(_answer.lower().strip())
                        print(colored("[/]", color="green"))
                    else:
                        print(colored("[X]", color="red"))
                    
                    total += 1
                
                if questions != []:
                    wrong_enum.append([key.replace(r";\n", "\n"), questions])    
    
    wg = ""
    for w in wrong_group:
        wg += colored("\n" + w[0] + "\n", attrs=["underline"])
        for ww in w[1]:
            wg += f"{colored(ww[0], 'green')}: {ww[1]}\n: {colored(ww[2], 'red')}\n"
    
    we = ""
    for w in wrong_enum:
        we += colored("\n" + w[0] + "\n", attrs=["underline"])
        for ww in w[1]:
            we += f"- {colored(ww, 'red')}\n"
    
    wronganswers = f"""
WRONG ANSWERS {points}/{total}
-----GROUPED-----
    {wg}
    
----ENUMERATED----
    {we}
    """
    print(wronganswers)
    pickle.dump(f"path: {path}{wronganswers}", open("./.lastattempt", "wb"))
    input()


if __name__ == "__main__":
    error = ""
    while True:
        title()

        print(colored("\nT: Translate your reviewer | L: Show your last attempt",
                      "magenta", attrs=["underline"]))

        print("\n::YOUR SAVES::")
        temp = 0

        for saves in rr.list_saves(rr.saves_folder):
            print(f"{temp}: {saves[:-5]}")
            temp += 1
        if error != "":
            print(colored(f"ERROR {error}", on_color="on_red"), end="")
        selection = input("\ninput: ")

        if selection.lower() == "t":
            title()
            path = input("\ninput file path:")
            try:
                translate(path)
                input("\nyour save file has been translated press enter to continue")
                error = ""
            except FileNotFoundError:
                error = "<TRANSLATOR> that path does not exist"

        elif selection.lower() == "l":
            title()
            try:
                print(":::::LAST ATTEMPT::::")
                print(pickle.load(open("./.lastattempt", "rb")))
                input()
                error = ""
            except FileNotFoundError:
                error = "<LAST ATTEMPT> you dont have any"
            
            
        else:
            try:
                start(
                    f"{rr.saves_folder}/{rr.list_saves(rr.saves_folder)[int(selection)]}")
                error = ""
            except IndexError:
                error = "<MAIN> there is no such save file in that index"
            except ValueError as e:
                
                error = f"<MAIN> invalid input {e}"

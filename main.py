#pylint:disable=W0106
import reviewer as rp
from reviewer.reviewer import Reviewer
from reviewer import translator

import json
import pickle
import time
from yaml import safe_load

rpy_conf = safe_load(open("rpy.yml"))
config = safe_load(open("config.yml"))


_ONGREEN = '\x1B[42m'
_ONGREY = '\x1B[47m'
_YELLOW = '\x1B[33m'
_GREEN = '\x1B[32m'
_RED = '\x1B[31m'
_GREY = '\x1B[30m'
_END = '\x1B[0m'

_UNDERLINE = '\033[4m'
_END2 = '\033[0m'

def title():
    rp.clear_screen()
    print("█▀▀▄ █▀▀ ▐▌ ▐▌ ▀ █▀▀ █   █ █▀▀ █▀▀▄", end="")
    print(f"{_GREEN}   █▀▄ ▀▄▄▀{_END}")
    print("█▐█▀ █▀▀  ▀▄▀  █ █▀▀ █ █ █ █▀▀ █▐█▀", end="")
    print(f"{_GREEN}   █▀    █{_END}")
    print("▀ ▀▀ ▀▀▀   ▀   ▀ ▀▀▀  ▀ ▀  ▀▀▀ ▀ ▀▀", end="")
    print(f"{_GREEN}   ▀    ▀ {_END}")
    print(f"{_ONGREEN}------------By:@LandChit------------{_END}" +
          f"   V{rpy_conf['version']}")

def save_file(save:dict, name:str):
    if config["pickled_save"]:
        file_type = ".rps"
        mode = "ab"
    else:
        file_type = ".json"
        mode = "w+"
    file = open(f"{config['save_dir']}/{name+file_type}", mode)
    json.dump(save, file, indent=4) if mode == "w+" else pickle.dump(save, file)

def translate_errors_format(warnings, errors):
    final = ""
    
    if warnings != []: final += f'\n{_YELLOW}[WARNINGS]{_END}'
    for i in warnings:
        final += f'\n{_YELLOW}WARNING: {_END}'+ i.as_string()
        
    if errors != []: final += f'\n{_RED}[ERRORS]{_END}'
    for i in errors:

        final += f'\n{_RED}ERROR: {_END}'+ i.as_string()
        
    if warnings == [] and errors == []:
        final += f"\n{_GREEN}TRANSLATED WITHOUT ANY ERRORS{_END}"
        
    return final

def translate():
    print(f"\n{_UNDERLINE}ID   NAME{'‎ '*10}{_END2}")
    tsaves:list[str] = rp.list_saves(config["text_dir"], config["text_type"])
    count = 0
    for tsave in tsaves:
        print(f"{count:03d} |", tsave.split(".", -1)[0])
        count += 1
    text_id = input("\nID of the text: ")
    try:
        
        text_id = int(text_id)
        
        title()
        f = open(config["text_dir"]+"/"+tsaves[text_id], errors='ignore').read()
        translated, warn, error = translator.Translate(f).transformed()
        
        print(translate_errors_format(warn, error))
        
        tsave_name = input("Save name (Uses text name if blank): ")
        if tsave_name == "":
            tsave_name = tsaves[text_id].split(".", -1)[0]
        
        save_file(translated, tsave_name)
    except ValueError :
        title()
        print(f"\n{_RED}FAILED: NOT AN INTEGER{_END}")
    except IndexError:
        title()
        print(f"\n{_RED}FAILED: INDEX OUT OF RANGE{_END}")
    
    input("\nPress Enter to Continue")

def last_runs():
    count = 0
    cache = open('./reviewer/cache.json', "r")
    content = json.load(cache)
    delete = False
    
    runs = [run for run in content["last_runs"].keys()]
    print(f"\n{_UNDERLINE}ID   NAME{'‎ '*10}{_END2}")
    print("d+[Id of save] To delete last runs; ex. d01")
    
    for run in runs:
        print(f"{count:03d} |", run)
        count += 1
    
    run_id = input("\nID of save: ")
    
    if run_id.startswith('d') or run_id.startswith('D'):
        delete = True
        
    try:
        run_id = run_id.removeprefix('d')
        run_id = run_id.removeprefix('D')
        run_id = run_id.strip()

        run_id = int(run_id)
        
        title()
        if not delete:
            print(content["last_runs"][runs[run_id]])
            input()
            return
        
        
        del content["last_runs"][runs[run_id]]
        print(content)
        # TODO: WONT DUMP 
        # json.dump(open('./reviewer/cache.json', "w"), cache, indent=4)
        
        
    except ValueError:
        title()
        print(f"\n{_RED}FAILED: NOT AN INTEGER{_END}")
    except IndexError:
        title()
        print(f"\n{_RED}FAILED: INDEX OUT OF RANGE{_END}")
    
    input()

def wrong_answer_format(wrong_e, wrong_oe, wrong_g):
    state = ""
    wrong_answers = ""
    
    if (wrong_e + wrong_oe + wrong_g) != []:
        state = f"\n{_RED}-------WRONG ANSWERS-------{_END}"
    else: state = f'\n{_GREEN}CONGRATS YOU GOT A PERFECT SCORE{_END}'

    for w in wrong_g:
        wrong_answers += f'{_ONGREY}GROUP{_END} {w[0]}\n'
        for i in w[1]:
            wrong_answers += f"{_GREEN}{i[1]}{_END}: {i[0]}\n"
            wrong_answers += f" :{_RED}{i[2]}{_END}\n"
    
    for w in wrong_e:
        wrong_answers += f'{_ONGREY}ENUM{_END} {w[0]}\n'
        for i in w[1]:
            wrong_answers += f"- {_RED}{i}{_END}\n"
    
    for w in wrong_oe:
        wrong_answers += f'{_ONGREY}OENUM{_END} {w[0]}\n'
        for i in w[1]:
            wrong_answers += f'{i[0]:03d}| {_RED}{i[1]}{_END}\n'
    
    return state, wrong_answers

def main_menu():
    last = ""
    
    while True:
        title()
        print("T: Translate a text file | L: Last Session")
        
        print(f"\n{_UNDERLINE}ID   NAME{'‎ '*10}{_END2}")
        file_type = "rps" if config["pickled_save"] else "json"
        mode = "rb" if config["pickled_save"] else "r"
        saves:list[str] = rp.list_saves(config["save_dir"], file_type)
        count = 0
        for save in saves:
            print(f"{count:03d} |", save.split(".", -1)[0])
            count += 1
        inp = input("\ninput: ")
        
        try:
            pointer = int(inp)
            title()
            content = open(f"{config['save_dir']}/{saves[pointer]}", mode)
            content = json.load(content) if mode == "r" else pickle.load(content)
            
            review = Reviewer(content)
            start_time = time.time()
            wrong_e, wrong_oe, wrong_g = review.start()
            end_time = time.time()
            answer_time = end_time - start_time
            
            state, formated = wrong_answer_format(wrong_e, wrong_oe, wrong_g)
            stats = f"""\n{_UNDERLINE}TIME(m:s): {rp.time_convert(answer_time)}\
                | SCORE: {review.correct_items}/{review.item_count}{_END2}\
            \n{state}\
            \n{formated}\
            """
            print(stats)
            input("press enter to continue")

        except ValueError:
            title()
            if inp.strip().upper() == "T":
                translate()
            elif inp.strip().upper() == "L":
                last_runs()
        except IndexError:
            ...

        
 
if __name__ == "__main__":
    # app = Reviewer()
    # app.start()
    
    main_menu()
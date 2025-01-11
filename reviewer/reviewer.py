
from reviewer.decorator import Decorator

from random import shuffle
import json

_HIGHLIGHT = '\x1B[47m'
_END = '\x1B[0m'
_GREY = '\x1B[30m'
_RED = '\x1B[31m'


class Reviewer():
    def __init__(self, dict:dict, shuffle_groups:bool = True) -> None:
        self.save = dict
        self.group_keys = [i for i in dict.keys()]
        if shuffle_groups: shuffle(self.group_keys)
        self.pos = -1
        self.mode:int
        self.items = None
        self.keys = None
        self.wrong_group = []
        self.wrong_enum = []
        self.wrong_oenum = []
        self.item_count = 0
        self.correct_items = 0
        self.next_group()
    
    def next_group(self):
        self.pos += 1
        self.current_group_key = self.group_keys[self.pos] if self.pos < len(self.group_keys) else False
        self.current_group = self.save[self.current_group_key] if self.current_group_key != False else None
            
        
        
    def start(self):
        while self.current_group is not None:
            try:
                self.mode = self.current_group['mode']
            except KeyError:
                error = f"{_RED}CORRUPTED GROUP: {_END}" + self.current_group_key
                error += f'{_GREY} (SKIPPING){_END}'
                print(error)
                self.next_group()
            
            if self.mode == 0:
                print(f'{_HIGHLIGHT}G {self.pos: 3d} {_END}', Decorator(self.current_group_key).decorated())
                self.items = self.current_group['items']
                temp = self.current_group['items'].keys()
                temp = [key for key in temp]
                shuffle(temp)
                self.keys = temp
                _wrong = self.ask()
                if _wrong[1] != []:
                    self.wrong_group.append(_wrong)
                
                
            elif self.mode == 1 or self.mode == 2:
                m = f'{_HIGHLIGHT}E ' if self.mode == 1 else f'{_HIGHLIGHT}OE' 
                print(f'{m}{self.pos: 3d} {_END}', Decorator(self.current_group_key).decorated())
                
                self.items = self.current_group['items']
                self.keys = True
                _wrong = self.ask()
                
                if _wrong[1] != []:
                    self.wrong_enum.append(_wrong) if self.mode == 1 else self.wrong_oenum.append(_wrong)
                
        
        return self.wrong_enum, self.wrong_oenum, self.wrong_group

    def ask(self):
        wrong = [self.current_group_key, []]
        
        
        while self.keys != []:
            if self.mode == 0:
                key = self.keys.pop(0)
                print(Decorator(key).decorated())
                answer = input(': ')
                if answer.lower().strip() != self.items[key].lower().strip():
                    wrong[1].append([Decorator(key).decorated(), self.items[key], answer])
                else: self.correct_items += 1
                
                self.item_count += 1
                
            elif self.mode == 1:
                items:list[str] = self.items.copy()
                
                for _ in self.items:
                    answer = input(': ')
                    try:
                        items.remove(answer.strip().lower())
                        self.correct_items += 1
                    except ValueError:
                        pass
                    self.item_count += 1
                
                wrong[1] += items
                self.keys = []
                
            elif self.mode == 2:
                _wrong = []
                count = 0
                for i in self.items:
                    count += 1
                    answer = input(f'{count:03d}: ')
                    if answer.strip().lower() != i:
                        _wrong.append([count, i])
                    else: self.correct_items += 1
                    
                    self.item_count += 1
                wrong[1] += _wrong
                self.keys = []
        
        self.next_group()
        
        return wrong 
                
        
        
# FOR TESTING
if __name__ == "__main__":
    review = Reviewer(json.load(open('./reviewer/test.json')))
    we, wg = review.start()
    print(we, wg)

    
        
        
        

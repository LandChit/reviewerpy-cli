from reviewer import errors as ers

ZWIDTH_SPACE = "​"

GROUP = 0
ENUMERATION = 1
ORDERED_ENUMERATION = 2


class Translate:
    def __init__(self, string: str) -> None:
        self.strings = string.splitlines()
        self.pos = -1
        self.current_line = None
        self.mode: int = None
        self.mode_name = ""
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_line = self.strings[self.pos] if self.pos < len(self.strings) else None
    
    def transformed(self):
        """Generates a json dictionary

        Returns:
            dict: json dictionary,
            list: warnings,
            list: errors,
        """        
        final = {}
        warnings = []
        errors = []
        
        while self.current_line is not None:
            print(self.current_line) if self.current_line.startswith('@') else ...
            if self.current_line == '' or self.current_line.startswith('#'):
                self.advance()
                
            elif self.current_line.startswith("@g"):
                self.mode = GROUP
                self.mode_name = self.current_line[2:].strip()
                self.advance()
            elif self.current_line.startswith("@e"):
                self.mode = ENUMERATION
                self.mode_name = self.current_line[2:].strip()
                self.advance()
            elif self.current_line.startswith("@oe"):
                self.mode = ORDERED_ENUMERATION
                self.mode_name = self.current_line[3:].strip()
                self.advance()
            elif self.current_line.startswith("@ "):
                # TODO: ADD A SYSTEM WHERE IT SKIPS THE FIRST UNDEFINED GROUP INITIATOR "@ "
                print(f"\"@ \" detected in line: {self.pos}")
                self.advance()
            else:
                if not self.mode: self.mode = 0
                _items, _warnings, _errors = self.make_item()
                
                final[self.mode_name] = _items
                warnings += _warnings
                errors += _errors

                
                
        return final, warnings, errors

    def make_item(self):
        warnings = []
        errors = []
        
        temp = {
                'mode':self.mode,
                'items': {} if self.mode == GROUP else []
                }
        
        while self.current_line is not None and not self.current_line.startswith('@'):
            
            if self.current_line == '' or self.current_line.startswith('#'):
                pass
            elif self.mode == GROUP:
                if ":" in self.current_line:
                    answer, question = self.current_line.split(':', 1)
                    temp["items"][question.strip()] = answer.strip()
                else:
                    errors.append(ers.ColumnNotFound(self.pos, self.current_line, 'Column not found skipping'))
                    
            elif self.mode == ENUMERATION or self.mode == ORDERED_ENUMERATION:
                if ":" in self.current_line:
                    warnings.append(ers.UnidentifiedGroup(self.pos, self.current_line, 'Potential unidentified group in enumeration'))
                temp["items"].append(self.current_line.strip().lower())
            self.advance()
        
        return temp, warnings, errors


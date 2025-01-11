import string

## CONSTANTS
STRIKE = 0
BOLD = 1
HIGHLIGHT = 2
UNDERLINE = 3

chars:str = string.printable
for symbol in ['-', '*', '=', '_']:
    chars = chars.replace(str(symbol), '')
CHARACTERS = chars



class DecoratorLexer:
    def __init__(self, text) -> None:
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()
        
    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
        self.next_char = self.text[self.pos + 1] if self.pos + 1 < len(self.text) else '❌' #any placeholder
        
    def make_tokens(self) -> list:
        tokens = []
        
        while self.current_char is not None:
            if self.current_char in '\t':
                self.advance()
            elif self.current_char in CHARACTERS:
                tokens.append(self.make_text())
                
            elif self.current_char in '-' and self.next_char in '-':
                tokens.append(STRIKE)
                self.advance();self.advance()
                
            elif self.current_char in '*' and self.next_char in '*':
                tokens.append(BOLD)
                self.advance();self.advance()
                
            elif self.current_char in '=' and self.next_char in '=':
                tokens.append(HIGHLIGHT)
                self.advance();self.advance()
                
            elif self.current_char in '_' and self.next_char in '_':
                tokens.append(UNDERLINE)
                self.advance();self.advance()
            else:
                tokens.append(self.current_char)
                self.advance()
                
        return tokens
    
    def make_text(self) -> str:
        text:str = ''
        
        while self.current_char is not None and self.current_char in CHARACTERS + ' \'\"':
            text += self.current_char
                
            self.advance()
                
        return text


class Decorator:
    def __init__(self, text:str) -> None:
        self.tokens = DecoratorLexer(text).make_tokens()
        self.pos = -1
        self.token = None
        self.advance()
        
    def advance(self):
        self.pos += 1
        self.token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        self.next_token = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
        self.next_next_token = self.tokens[self.pos + 2] if self.pos + 2 < len(self.tokens) else None
    
    def decorated(self) -> str:
        text:str = ''
        
        while self.token is not None:
            if type(self.token) == str:
                text += self.token
                self.advance()
            elif self.token == STRIKE:
                text += self.to_decorate(STRIKE)
            elif self.token == BOLD:
                text += self.to_decorate(BOLD)
            elif self.token == HIGHLIGHT:
                text += self.to_decorate(HIGHLIGHT)
            elif self.token == UNDERLINE:
                text += self.to_decorate(UNDERLINE)
            else:
                self.advance()
        return text
                
    def to_decorate(self, _type) -> str:
        _BOLD = '\033[1m'
        _UNDERLINE = '\033[4m'
        _END = '\033[0m'
        
        _HIGHLIGHT = '[43m'
        _END2 = '[0m'
        
        text:str = ''

        
        if type(self.next_token) == str and self.next_next_token == _type: # Checks if closed
            match _type:
                case 0:
                    text += ''.join(['\u0336' + char for char in self.next_token])
                case 1:
                    text += _BOLD + self.next_token + _END
                case 2:
                    text += _HIGHLIGHT + self.next_token + _END2
                case 3:
                    text += _UNDERLINE + self.next_token + _END
            self.advance(); self.advance()
        else:
            match _type:
                case 0:
                    text += '--'
                case 1:
                    text += '**'
                case 2:
                    text += '=='
                case 3:
                    text += '__'
        self.advance()
                
        return text
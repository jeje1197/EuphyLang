import string

from .token import *
from .position import Position
from .exception import ParseException

WHITESPACE = ['\n', '\t', '\r', ' ']
DIGITS = '0123456789'
DIGITS_AND_DECIMAL = DIGITS + '.'
BEGIN_SYMBOL_CHARACTERS = string.ascii_letters + '_'
SYMBOL_CHARACTERS = string.ascii_letters + '_' + string.digits

KEYWORDS = [
    'boolean', 'number', 'string', 'dynamic', 'function', 'list', 'table',

    'print', 
    
    'if', 'else', 'for', 'while', 'break', 'continue',

    'return',

    'true', 'false', 'print',

    'class'
]
TWO_CHAR_OPERATORS = ['<=', '>=', '==', '!=', '&&', '||']
SINGLE_CHAR_OPERATORS = ['+', '-', '*', '/', '%', '<', '>', '=', '.']
SEPARATORS = [',', ':', ';', '(', ')', '{', '}', '[', ']']

ESCAPE_CHARS = {
    'n': '\n',
    't': '\t',
    'r': '\r',
    '\\': '\\'
}

class Lexer:
    def __init__(self, file_name, code) -> None:
        self.code = code
        self.position = Position(file_name)
        self.index = -1
        self.cur = None

        self.get_next()
        self.tokens = []

    def has_next(self, steps_ahead=1) -> bool:
        return self.index + steps_ahead < len(self.code)
    
    def get_next(self) -> str:
        if self.has_next():
            if self.cur == '\n': 
                self.position.advance()
            self.index += 1
            self.cur = self.code[self.index]
        else:
            self.cur = ''
        return self.cur
    
    def lookahead(self, steps_ahead=1) -> str:
        if self.has_next(steps_ahead):
            return self.code[self.index + steps_ahead]
        return ''
    
    def create_token(self, type, value=None) -> None:
        new_token = Token(type, value, self.position.copy())
        self.tokens.append(new_token)

    def generate_tokens(self) -> list[Token]:
        self.tokens = []

        while (self.cur):
            cur = self.cur
            next_two = self.cur + self.lookahead()

            if cur in WHITESPACE:
                self.get_next()
            elif next_two == '//': # Scan comments
                self.skip_comment()
            elif cur in DIGITS: # Scan number
                self.scan_number()
            elif cur == '"':    # Scan string
                self.scan_string() 
            elif cur in BEGIN_SYMBOL_CHARACTERS: 
                self.scan_keyword_or_identifier()
            elif cur in TWO_CHAR_OPERATORS:
                self.scan_two_char_operators()
            elif cur in SINGLE_CHAR_OPERATORS:
                self.scan_single_char_operator()
            elif cur in SEPARATORS:
                self.scan_separator()
            else:
                raise ParseException(f'Did not reach end of input at {self.position}')
        self.create_token(TOKEN_EOF)
        return self.tokens
                
    def skip_comment(self) -> None:
        while self.cur and self.cur != '\n':
            self.get_next()

    def scan_number(self) -> None:
        number_literal = ''
        decimal_count = 0
        while self.cur and self.cur in DIGITS_AND_DECIMAL:
            if self.cur == '.':
                if decimal_count == 1: break
                decimal_count += 1
            number_literal += self.cur
            self.get_next()
        print (self.cur)
        self.create_token(TOKEN_NUMBER, number_literal)

    def scan_string(self) -> None:
        self.get_next()
        string_literal = ''
        while self.cur and self.cur != '"':
            if self.cur == '\\' and self.lookahead() in ESCAPE_CHARS:
                string_literal += ESCAPE_CHARS[self.lookahead()]
                self.get_next()
                self.get_next()
            else:
                string_literal += self.cur
                self.get_next()
        
        if self.cur != '"':
            raise ParseException(f'Unterminated string literal at {self.position}')
        self.get_next()
        self.create_token(TOKEN_STRING, string_literal)

    def scan_keyword_or_identifier(self) -> None:
        symbol = ''
        while self.cur and self.cur in SYMBOL_CHARACTERS:
            symbol += self.cur
            self.get_next()
        if symbol in KEYWORDS:
            self.create_token(TOKEN_KEYWORD, symbol)
        else:
            self.create_token(TOKEN_IDENTIFIER, symbol)

    def scan_two_char_operators(self) -> None:
        self.create_token(TOKEN_OPERATOR, self.cur + self.lookahead())
        self.get_next()
        self.get_next()

    def scan_single_char_operator(self) -> None:
        self.create_token(TOKEN_OPERATOR, self.cur)
        self.get_next()

    def scan_separator(self) -> None:
        self.create_token(TOKEN_SEPARATOR, self.cur)
        self.get_next()

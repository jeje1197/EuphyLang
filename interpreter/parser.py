from .token import *
from .exception import ParseException
from .astnode import *

class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.index = -1
        self.cur = None

    def has_next(self, steps_ahead=1):
        return self.index + steps_ahead < len(self.tokens)
    
    def get_next(self):
        if self.has_next():
            self.index += 1
            self.cur = self.tokens[self.index]
        else:
            self.cur = None

    def match(self, type, value=None):
        if not self.cur: return False
        if not value: return self.cur.type == type
        return self.cur.type == type and self.cur.value == value

    def matchKeyword(self, value):
        if not self.cur: return False
        return self.cur.value == value

    def generate_ast(self):
        self.get_next()
        return self.statements()
    
    def statements(self):
        statement_list = []

        statement = self.statement()
        while statement:
            statement_list.append(statement)
            statement = self.statement()
        return statement_list
    
    def statement(self):
        if self.matchKeyword('print'):
            return self.print_statement()
        return None

    def print_statement(self) -> PrintNode:
        token = self.cur
        self.get_next()

        expr = self.expression()
        if not expr: raise ParseException(f'Expected expression at {token.position}')
        return PrintNode(expr).set_position(token.position)
    
    def expression(self):
        return self.atom()

    def atom(self):
        token = self.cur

        if self.match(TOKEN_NUMBER):
            self.get_next()
            return NumberNode(token.value).set_position(token.position)
        elif self.match(TOKEN_STRING):
            self.get_next()
            return StringNode(token.value).set_position(token.position)
        
        return None
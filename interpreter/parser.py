from .token import *
from .exception import ParseException
from .astnode import *

class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.index = -1
        self.cur = None

        self.get_next()

    def has_next(self, steps_ahead=1):
        return self.index + steps_ahead < len(self.tokens)
    
    def get_next(self):
        if self.has_next():
            self.index += 1
            self.cur = self.tokens[self.index]
        else:
            self.cur = None

    def lookahead(self, steps_ahead=1):
        if self.has_next(steps_ahead):
            return self.tokens[self.index + steps_ahead]
        return None

    def reverse(self, target_index):
        self.index = target_index - 1
        self.get_next()

    def match(self, type, value=None):
        if not self.cur: return False
        if not value: return self.cur.type == type
        return self.cur.type == type and self.cur.value == value
    
    def match_lookahead(self, steps_ahead=1, type=None, value=None):
        token = self.lookahead(steps_ahead)
        if not token: return False
        if not value: return token.type == type
        return token.type == type and token.value == value

    def matchKeyword(self, keyword):
        if not self.cur: return False
        return self.cur.type == TOKEN_KEYWORD and self.cur.value == keyword
    
    def matchKeywords(self, keywords):
        if not self.cur: return False
        return self.cur.type == TOKEN_KEYWORD and self.cur.value in keywords
    
    def matchOperator(self, operator):
        if not self.cur: return False
        return self.cur.type == TOKEN_OPERATOR and self.cur.value == operator

    def matchOperators(self, operators):
        if not self.cur: return False
        return self.cur.type == TOKEN_OPERATOR and self.cur.value in operators
    
    def matchSeparator(self, separator):
        if not self.cur: return False
        return self.cur.type == TOKEN_SEPARATOR and self.cur.value == separator
    
    def matchSeparators(self, separators):
        if not self.cur: return False
        return self.cur.type == TOKEN_SEPARATOR and self.cur.value in separators

    def generate_ast(self):
        statements = self.statements()
        if not self.match(TOKEN_EOF):
            raise ParseException(f'Did not reach end of file at {self.cur.position}')
        return statements
    
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
        elif self.matchSeparator('{'):
            return self.code_block()
        elif self.matchKeyword('if'):
            return self.if_statement()
        elif self.matchKeyword('while'):
            return self.while_loop()
        elif self.matchKeyword('break'):
            return self.break_statement()
        elif self.matchKeyword('continue'):
            return self.continue_statement()

        elif self.match(TOKEN_IDENTIFIER) and self.match_lookahead(1, TOKEN_OPERATOR, '='):
            return self.variable_assignment()
        
        revert_point = self.index
        data_type = self.parse_type()
        if data_type and self.match(TOKEN_IDENTIFIER):
            if self.match_lookahead(TOKEN_SEPARATOR, '('):
                return self.function_declaration()
            return self.variable_declaration(data_type)
        else:
            self.reverse(revert_point)
        return None
    
    def print_statement(self) -> PrintNode:
        token = self.cur
        self.get_next()

        expression = self.expression()
        if not expression: raise ParseException(f'Expected expression at {token.position}')
        return PrintNode(expression).set_position(token.position)
    
    def code_block(self):
        token = self.cur
        self.get_next()

        statements = self.statements()
        if not self.matchSeparator('}'):
            raise ParseException(f'Expected \'{"}"}\' at {token.position}')
        self.get_next()
        return CodeBlockNode(statements).set_position(token.position)
    
    def parse_type(self):
        data_type = ''

        if not (self.matchKeywords(['boolean', 'number', 'string', 'dynamic',
            'list', 'table']) or self.match(TOKEN_IDENTIFIER)):
            return ''
        data_type += self.cur.value
        self.get_next()
        return data_type
    
    def variable_declaration(self, data_type):
        if not self.match(TOKEN_IDENTIFIER):
            raise ParseException(f'Expected identifier after type at {self.cur.position}')
        identifier_token = self.cur
        self.get_next()

        expression = None
        if self.matchOperator('='):
            self.get_next()

            expression = self.expression()
            if not expression: raise ParseException(f'Expected expression at {self.cur.position}')
        return VariableDeclarationNode(data_type, identifier_token.value, expression).set_position(identifier_token.position)

    def variable_assignment(self):
        identifier_token = self.cur
        self.get_next()

        if not self.matchOperator('='):
            raise ParseException(f'Expected \'=\' after identifier at {identifier_token.position}')
        self.get_next()

        expression = self.expression()
        if not expression: raise ParseException(f'Expected expression at {self.cur.position}')
        return VariableAssignmentNode(identifier_token.value, expression).set_position(identifier_token.position)
    
    def if_statement(self):
        token = self.cur
        self.get_next()

        if not self.matchSeparator('('):
            raise ParseException(f'Expected \'(\' at {self.cur.position}')
        self.get_next()

        expression = self.expression()
        if not expression: raise ParseException(f'Expected condition expression at {self.cur.position}')

        if not self.matchSeparator(')'):
            raise ParseException(f'Expected \')\' at {self.cur.position}')
        self.get_next()

        true_statement = self.statement()
        if not true_statement: raise ParseException(f'Expected statement after if condition {self.cur.position}')

        else_statement = None
        if self.matchKeyword('else'):
            self.get_next()

            else_statement = self.statement()
            if not else_statement: raise ParseException(f'Expected statement after else {self.cur.position}')

        return IfNode(expression, true_statement, else_statement).set_position(token.position)

    def while_loop(self):
        token = self.cur
        self.get_next()

        if not self.matchSeparator('('):
            raise ParseException(f'Expected \'(\' at {self.cur.position}')
        self.get_next()

        expression = self.expression()
        if not expression: raise ParseException(f'Expected condition expression at {self.cur.position}')

        if not self.matchSeparator(')'):
            raise ParseException(f'Expected \')\' at {self.cur.position}')
        self.get_next()

        statement = self.statement()
        if not statement: raise ParseException(f'Expected statement after while condition {self.cur.position}')
        return WhileNode(expression, statement).set_position(token.position)

    def break_statement(self):
        token = self.cur
        self.get_next()
        return BreakNode().set_position(token.position)
    
    def continue_statement(self):
        token = self.cur
        self.get_next()
        return ContinueNode().set_position(token.position)
    
    def function_declaration(self, return_type):
        if not self.match(TOKEN_IDENTIFIER):
            raise ParseException(f'Expected identifier after type at {self.cur.position}')
        identifier_token = self.cur
        self.get_next()
    
    def expression(self):
        return self.logical()
    
    def logical(self):
        return self.binary_op(self.comparison, ['&&', '||'])
    
    def comparison(self):
        return self.binary_op(self.term, ['<', '>', '<=', '>=', '==', '!='])
    
    def term(self):
        return self.binary_op(self.factor, ['+', '-'])
    
    def factor(self):
        return self.binary_op(self.atom, ['*', '/', '%'])

    def atom(self):
        token = self.cur
        if self.matchOperators(['+', '-']):
            return self.unary_op()
        elif self.match(TOKEN_NUMBER):
            self.get_next()
            return NumberNode(token.value).set_position(token.position)
        elif self.match(TOKEN_STRING):
            self.get_next()
            return StringNode(token.value).set_position(token.position)
        elif self.matchKeywords(['true', 'false']):
            self.get_next()
            return BooleanNode(token.value).set_position(token.position)
        elif self.matchKeyword('none'):
            self.get_next()
            return NoneNode().set_position(token.position)
        elif self.match(TOKEN_IDENTIFIER):
            self.get_next()
            return VariableAccessNode(token.value).set_position(token.position)
        elif self.matchSeparator('('):
            self.parenthesized_expression()
        elif self.matchSeparator('[]'):
            self.list_expression()
        return None
    
    def unary_op(self):
        operator_token = self.cur
        self.get_next()
        atomNode = self.atom()
        if not atomNode:
            raise ParseException(f'Expected expression at {operator_token.position}')
        return UnaryOpNode(operator_token.value, atomNode).set_position(operator_token.position)
    
    def binary_op(self, function, operators):
        left_node = function()
        while left_node and self.matchOperators(operators):
            operator_token = self.cur
            self.get_next()

            right_node = function()
            if not right_node:
                raise ParseException(f'Expected expression at {operator_token.position}')
            left_node = BinaryOpNode(left_node, operator_token.value, right_node).set_position(left_node.position)
        return left_node
    
    def parenthesized_expression(self):
        token = self.cur
        self.get_next()

        expression = self.expression()
        if not expression:
            raise ParseException(f'Expected expression at {token.position}')
        if not self.matchSeparator(')'):
            raise ParseException(f'Expected \')\' at {self.cur.position}')
        self.get_next()
        return expression
    
    def list_expression(self):
        token = self.cur
        self.get_next()

        element_nodes = []
        expression = self.expression()
        if expression:
            element_nodes.append(element_nodes)

            while self.matchSeparator(',') and not self.matchSeparator(']'):
                self.get_next()

                expression = self.expression()
                if not expression:
                    raise ParseException(f'Expected expression at {token.position}')
                element_nodes.append(expression)
        
        if not self.matchSeparator(']'):
            raise ParseException(f'Expected \']\' at {token.position}')
        self.get_next()
        return ListNode(element_nodes).set_position(token.position)
    
    # def table_expression(self):
    #     token = self.cur
    #     self.get_next()

    #     element_nodes = []
    #     expression = self.expression()
    #     if expression:
    #         element_nodes.append(element_nodes)

    #         while self.matchSeparator(',') and not self.matchSeparator(']'):
    #             self.get_next()

    #             expression = self.expression()
    #             if not expression:
    #                 raise ParseException(f'Expected expression at {token.position}')
    #             element_nodes.append(expression)
        
    #     if not self.matchSeparator(']'):
    #         raise ParseException(f'Expected \']\' at {token.position}')
    #     self.get_next()
    #     return ListNode(element_nodes).set_position(token.position)
        
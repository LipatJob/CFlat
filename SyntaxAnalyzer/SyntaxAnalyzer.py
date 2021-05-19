from os import execlp
from Lib.Node import *
from Lib.Node import NodeType as NT

from Lib.Token import *
from Lib.Token import TokenType as TT
from typing import List
from Lib.ErrorHandler import *


def raise_syntax_error(expected, actual):
    raise_error(f"Syntax Error: expected {expected} got {actual}")


class SyntaxAnalyzer:
    def run(self, tokens: List[Token]) -> 'Node':
        self.tokens = tokens
        self.pointer = 0
        return self.expression(0)

    def current(self):
        return self.tokens[self.pointer]

    def next(self):
        if self.is_last():
            raise IndexError()
        self.pointer += 1

    def is_last(self):
        return self.pointer >= len(self.tokens)

    def expect(self, *expected_types):
        for expected in expected_types:
            if self.current().type == expected:
                self.next()
                return self.current()
        else:
            raise_error("or".join(expected_types), self.current().type)
    
    def is_type(self, *args):
        for arg in args:
            if self.current().type == arg:
                return True
        return False

    # <program>
    def program(self):
        # <block>
        return Node(NT.PROGRAM, self.block())

    # <block>
    def block(self):
        # <statement>*
        if self.is_type(TT.END_OF_FILE, TT.CLOSE_CURLY_BRACES):
            return None
        return Node("block", [self.statement(), self.block()])

    # <statement>
    def statement(self):
        node = None
        
        # <for_loop>
        if self.is_type(TT.FOR):
            node = self.for_loop()
        
        # <while_loop>
        elif self.is_type(TT.WHILE):
            node = self.while_loop()
        
        # <if_statement>
        elif self.is_type(TT.IF):
            node = self.if_statement()
        
        # <declaration> ";"
        elif self.is_type(TT.INT_DATA_TYPE, TT.STRING_DATA_TYPE, TT.BOOL_DATA_TYPE):
            node = self.declaration()
            self.expect(TT.SEMI_COLON)
        
        # <assignment> ";"
        elif self.is_type(TT.ASSIGN):
            node = self.assign()
            self.expect(TT.SEMI_COLON)
        
        # <output> ";"
        elif self.is_type(TT.PRINT):
            node = self.print()
            self.expect(TT.SEMI_COLON)
        
        # Expression
        else:
            node = self.expression()
            self.expect(TT.SEMI_COLON)
        
        return Node(NT.STATEMENT, [node])

    def declaration(self):
        # <declaration> ::= <data_type> <identifier> "=" <expression>
        data_type = self.expect(TT.INT_DATA_TYPE, TT.BOOL_DATA_TYPE, TT.STRING_DATA_TYPE)
        identifier = self.expect(TT.IDENTIFIER)
        self.expect(TT.EQUAL)
        expression = self.expression()
        return Node(NT.DECLARATION, [data_type, identifier, expression])

    def assign(self):
        # <assignment> ::= "set" <identifier> "=" <expression>
        self.expect(TT.ASSIGN)
        identifier = self.expect(TT.IDENTIFIER)
        self.expect(TT.EQUAL)
        expression = self.expression()
        return Node(NT.ASSIGNMENT, [identifier, expression])

    def print(self):
        # <output> ::= "print" "(" <expression> ")"
        self.expect(TT.PRINT)
        self.expect(TT.OPEN_PARENTHESIS)
        expression = self.expression()
        self.expect(TT.CLOSE_PARENTHESIS)
        return Node(NT.PRINT, [expression])
    
    def input(self):
        # <input> ::= "input" "(" <expression> ")"
        self.expect(TT.INPUT)
        self.expect(TT.OPEN_PARENTHESIS)
        expression = self.expression()
        self.expect(TT.CLOSE_PARENTHESIS)

        return Node(NT.INPUT, [expression])

    def for_loop(self):
        # <for_loop> ::= "for" "(" <declaration> ";" <expression> ";" <expression> ")" "{" <block> "}"
        self.expect(TT.FOR)
        self.expect(TT.OPEN_PARENTHESIS)
        initialization = self.declaration()
        self.expect(TT.SEMI_COLON)
        condition = self.expression()
        self.expect(TT.SEMI_COLON)
        increment = self.expression()
        self.expect(TT.CLOSE_PARENTHESIS)

        self.expect(TT.OPEN_CURLY_BRACES)
        block = self.block()
        self.expect(TT.CLOSE_PARENTHESIS)

        return Node(NT.FOR, [initialization, condition, increment, block])

    def while_loop(self):
        # <while_loop> ::= "while" "(" <expression> ")" "{" <block> "}"
        self.expect(TT.WHILE)
        self.expect(TT.OPEN_PARENTHESIS)
        condition = self.expression()
        self.expect(TT.CLOSE_PARENTHESIS)

        self.expect(TT.OPEN_CURLY_BRACES)
        block = self.block()
        self.expect(TT.CLOSE_PARENTHESIS)

        return Node(NT.WHILE, [condition, block])

    def if_statement(self):
        # TODO elif and else
        # <selection_statement> ::= "if" "(" <expression> ")" "{" <block> "}" <elif>
        self.expect(TT.IF)
        self.expect(TT.OPEN_PARENTHESIS)
        condition = self.expression()
        self.expect(TT.CLOSE_PARENTHESIS)

        self.expect(TT.OPEN_CURLY_BRACES)
        block = self.block()
        self.expect(TT.CLOSE_CURLY_BRACES)
        optional = self.elif_statement()
        return Node(NT.IF, [condition, block, optional])

    def elif_statement(self):
        # elif ("elif" "(" <expression> ")" "{" <block> "}")* ("else" "{" <statement> "}")?
        if self.is_type(TT.ELIF):
            self.expect(TT.ELIF)
            self.expect(TT.OPEN_PARENTHESIS)
            condition = self.expression()
            self.expect(TT.CLOSE_PARENTHESIS)
            self.expect(TT.OPEN_CURLY_BRACES)
            block = self.block()
            self.expect(TT.CLOSE_CURLY_BRACES)
            optional = self.elif_statement()
            return Node(NT.ELIF, [condition, block, optional])
        elif self.is_type(TT.ELSE):
            self.expect(TT.ELSE)
            self.expect(TT.OPEN_CURLY_BRACES)
            block = self.block()
            self.expect(TT.CLOSE_CURLY_BRACES)
            return Node(NT.ELSE, block)
        return None


    def expression(self, precedence = 0):
        if self.is_type(TT.SEMI_COLON):
            return None
        
        if self.is_type(TT.INPUT):
            return self.input()

        expression_tree = self.term()

        while NT.is_binary_operator(self.current().type) and NT.get_precedence(self.current().type) >= precedence:
            current = self.current()
            print(current)

            self.next()

            next_precedence = NT.get_precedence(current.type)
            if NT.get_associativity(current.type) != "RIGHT":
                next_precedence += 1

            expression_tree = Node(
                NodeType.to_node_type(current.type), [expression_tree, self.expression(next_precedence)])

        return expression_tree

    def term(self):
        node = None
        if self.is_type(TT.OPEN_PARENTHESIS):
            node = self.parenthesis_expression()
        elif self.is_type(TT.MINUS):
            self.next()
            node = Node(NT.NEGATE, [self.expression(
                NT.get_precedence(NT.NEGATE))])
        elif self.is_type(TT.NOT):
            self.next()
            node = Node(NT.NOT, [self.expression(Types.get_precedence("not"))])
        elif self.is_type(TT.IDENTIFIER):
            node = Node(NT.IDENTIFIER, [self.current()])
            self.next()
        elif self.is_type(TT.INT_LITERAL, TT.BOOL_LITERAL, TT.STRING_LITERAL):
            node = Node(NT.to_node_type(self.current().type), [self.current()])
            self.next()
        else:
            raise_syntax_error("", "")
        return node

    def parenthesis_expression(self):
        self.expect(TT.OPEN_PARENTHESIS)
        node = Node(None, [self.expression()])
        self.expect(TT.CLOSE_PARENTHESIS)
        return node

    def print_tree(self, current: Node):
        if current == None:
            print(";\n")
        else:
            if self.is_type(TT.INT_LITERAL, TT.BOOL_LITERAL, TT.STRING_LITERAL, TT.IDENTIFIER):
                print(current.parameters[0].value, end=" ")
            else:
                print(current.token, end=" ")
                for node in current.parameters:
                    self.print_tree(node)

    """
    def traverse_tree(self, current: Node):
        if current == None: return

        # check if literal or identifier

        # traverse tree
        for param in current.parameters:
            self.traverse_tree(param)
        
        # evaluate
        if current.type == "if statement":
            if current.parameters[0].type != "boolean type":
                raise_error()
        
        if current.type == "add":
            if current.parameters[0].type != "int":
                raise_error()

        if current.type == "declaration":
            # identifier
            if current.parameters[1].value is already declared:
                raise_error("identifier has already been ")

    """



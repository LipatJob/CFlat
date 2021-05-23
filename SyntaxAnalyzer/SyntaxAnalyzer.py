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
        return self.program()

    def current(self):
        if self.is_complete(): return None
        return self.tokens[self.pointer]

    def next(self):
        self.pointer += 1

    def is_complete(self):
        return self.pointer >= len(self.tokens)

    def expect(self, *expected_types):
        for expected in expected_types:
            current_type = self.current()
            if current_type.type == expected:
                cur = self.current()
                self.next()
                return cur
        else:
            raise_syntax_error("or".join(expected_types), self.current().type)

    def is_type(self, *args):
        for arg in args:
            if self.current().type == arg:
                return True
        return False

    # <program>
    def program(self):
        # <block>
        return Node(NT.PROGRAM, [self.block()])

    # <block>
    def block(self):
        # <statement>*
        node = Node(NT.BLOCK, [])
        while not self.is_complete() and not self.is_type(TT.END_OF_FILE, TT.CLOSE_CURLY_BRACES):
            node.parameters.append(self.statement())

        return node

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
        elif self.is_type(TT.SET):
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
        dt = self.expect(
            TT.INT_DATA_TYPE, TT.BOOL_DATA_TYPE, TT.STRING_DATA_TYPE)
        data_type = Node(NT.to_node_type(dt.type),[])

        id = self.expect(TT.IDENTIFIER)
        identifier = Node(NT.to_node_type(id.type), [id.value])
         
        self.expect(TT.EQUAL)
        expression = self.expression()
        return Node(NT.DECLARATION, [data_type, identifier, expression])

    def assign(self):
        # <assignment> ::= "set" <identifier> "=" <expression>
        self.expect(TT.EQUAL)
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
        self.expect(TT.CLOSE_CURLY_BRACES)

        return Node(NT.FOR, [initialization, condition, increment, block])

    def while_loop(self):
        # <while_loop> ::= "while" "(" <expression> ")" "{" <block> "}"
        self.expect(TT.WHILE)
        self.expect(TT.OPEN_PARENTHESIS)
        condition = self.expression()
        self.expect(TT.CLOSE_PARENTHESIS)

        self.expect(TT.OPEN_CURLY_BRACES)
        block = self.block()
        self.expect(TT.CLOSE_CURLY_BRACES)

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

        parameters = [condition, block]

        optional = self.elif_statement()
        if optional != None:
            parameters.append(optional)

        return Node(NT.IF, parameters)

    def elif_statement(self):
        # elif ("elif" "(" <expression> ")" "{" <block> "}")* ("else" "{" <statement> "}")?
        if self.current() == None: 
            return None
        if self.is_type(TT.ELIF):
            self.expect(TT.ELIF)
            self.expect(TT.OPEN_PARENTHESIS)
            condition = self.expression()
            self.expect(TT.CLOSE_PARENTHESIS)
            self.expect(TT.OPEN_CURLY_BRACES)
            block = self.block()
            self.expect(TT.CLOSE_CURLY_BRACES)

            parameters = [condition, block]

            optional = self.elif_statement()
            if optional != None:
                parameters.append(optional)

            return Node(NT.ELIF, parameters)
        elif self.is_type(TT.ELSE):
            self.expect(TT.ELSE)
            self.expect(TT.OPEN_CURLY_BRACES)
            block = self.block()
            self.expect(TT.CLOSE_CURLY_BRACES)
            return Node(NT.ELSE, [block])
        return None

    def expression(self, precedence=0):
        if self.is_type(TT.SEMI_COLON):
            return None

        if self.is_type(TT.INPUT):
            return self.input()

        expression_tree = self.term()

        while NT.is_binary_operator(self.current().type) and NT.get_precedence(NT.to_node_type(self.current().type)) >= precedence:
            current = self.current()
            print(current)

            self.next()
            node_type = NT.to_node_type(current.type)
            next_precedence = NT.get_precedence(node_type)
            if NT.get_associativity(node_type) != "RIGHT":
                next_precedence += 1

            expression_tree = Node(
                node_type, [expression_tree, self.expression(next_precedence)])

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
            node = Node(NT.NOT, [self.expression(TT.get_precedence(NT.NOT))])
        elif self.is_type(TT.IDENTIFIER):
            node = Node(NT.IDENTIFIER, [self.current().value])
            self.next()
        elif self.is_type(TT.INT_LITERAL, TT.BOOL_LITERAL, TT.STRING_LITERAL):
            node = Node(NT.to_node_type(self.current().type), [self.current().value])
            self.next()
        else:
            raise_syntax_error("Expected term", self.current())
        return node

    def parenthesis_expression(self):
        self.expect(TT.OPEN_PARENTHESIS)
        node = self.expression()
        self.expect(TT.CLOSE_PARENTHESIS)
        return node

    def print_tree(self, current: Node, tabs = 0):
        start = "  "*tabs
        if current == None:
            print(";\n")
        else:
            if current.value in {NT.INT_LITERAL, NT.BOOL_LITERAL, NT.STRING_LITERAL, NT.IDENTIFIER}:
                print(start+current.parameters[0])
            else:
                print(start+current.value)
                for node in current.parameters:
                    self.print_tree(node, tabs + 1)

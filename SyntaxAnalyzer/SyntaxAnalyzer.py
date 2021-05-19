from os import execlp
from Lib.Node import Node
from Lib.Token import *
from Lib.Token import TokenType as TT
from typing import List
from Lib.ErrorHandler import *
from pprint import pprint


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

    def expect(self, expected):
        if self.current().type != expected:
            raise_error(expected, self.current().type)
        self.next()
        return self.current()

    # <program>
    def program(self):
        # <block>
        return Node("program", self.block())

    # <block>
    def block(self):
        # <statement>*
        if self.current() == Types.end_of_file:
            return None
        return Node("block", [self.statement(), self.block()])

    # <statement>
    def statement(self):
        node = None
        current_type = self.current().type
        if current_type == TT.FOR:
            node = self.for_loop()
        elif current_type == TT.WHILE:
            node = self.while_loop()
        elif current_type == TT.IF:
            node = self.if_statement()
        if current_type in (TT.INT, TT.STRING, TT.BOOL):
            node = self.declaration()
            self.expect(TT.SEMI_COLON)
        elif current_type == TT.EQUAL:
            node = self.assign()
            self.expect(TT.SEMI_COLON)
        elif current_type == TT.PRINT:
            node = self.print()
            self.expect(TT.SEMI_COLON)
        elif current_type == TT.INPUT:
            node = self.input()
            self.expect(TT.SEMI_COLON)
        else:
            node = self.expression()
            self.expect(TT.SEMI_COLON)
        return Node("statement", [node])

    def declaration(self):
        data_type = self.expect("data_type")
        identifier = self.expect(TT.IDENTIFIER)
        self.expect(TT.EQUAL)
        expression = self.expression()
        return Node("declaration", [data_type, identifier, expression])

    def assign(self):
        identifier = self.expect(TT.IDENTIFIER)
        self.expect(TT.EQUAL)
        expression = self.expression()
        return Node("assignment", [identifier, expression])

    def print(self):
        self.expect(TT.PRINT)
        self.expect(TT.OPEN_PARENTHESIS)
        expression = self.expression()
        self.expect(TT.CLOSE_PARENTHESIS)
        return Node("print", [expression])
    
    def input(self):
        self.expect(TT.INPUT)
        self.expect(TT.OPEN_PARENTHESIS)
        expression = self.expression()
        self.expect(TT.CLOSE_PARENTHESIS)
        return Node("input", [expression])

    def for_loop(self):
        self.expect(TT.FOR)
        self.expect(TT.OPEN_PARENTHESIS)
        initialization = self.declaration()

        self.expect(TT.SEMI_COLON)
        condition = self.expression()
        self.expect(TT.SEMI_COLON)

        increment = self.expression()
        self.expect(TT.CLOSE_PARENTHESIS)

        self.block()
        return Node("for", [initialization, condition, increment])

    def while_loop(self):
        self.expect(TT.WHILE)
        self.expect(TT.OPEN_PARENTHESIS)
        condition = self.expression()
        self.expect(TT.CLOSE_PARENTHESIS)
        self.expect(TT.OPEN_CURLY_BRACES)
        block = self.block()
        self.expect(TT.CLOSE_PARENTHESIS)
        return Node("while", [condition, block])

    def if_statement(self):
        # TODO elif and else
        self.expect(TT.IF)
        self.expect(TT.OPEN_PARENTHESIS)
        condition = self.expression()
        self.expect(TT.CLOSE_PARENTHESIS)
        self.expect(TT.OPEN_CURLY_BRACES)
        block = self.block()
        self.expect(TT.CLOSE_CURLY_BRACES)
        optional = self.elif_statement()
        return Node("if", [condition, block, optional])

    def elif_statement(self):
        if self.current().type == TT.ELIF:
            self.expect(TT.ELIF)
            self.expect(TT.OPEN_PARENTHESIS)
            condition = self.expression()
            self.expect(TT.CLOSE_PARENTHESIS)
            self.expect(TT.OPEN_CURLY_BRACES)
            block = self.block()
            self.expect(TT.CLOSE_CURLY_BRACES)
            optional = self.elif_statement()
            return Node("elif", [condition, block, optional])
        elif self.current().type == TT.ELSE:
            self.expect(TT.ELSE)
            self.expect(TT.OPEN_CURLY_BRACES)
            block = self.block()
            self.expect(TT.CLOSE_CURLY_BRACES)
            return Node("else", block)
        return None


    def expression(self, precedence = 0):
        if self.current().type == TT.SEMI_COLON:
            return None
        
        if(self.current().type == TT.PRINT):
            return self.print()

        expression_tree = self.term()

        while Types.is_binary_operator(self.current().type) and Types.get_precedence(self.current().type) >= precedence:
            current = self.current()
            print(current)

            self.next()

            next_precedence = Types.get_precedence(current.type)
            if Types.get_associativity(current.type) != "RIGHT":
                next_precedence += 1

            expression_tree = Node(
                current.type, [expression_tree, self.expression(next_precedence)])

        return expression_tree

    def term(self):
        current_token = self.current().type
        node = None
        if current_token == TT.OPEN_PARENTHESIS:
            node = self.parenthesis_expression()
        elif current_token == TT.MINUS:
            self.next()
            node = Node("negate", [self.expression(
                Types.get_precedence("negate"))])
        elif current_token == TT.NOT:
            self.next()
            node = Node("not", [self.expression(Types.get_precedence("not"))])
        elif current_token == TT.IDENTIFIER:
            node = Node("identifier", [self.current()])
            self.next()
        elif current_token in {TT.INT_LITERAL, TT.BOOL_LITERAL, TT.STRING_LITERAL}:
            node = Node("literal", [self.current()])
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
            if current.token in {TT.INT_LITERAL, TT.BOOL_LITERAL, TT.STRING_LITERAL, TT.IDENTIFIER}:
                print(current.parameters[0].value, end=" ")
            else:
                print(current.token, end=" ")
                for node in current.parameters:
                    self.print_tree(node)

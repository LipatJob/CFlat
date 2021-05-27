from os import execlp
from Lib.Node import *
from Lib.Node import NodeType as NT

from Lib.Token import *
from Lib.Token import TokenType as TT
from typing import List
from Lib.ErrorHandler import *


class SyntaxAnalyzer:
    def run(self, tokens: List[Token]) -> 'Node':
        self.tokens = tokens
        self.pointer = 0
        return self.program()

    def current(self):
        if self.is_complete():
            return None
        return self.tokens[self.pointer]

    def next(self):
        self.pointer += 1

    def is_complete(self):
        return self.pointer >= len(self.tokens)

    def expect(self, *expected_types):
        if self.is_complete():
            raise_syntax_error(", ".join(expected_types),
                               "END_OF_FILE", self.tokens[-1])
        for expected in expected_types:
            current_type = self.current()
            if current_type.type == expected:
                cur = self.current()
                self.next()
                return cur
        else:
            raise_syntax_error("or".join(expected_types),
                               self.current().type, self.current())

    def is_type(self, *args):
        if self.is_complete(): return False
        for arg in args:
            if self.current().type == arg:
                return True
        return False

    # <program>
    def program(self):
        # <block>
        return Node(NT.PROGRAM, [self.block()], self.current())

    # <block>
    def block(self):
        # <statement>*
        node = Node(NT.BLOCK, [], self.current())
        while not self.is_complete() and not self.is_type(TT.END_OF_FILE, TT.CLOSE_CURLY_BRACES):
            node.parameters.append(self.statement())

        return node

    # <statement>
    def statement(self):
        token = self.current()
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

        return Node(NT.STATEMENT, [node], token)

    def declaration(self):
        # <declaration> ::= <data_type> <identifier> "=" <expression>
        dt = self.expect(
            TT.INT_DATA_TYPE, TT.BOOL_DATA_TYPE, TT.STRING_DATA_TYPE)
        data_type = Node(NT.to_node_type(dt.type), [])

        id = self.expect(TT.IDENTIFIER)
        identifier = Node(NT.to_node_type(id.type), [id.value], id)

        self.expect(TT.EQUAL)
        expression = self.expression()
        return Node(NT.DECLARATION, [data_type, identifier, expression], dt)

    def assign(self):
        # <assignment> ::= "set" <identifier> "=" <expression>
        set = self.expect(TT.SET)

        id = self.expect(TT.IDENTIFIER)
        identifier = Node(NT.to_node_type(id.type), [id.value], id)

        self.expect(TT.EQUAL)
        expression = self.expression()
        return Node(NT.ASSIGNMENT, [identifier, expression], set)

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
        parameters = []
        if self.current().type != TT.CLOSE_PARENTHESIS:
            parameters.append(self.expression())
        self.expect(TT.CLOSE_PARENTHESIS)

        return Node(NT.INPUT, [Node(NT.STRING_LITERAL, [""])])

    def for_loop(self):
        # <for_loop> ::= "for" "(" <declaration> ";" <expression> ";" <expression> ")" "{" <block> "}"
        for_token = self.expect(TT.FOR)
        self.expect(TT.OPEN_PARENTHESIS)
        initialization = self.declaration()
        self.expect(TT.SEMI_COLON)
        condition = self.expression()
        self.expect(TT.SEMI_COLON)
        increment = self.assign()
        self.expect(TT.CLOSE_PARENTHESIS)

        self.expect(TT.OPEN_CURLY_BRACES)
        block = self.block()
        self.expect(TT.CLOSE_CURLY_BRACES)

        return Node(NT.FOR, [initialization, condition, increment, block], for_token)

    def while_loop(self):
        # <while_loop> ::= "while" "(" <expression> ")" "{" <block> "}"
        while_token = self.expect(TT.WHILE)
        self.expect(TT.OPEN_PARENTHESIS)
        condition = self.expression()
        self.expect(TT.CLOSE_PARENTHESIS)

        self.expect(TT.OPEN_CURLY_BRACES)
        block = self.block()
        self.expect(TT.CLOSE_CURLY_BRACES)

        return Node(NT.WHILE, [condition, block], while_token)

    def if_statement(self):
        # TODO elif and else
        # <selection_statement> ::= "if" "(" <expression> ")" "{" <block> "}" <elif>
        if_token = self.expect(TT.IF)
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

        return Node(NT.IF, parameters, if_token)

    def elif_statement(self):
        # elif ("elif" "(" <expression> ")" "{" <block> "}")* ("else" "{" <statement> "}")?
        if self.current() == None:
            return None
        if self.is_type(TT.ELIF):
            elif_token = self.expect(TT.ELIF)
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

            return Node(NT.ELIF, parameters, elif_token)
        elif self.is_type(TT.ELSE):
            else_token = self.expect(TT.ELSE)
            self.expect(TT.OPEN_CURLY_BRACES)
            block = self.block()
            self.expect(TT.CLOSE_CURLY_BRACES)
            return Node(NT.ELSE, [block], else_token)
        return None

    def expression(self, precedence=0):
        if self.is_type(TT.INPUT):
            return self.input()

        expression_tree = self.term()
        if self.is_type(TT.SEMI_COLON) or self.is_complete(): return expression_tree

        while NT.is_binary_operator(self.current().type) and NT.get_precedence(NT.to_node_type(self.current().type)) >= precedence:
            current = self.current()

            self.next()
            node_type = NT.to_node_type(current.type)
            next_precedence = NT.get_precedence(node_type)
            if NT.get_associativity(node_type) != "RIGHT":
                next_precedence += 1

            expression_tree = Node(
                node_type, [expression_tree, self.expression(next_precedence)], current)

        return expression_tree

    def term(self):
        node = None
        if self.is_type(TT.OPEN_PARENTHESIS):
            node = self.parenthesis_expression()
        elif self.is_type(TT.MINUS):
            current = self.current()
            self.next()
            node = Node(NT.NEGATE, [self.expression(
                NT.get_precedence(NT.NEGATE))], current)
        elif self.is_type(TT.NOT):
            current = self.current()
            self.next()
            node = Node(NT.NOT, [self.expression(
                NT.get_precedence(NT.NOT))], current)
        elif self.is_type(TT.IDENTIFIER):
            node = Node(NT.IDENTIFIER, [self.current().value], self.current())
            self.next()
        elif self.is_type(TT.INT_LITERAL, TT.BOOL_LITERAL, TT.STRING_LITERAL):
            node = Node(NT.to_node_type(self.current().type), [
                        self.current().value], self.current())
            self.next()
        else:
            raise_syntax_error("TERM", self.current().type, self.current())
        return node

    def parenthesis_expression(self):
        self.expect(TT.OPEN_PARENTHESIS)
        node = self.expression()
        self.expect(TT.CLOSE_PARENTHESIS)
        return node

    def print_tree(self, current: Node, tabs=0):
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

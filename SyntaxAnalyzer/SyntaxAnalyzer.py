from os import execlp
from Lib.Node import Node
from Lib.Token import *
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
        return self.current()
        self.next()

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
        if current_type == "for":
            node = self.for_loop()
        elif current_type == "while":
            node = self.while_loop()
        elif current_type == "if":
            node = self.if_statement()
        if current_type == "keyword":
            node = self.declaration()
            self.expect(";")
        elif current_type == "assign":
            node = self.assign()
            self.expect(";")
        elif current_type == "print":
            node = self.print()
            self.expect(";")
        elif current_type == "input":
            node = self.input()
            self.expect(";")
        else:
            node = self.expression()
            self.expect(";")
        return Node("statement", [node])

    def declaration(self):
        data_type = self.expect("data_type")
        identifier = self.expect("identifier")
        self.expect("=")
        expression = self.expression()
        return Node("declaration", [data_type, identifier, expression])

    def assign(self):
        identifier = self.expect("identifier")
        self.expect("=")
        expression = self.expression()
        return Node("assignment", [identifier, expression])

    def print(self):
        self.expect("print")
        self.expect("(")
        expression = self.expression()
        self.expect(")")
        return Node("print", [expression])
    
    def input(self):
        self.expect("input")
        self.expect("(")
        expression = self.expression()
        self.expect(")")
        return Node("input", [expression])

    def for_loop(self):
        self.expect("for")
        self.expect("(")
        initialization = self.declaration()

        self.expect(";")
        condition = self.expression()
        self.expect(";")

        increment = self.expression()
        self.expect(")")

        self.block()
        return Node("for", [initialization, condition, increment])

    def while_loop(self):
        self.expect("while")
        self.expect("(")
        condition = self.expression()
        self.expect(")")
        self.expect("{")
        block = self.block()
        self.expect("}")
        return Node("while", [condition, block])

    def if_statement(self):
        # TODO elif and else
        self.expect("if")
        self.expect("(")
        condition = self.expression()
        self.expect(")")
        self.expect("{")
        block = self.block()
        self.expect("}")
        return Node("if", [condition, block])

    def expression(self, precedence = 0):
        if self.current().type == ";":
            return None
        
        if(self.current().type == "print"):
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
        if current_token == "(":
            node = self.parenthesis_expression()
        elif current_token == "-":
            self.next()
            node = Node("negate", [self.expression(
                Types.get_precedence("negate"))])
        elif current_token == "not":
            self.next()
            node = Node("not", [self.expression(Types.get_precedence("not"))])
        elif current_token == "identifier":
            node = Node("identifier", [self.current()])
            self.next()
        elif current_token == "literal":
            node = Node("literal", [self.current()])
            self.next()
        else:
            raise_syntax_error("", "")
        return node

    def parenthesis_expression(self):
        self.expect(")")
        node = Node(None, [self.expression()])
        self.expect("(")
        return node

    def print_tree(self, current: Node):
        if current == None:
            print(";\n")
        else:
            if current.token in {"literal", "identifier"}:
                print(current.parameters[0].value, end=" ")
            else:
                print(current.token, end=" ")
                for node in current.parameters:
                    self.print_tree(node)

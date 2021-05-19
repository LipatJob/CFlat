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
        if self.is_last(): raise IndexError()
        self.pointer += 1
    
    def is_last(self):
        return self.pointer >= len(self.tokens)

    def expect(self, expected):
        if self.current().type != expected:
            raise_error(expected, self.current().type)
        self.next()

    def program(self):
        return Node(self.block())
    
    def block(self):
        if self.current() == Types.end_of_file:
            return None
        return Node("block", [self.statement(), self.block()])
    
    def statement(self):
        if self.current().type == "keyword":
            return self.declaration()
        elif self.current().type == "for":
            return self.for_loop()
        elif self.current().type == "while":
            return self.while_loop()
        elif self.current.type == "if":
            return self.if_statement()
        return Node("statement", [self.expression()])
    
    def declaration(self):
        return Node("declaration", [None, self.expression(), self.expression])
    
    def for_loop(self):
        return Node("for", [self.declaration(), self.expression(), self.expression(), self.block()])

    def while_loop(self):
        return Node("while", [self.expression(), self.block()])
    
    def if_statement(self):
        # TODO elif and else
        return Node("if", [self.expression(), self.block()])
    
    def expression(self, precedence):
        if self.current().type == ";": return None 

        expression_tree = self.term()

        while Types.is_binary_operator(self.current().type) and Types.get_precedence(self.current().type) >= precedence:
            current = self.current()
            print(current)

            self.next()

            next_precedence = Types.get_precedence(current.type)
            if Types.get_associativity(current.type) != "RIGHT":
                next_precedence += 1

            
            expression_tree = Node(current.type, [expression_tree, self.expression(next_precedence)])

        return expression_tree
    
    def term(self):
        current_token = self.current().type
        print(current_token)
        node = None
        if current_token  == "(":         
            node = self.parenthesis_expression()
        elif current_token == "identifier":
            node = Node("identifier", [self.current()])
            self.next()            
        elif current_token == "literal":
            node =  Node("literal", [self.current()])
            self.next()            
        else:
            raise_syntax_error("", "")
        return node


    def parenthesis_expression(self):
        return Node(None, [self.expression()])
    
    def print_tree(self, current:Node):
        if current == None:
            print(";\n")
        else:
            if current.token in {"literal", "identifier"}:
                print(current.parameters[0].value)
            else:
                pprint(current.token)
                for node in current.parameters:
                    self.print_tree(node)

from Lib.Node import Node
from Lib.Token import *
from typing import List
from Lib.ErrorHandler import * 

def raise_syntax_error(expected, actual):
    raise_error(f"Syntax Error: expected {expected} got {actual}")

class SyntaxAnalyzer:
    def run(self, tokens: List[Token]) -> 'Node':
        self.tokens = tokens
        self.pointer = 0
        return Node()
    
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
        if self.current().type == Types.keyword_datatype:
            return self.declaration()
        elif self.current().type == Types.keyword_for_loop:
            return self.for_loop()
        elif self.current().type == Types.keyword_while_loop:
            return self.while_loop()
        elif self.current.type == Types.keyword_conditional_statement:
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
    
    def expression(self, min_precedence):
        left_hand_side = self.term()

        while self.is_binary_operator(current.type) and self.get_precedence(current.type) > min_precedence:
            current = self.current()
            precedence = self.get_precedence(current.type)
            associativity = self.get_associativity(self.type)

            next_min_precedence = precedence + 1 if associativity == 'LEFT' else precedence

            right_hand_side = self.expression(next_min_precedence)

        return Node(None, [left_hand_side, right_hand_side])
    
    def is_binary_operator(self, operator):
        return 0
    
    def get_precedence(self, operator):
        return 0

    def get_associativity(self, operator):
        return 0
    
    def term(self):
        current_token = self.current().type
        if current_token  == Types.symbol_left_parenthesis:
            return self.parenthesis_expression()
        elif current_token == Types.identifier:
            return Node("Identifier", [self.current])
        elif current_token == Types.literal_integer:
            return Node("literal", [self.current])
        else:
            raise_syntax_error("", "")


    def parenthesis_expression(self):
        return Node(None, [self.expression()])
    

        
    
    
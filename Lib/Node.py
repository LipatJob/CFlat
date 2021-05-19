from typing import List
from Lib.Token import Token

class Node:
    def __init__(self, token :'Token', parameters : List['Node']):
        self.token = token
        self.parameters = parameters

class NodeType:
    PROGRAM = "PROGRAM"
    BLOCK = "BLOCK"
    STATEMENT = "STATEMENT"
    DECLARATION = "DECLARATION"
    ASSIGNMENT = "ASSIGNMENT"
    PRINT = "PRINT"
    INPUT = "INPUT"
    FOR = "FOR"
    WHILE = "WHILE"
    IF = "IF"
    ELIF = "ELIF"
    ELSE = "ELSE"
    NEGATE = "NEGATE"
    NOT = "NOT"

    IDENTIFIER = "IDENTIFIER"
    INT_LITERAL = "INT_LITERAL"
    STRING_LITERAL = "STRING_LITERAL"
    BOOL_LITERAL = "BOOL_LITERAL"

    @classmethod
    def to_node_type(cls, token_type):
        pass

    precedence = {
        "negate": 6,
        "not": 6,
        "*": 5,
        "/": 5,
        "+": 4,
        "-": 4,
        ">": 3,
        "<": 3,
        ">=": 3,
        "<=": 3,
        "==": 2,
        "!=": 2,
        "and": 1,
        "or": 0,
    }

    associativity = {
        "+": "LEFT",
        "-":  "LEFT",
        "*":  "LEFT",
        "/":  "LEFT",
    }

    @classmethod
    def get_precedence(cls, operator):
        return cls.precedence[operator]

    @classmethod
    def get_associativity(cls, operator):
        return cls.associativity[operator]

    @classmethod
    def is_binary_operator(cls, operator):
        return operator in cls.precedence
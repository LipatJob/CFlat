from typing import List
from Lib.Token import Token

class Node:
    def __init__(self, value, parameters : List['Node']):
        self.value = value
        self.parameters = parameters

class NodeType:
    PROGRAM = "PROGRAM" # (BLOCK)
    BLOCK = "BLOCK"# (STATMENT)
    STATEMENT = "STATEMENT"
    DECLARATION = "DECLARATION"
    ASSIGNMENT = "ASSIGNMENT" # (DATE_TYPE, IDENTIFER, EXPRESSION)
    PRINT = "PRINT"
    INPUT = "INPUT"

    FOR = "FOR"
    WHILE = "WHILE"

    IF = "IF"
    ELIF = "ELIF"
    ELSE = "ELSE"

    IDENTIFIER = "IDENTIFIER"
    INT_LITERAL = "INT_LITERAL"
    STRING_LITERAL = "STRING_LITERAL"
    BOOL_LITERAL = "BOOL_LITERAL"

    NEGATE = "NEGATE"
    ADD = "ADD"
    SUBTRACT = "SUBTRACT"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"

    EQUAL = "EQUAL"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"

    DOUBLE_EQUAL = "DOUBLE_EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    MORE_THAN = "MORE_THAN"
    LESS = "LESS"
    MORE = "MORE"
    LESS_EQUAL = "LESS_EQUAL"
    MORE_EQUAL = "MORE_EQUAL"
    END_OF_FILE = "END_OF_FILE"

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
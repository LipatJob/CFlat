from typing import List
from Lib.Token import Token, TokenType as TT


class Node:
    def __init__(self, value, parameters: List['Node'], token_source: Token = None, expression_type=None):
        self.value = value
        self.parameters = parameters
        self.expression_type = expression_type
        self.token_source = token_source


class ExpressionType:
    INT = "INT"
    STRING = "STRING"
    BOOL = "BOOL"

    @classmethod
    def to_expresion_type(cls, node_type):
        conversion = {
            NodeType.INT_DATA_TYPE: cls.INT,
            NodeType.STRING_DATA_TYPE: cls.STRING,
            NodeType.BOOL_DATA_TYPE: cls.BOOL,
        }

        return conversion[node_type]


class NodeType:
    PROGRAM = "PROGRAM"  # (BLOCK)
    BLOCK = "BLOCK"  # (STATMENT)
    STATEMENT = "STATEMENT"
    DECLARATION = "DECLARATION"  # (DATE_TYPE, IDENTIFER, EXPRESSION)
    ASSIGNMENT = "ASSIGNMENT"
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
    INT_DATA_TYPE = "INT_DATA_TYPE"
    BOOL_DATA_TYPE = "BOOL_DATA_TYPE"
    STRING_DATA_TYPE = "STRING_DATA_TYPE"

    NEGATE = "NEGATE"
    ADD = "ADD"
    SUBTRACT = "SUBTRACT"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"

    AND = "AND"
    OR = "OR"
    NOT = "NOT"

    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS = "LESS"
    MORE = "MORE"
    LESS_EQUAL = "LESS_EQUAL"
    MORE_EQUAL = "MORE_EQUAL"
    END_OF_FILE = "END_OF_FILE"

    token_to_node_table = {
        TT.AND: AND,
        TT.OR: OR,
        TT.NOT: NOT,
        TT.PLUS: ADD,
        TT.MINUS: SUBTRACT,
        TT.STAR: MULTIPLY,
        TT.SLASH: DIVIDE,
        TT.DOUBLE_EQUAL: EQUAL,
        TT.NOT_EQUAL: NOT_EQUAL,
        TT.LESS: LESS,
        TT.MORE: MORE,
        TT.LESS_EQUAL: LESS_EQUAL,
        TT.MORE_EQUAL: MORE_EQUAL,
        TT.INT_LITERAL: INT_LITERAL,
        TT.STRING_LITERAL: STRING_LITERAL,
        TT.BOOL_LITERAL: BOOL_LITERAL,
        TT.INT_DATA_TYPE: INT_DATA_TYPE,
        TT.BOOL_DATA_TYPE: BOOL_DATA_TYPE,
        TT.STRING_DATA_TYPE: STRING_DATA_TYPE,
        TT.IDENTIFIER: IDENTIFIER,
    }

    @classmethod
    def to_node_type(cls, token_type):
        return cls.token_to_node_table[token_type]

    precedence = {
        NEGATE: 6,
        NOT: 6,
        MULTIPLY: 5,
        DIVIDE: 5,
        ADD: 4,
        SUBTRACT: 4,
        MORE: 3,
        LESS: 3,
        MORE_EQUAL: 3,
        LESS_EQUAL: 3,
        EQUAL: 2,
        NOT_EQUAL: 2,
        AND: 1,
        OR: 0,
    }

    binary_operators = {
        TT.AND,
        TT.OR,
        TT.NOT,
        TT.PLUS,
        TT.MINUS,
        TT.STAR,
        TT.SLASH,
        TT.DOUBLE_EQUAL,
        TT.NOT_EQUAL,
        TT.LESS,
        TT.MORE,
        TT.LESS_EQUAL,
        TT.MORE_EQUAL,
    }

    associativity = {
        NEGATE: "LEFT",
        NOT: "LEFT",
        MULTIPLY: "LEFT",
        DIVIDE: "LEFT",
        ADD: "LEFT",
        SUBTRACT: "LEFT",
        MORE: "LEFT",
        LESS: "LEFT",
        MORE_EQUAL: "LEFT",
        LESS_EQUAL: "LEFT",
        EQUAL: "LEFT",
        NOT_EQUAL: "LEFT",
        AND: "LEFT",
        OR: "LEFT",
    }

    @classmethod
    def get_precedence(cls, operator):
        return cls.precedence[operator]

    @classmethod
    def get_associativity(cls, operator):
        return cls.associativity[operator]

    @classmethod
    def is_binary_operator(cls, operator):
        return operator in cls.binary_operators

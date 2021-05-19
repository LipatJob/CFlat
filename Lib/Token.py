from dataclasses import dataclass


@dataclass
class Token:
    type: str
    value: str

    # Implement later
    line: int = 0  # In what line is the start of the token found
    column: int = 0  # How many characters are there before the start of the token


class Reserved:
    keyword_datatype = ["int", "string", "bool"]
    keyword_boolean_literal = ["True", "False"]
    comments = ["//", "/*"]
    keyword_inputoutput = ["input", "print"]
    symbols_delimiters = [",", "(", ")", ";", "{", "}"]
    keyword_conditional_statement = ["if", "elif", "else"]
    keyword_function = ["void", "return"]
    keyword_loops = ["while", "for"]
    symbols_assignment_operator = ["="]
    keyword_logical_operator = ["and", "or", "not"]
    symbols_arithmetic_operator = ["+", "-", "*", "/"]
    symbols_relational_operator = ["==", "!=", ">", "<", ">=", "<="]


class Types:
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

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
    keyword_datatype = "keyword_datatype"
    keyword_boolean_literal = "keyword_boolean_literal"
    comments = "comments"
    keyword_inputoutput = "keyword_inputoutput"
    symbols_delimiters = "symbols_delimiters"
    keyword_conditional_statement = "keyword_conditional_statement"
    keyword_function = "keyword_function"
    keyword_loops = "keyword_loops"
    symbols_assignment_operator = "symbols_assignment_operator"
    keyword_logical_operator = "keyword_logical_operator"
    symbols_arithmetic_operator = "symbols_arithmetic_operator"
    symbols_relational_operator = "symbols_relational_operator"

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

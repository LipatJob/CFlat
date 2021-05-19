from dataclasses import dataclass


@dataclass
class Token:
    type: str
    value: str

    # Implement later
    line: int = 0  # In what line is the start of the token found
    column: int = 0  # How many characters are there before the start of the token


class Reserved:
    reserved={
        "int": "keyword_datatype",
        "string": "keyword_datatype" ,
        "bool": "keyword_datatype" ,
        "True": "keyword_boolean_literal" ,
        "False": "keyword_boolean_literal" ,
        "//": "comments" ,
        "/*": "comments" ,
        "input": "keyword_inputoutput" ,
        "print": "keyword_inputoutput" ,
        ",": "symbols_delimiters" ,
        "(": "symbols_delimiters" ,
        ")": "symbols_delimiters" ,
        ";": "symbols_delimiters" ,
        "{": "symbols_delimiters" ,
        "}": "symbols_delimiters" ,
        "if": "keyword_conditional_statement" ,
        "elif": "keyword_conditional_statement",
        "else": "keyword_conditional_statement",
        "void": "keyword_function" ,
        "return": "keyword_function",
        "def": "keyword_function",
        "while": "keyword_loops" ,
        "for": "keyword_loops" ,
        "=": "symbols_assignment_operator",
        "and": "keyword_logical_operator",
        "or": "keyword_logical_operator" ,
        "not": "keyword_logical_operator" ,
        "+": "symbols_arithmetic_operator" ,
        "-": "symbols_arithmetic_operator" ,
        "*": "symbols_arithmetic_operator" ,
        "/": "symbols_arithmetic_operator" ,
        "==": "symbols_relational_operator",
        "!=": "symbols_relational_operator",
        ">": "symbols_relational_operator" ,
        "<": "symbols_relational_operator" ,
        ">=": "symbols_relational_operator",
        "<=": "symbols_relational_operator"
     }

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

class TokenType:
    INT = "INT"
    STRING = "STRING"
    BOOL = "BOOL"
    IDENTIFIER = "IDENTIFIER"
    INT_LITERAL = "INT_LITERAL"
    STRING_LITERAL = "STRING_LITERAL"
    BOOL_LITERAL = "BOOL_LITERAL"

    DOUBLE_SLASH = "DOUBLE_SLASH"
    SLASH_STAR = "SLASH_STAR"
    INPUT = "INPUT"
    PRINT = "PRINT"
    
    COMMA = "COMMA"
    OPEN_PARENTHESIS = "OPEN_PARENTHESIS"
    CLOSE_PARENTHESIS = "CLOSE_PARENTHESIS"
    SEMI_COLON = "SEMI_COLON"
    OPEN_CURLY_BRACES = "OPEN_CURLY_BRACES"
    CLOSE_CURLY_BRACES = "CLOSE_CURLY_BRACES"


    IF = "IF"
    ELIF = "ELIF"
    ELSE = "ELSE"

    WHILE = "WHILE"
    FOR = "FOR"

    VOID = "VOID"
    RETURN = "RETURN"

    EQUAL = "EQUAL"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"

    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"

    DOUBLE_EQUAL = "DOUBLE_EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    MORE_THAN = "MORE_THAN"
    LESS = "LESS"
    MORE = "MORE"
    LESS_EQUAL = "LESS_EQUAL"
    MORE_EQUAL = "MORE_EQUAL"
    END_OF_FILE = "END_OF_FILE"
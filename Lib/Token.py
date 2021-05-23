from dataclasses import dataclass


@dataclass
class Token:
    type: str
    value: str

    # Implement later
    line: int = 0  # In what line is the start of the token found
    column: int = 0  # How many characters are there before the start of the token
'''
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
'''
class TokenType:
    INT_DATA_TYPE = "INT"
    STRING_DATA_TYPE = "STRING"
    BOOL_DATA_TYPE = "BOOL"
    IDENTIFIER = "IDENTIFIER"
    INT_LITERAL = "INT_LITERAL"
    STRING_LITERAL = "STRING_LITERAL"
    BOOL_LITERAL = "BOOL_LITERAL"

    DOUBLE_SLASH = "DOUBLE_SLASH"
    SLASH_STAR = "SLASH_STAR"
    INPUT = "INPUT"
    PRINT = "PRINT"
    
    SET="SET"
    DEF="DEF" #nakalimutan ata natin to?
    SINGLE_LINE_COMMENT ="SINGLE_LINE_COMMENT"#nakalimutan ata natin to?
    MULTI_LINE_COMMENT ="MULTI_LINE_COMMENT"#nakalimutan ata natin to?

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

    EQUAL = "EQUAL" ##### huh umulit
    AND = "AND"
    OR = "OR"
    NOT = "NOT"

    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"

    DOUBLE_EQUAL = "DOUBLE_EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS = "LESS"
    MORE = "MORE"
    LESS_EQUAL = "LESS_EQUAL"
    MORE_EQUAL = "MORE_EQUAL"
    END_OF_FILE = "END_OF_FILE"

class Reserved:
    reserved={
        "int": TokenType.INT_DATA_TYPE ,
        "string": TokenType.STRING_DATA_TYPE ,
        "bool": TokenType.BOOL_DATA_TYPE,
        "True": TokenType.BOOL_LITERAL ,
        "False": TokenType.BOOL_LITERAL ,
        "//": TokenType.DOUBLE_SLASH ,
        "/*": TokenType.SLASH_STAR ,
        "input": TokenType.INPUT ,
        "print": TokenType.PRINT ,
        ",": TokenType.COMMA ,
        "(": TokenType.OPEN_PARENTHESIS ,
        ")": TokenType.CLOSE_PARENTHESIS ,
        ";": TokenType.SEMI_COLON ,
        "{": TokenType.OPEN_CURLY_BRACES ,
        "}": TokenType.CLOSE_CURLY_BRACES ,
        "if": TokenType.IF ,
        "elif": TokenType.ELIF ,
        "else": TokenType.ELSE ,
        "void": TokenType.VOID ,
        "return": TokenType.RETURN,
        "def": TokenType.DEF,
        "while": TokenType.WHILE ,
        "for": TokenType.FOR ,
        "=": TokenType.EQUAL,
        "and": TokenType.AND,
        "or": TokenType.OR ,
        "not": TokenType.NOT ,
        "+": TokenType.PLUS ,
        "-": TokenType.MINUS ,
        "*": TokenType.STAR ,
        "/": TokenType.SLASH ,
        "==": TokenType.DOUBLE_EQUAL,
        "!=": TokenType.NOT_EQUAL,
        ">": TokenType.MORE ,
        "<": TokenType.LESS ,
        ">=": TokenType.MORE_EQUAL,
        "<=": TokenType.LESS_EQUAL,
        "set":TokenType.SET
     }
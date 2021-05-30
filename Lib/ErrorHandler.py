from Lib.Node import ExpressionType as ET, NodeType as NT, Node
from Lib.Token import Token


def raise_error(error_message):
    print(error_message)
    raise Exception()

def raise_token_error(linecount, charcount):
    raise TokenError("ERROR: Unexpected token! Line: "+ str(linecount)+" Column: "+ str(charcount))

def raise_type_error(source: Token):
    raise TypeError(f"TYPE ERROR: Unexpected data type!\nSOURCE: Line {source.line} Column {source.column}")

def raise_identifier_error(character, source: Token):
    raise IdentifierError("IDENTIFIER ERROR: Variable " + character + f" is already in use!\nSOURCE: Line {source.line}, Column {source.column}")

def raise_undeclaredVariable_error(character, source: Token):
    raise UndeclaredVariableError("UNDECLARED VARIABLE ERROR: Variable " + character + f" is not defined!\nSOURCE: Line {source.line}, Column {source.column}")

def raise_syntax_error(expected, actual, token):
    raise SyntaxError(f"Syntax Error: expected {expected} got {actual} on line {token.line} column {token.column}")

class SemanticError(Exception):
    def __init__(self, message):
        super().__init__(message)

class TokenError(Exception):
     def __init__(self, message):
        super().__init__(message)


class TypeError(SemanticError):
     def __init__(self, message):            
        super().__init__(message)


class IdentifierError(SemanticError):
     def __init__(self, message):            
        super().__init__(message)


class SyntaxError(Exception):
     def __init__(self, message):
        super().__init__(message)


class UndeclaredVariableError(SemanticError):
     def __init__(self, message):            
        super().__init__(message)


    
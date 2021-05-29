def raise_error(error_message):
    print(error_message)
    raise Exception()

def raise_token_error(linecount,charcount):
    raise TokenError("ERROR: Unexpected token! Line: "+ str(linecount)+" Column: "+ str(charcount))

def raise_type_error():
    raise TypeError("ERROR: Unexpected type!")

def raise_identifier_error():
    raise IdentifierError("ERROR: Variables is already in use!")

def raise_undeclaredVariable_error(character):
    raise UndeclaredVariableError("ERROR: Variable", character, "is not defined!")

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


    
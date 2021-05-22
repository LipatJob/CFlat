def raise_error(error_message):
    print(error_message)
    exit()

def raise_type_error():
    raise_error("ERROR: Unexpected type!")

def raise_identifier_error():
    raise_error("ERROR: Variables is already in use!")

def raise_undeclaredVariable_error(character):
    raise_error("ERROR: Variable", character, "is not defined!")

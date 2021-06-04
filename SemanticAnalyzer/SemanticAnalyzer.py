from Lib.Node import Node, NodeType as NT, ExpressionType as ET
from Lib.Token import Token
from Lib.ErrorHandler import *

class SemanticAnalyzer:
    def __init__(self) -> None:
        self.SymbolDictionary = dict()

    def run(self, root: Node):
        self.SymbolDictionary = dict()
        self.analyze(root)
        return self.SymbolDictionary

    def analyze(self, root: Node):
        # Added traversal function code for type checking
        # NOTE: Type checking for Assignment, Declaration and Input still pending

        if root == None or len(root.parameters) == 0: return

        # Terminal expressions for leaf nodes
        # If identifier, check key if it exists and data type in SymbolDictionary
        # Otherwise, throw an error
        elif root.value in {NT.IDENTIFIER, NT.INT_LITERAL, NT.STRING_LITERAL, NT.BOOL_LITERAL, NT.INPUT}:
            if root.value == NT.INT_LITERAL:
                root.expression_type = ET.INT
            elif root.value in {NT.STRING_LITERAL, NT.INPUT}:
                root.expression_type = ET.STRING
            elif root.value == NT.BOOL_LITERAL:
                root.expression_type = ET.BOOL
            elif root.value == NT.IDENTIFIER:
                
                # Check if identifier is in the SymbolDictionary
                if root.parameters[0] not in self.SymbolDictionary:
                    raise_undeclaredVariable_error(root.parameters[0], root.token_source)
                else:
                    data_type = self.SymbolDictionary[root.parameters[0]][0]
                    root.expression_type = ET.to_expresion_type(data_type)
            return
        
        # (Code block not yet final)
        if root.value == NT.DECLARATION:
            self.analyze(root.parameters[2])
        else:
            for x in root.parameters:
                self.analyze(x)

        # DECLARATION STATEMENT
        # Enter code for storing variables
        # Check if dictionary is empty
        # If empty, store node values in dictionary
        # If not empty, compare the value in the dictionary
        if root.value == NT.DECLARATION:
            if root.parameters[0].value == NT.INT_DATA_TYPE and root.parameters[2].expression_type != ET.INT:
                raise_type_error(root.token_source)
            elif root.parameters[0].value == NT.STRING_DATA_TYPE and root.parameters[2].expression_type != ET.STRING:
                raise_type_error(root.token_source)
            elif root.parameters[0].value == NT.BOOL_DATA_TYPE and root.parameters[2].expression_type != ET.BOOL:
                raise_type_error(root.token_source)
            else:
                if len(self.SymbolDictionary) == 0 or root.parameters[1].parameters[0] not in self.SymbolDictionary:
                    # Add values into SymbolTable
                    self.SymbolDictionary[root.parameters[1].parameters[0]] = [root.parameters[0].value, root.parameters[2].parameters[0]]
                else:
                    # Find current identifier value in SymbolTable
                    if root.parameters[1].parameters[0] in self.SymbolDictionary:
                        raise_identifier_error(root.parameters[1].parameters[0], root.parameters[1].token_source)
                    elif root.parameters[1].parameters[0] not in self.SymbolDictionary:
                        raise_undeclaredVariable_error(root.parameters[1].parameters[0], root.token_source)
            return

        # CHECK EXPRESSION (Code block not yet final)
        if root.parameters[0] == NT.INT_LITERAL:
            root.expression_type = ET.INT

        # EXPRESSIONS 
        if root.value in {NT.ADD, NT.SUBTRACT, NT.MULTIPLY, NT.DIVIDE}:
            if root.parameters[0].expression_type != ET.INT or root.parameters[1].expression_type != ET.INT:
                if root.parameters[0].expression_type != ET.INT:    
                    raise_type_error(root.parameters[0].token_source)
                else:
                    raise_type_error(root.parameters[1].token_source)
            else:
                root.expression_type = ET.INT

        # UNARY EXPRESSION
        elif root.value == NT.NEGATE:
            if root.parameters[0].expression_type != ET.INT:
                raise_type_error(root.token_source)
            else:
                root.expression_type = ET.INT
            
        # EQUALITY OPERATORS
        elif root.value in {NT.EQUAL, NT.NOT_EQUAL}:
            if root.parameters[0].expression_type != root.parameters[1].expression_type:
                raise_type_error(root.token_source)
            else:
                root.expression_type = ET.BOOL
        # RELATIONAL OPERATORS      
        elif root.value in {NT.LESS, NT.MORE, NT.LESS_EQUAL, NT.MORE_EQUAL}:
            if root.parameters[0].expression_type != ET.INT or root.parameters[1].expression_type != ET.INT:
                raise_type_error(root.token_source)
            else:
                root.expression_type = ET.BOOL

        # LOGICAL OPERATORS
        elif root.value ==  NT.NOT:
            if root.parameters[0].expression_type != ET.BOOL:
                raise_type_error(root.parameters[0].token_source)
            else:
                root.expression_type = ET.BOOL
        elif root.value in {NT.AND, NT.OR}:
            if root.parameters[0].expression_type != ET.BOOL or root.parameters[1].expression_type != ET.BOOL:
                if root.parameters[0].expression_type != ET.BOOL:
                    raise_type_error(root.parameters[0].token_source)
                else:
                    raise_type_error(root.parameters[1].token_source)
            else:
                root.expression_type = ET.BOOL

        # SELECTION STATEMENTS
        elif root.value in {NT.IF, NT.ELIF}:
            if root.parameters[0].expression_type != ET.BOOL:
                raise_type_error(root.token_source)

        # FOR LOOP
        elif root.value == NT.FOR:
            if root.parameters[1].expression_type != ET.BOOL:
                raise_type_error(root.parameters[1].token_source)

        # WHILE LOOP
        elif root.value == NT.WHILE:
            if root.parameters[0].expression_type != ET.BOOL:
                raise_type_error(root.parameters[0].token_source)

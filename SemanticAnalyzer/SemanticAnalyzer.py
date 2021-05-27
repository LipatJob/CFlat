from Lib.Node import Node, NodeType as NT, ExpressionType as ET
from Lib.Token import Token
from Lib.ErrorHandler import *

class SemanticAnalyzer:
    SymbolDictionary = dict()



    def run(self, root: Node):

        # Added traversal function code for type checking
        # NOTE: Type checking for Assignment, Declaration and Input still pending

        if root == None: return

        # Terminal expressions for leaf nodes
        # If identifier, check key if it exists and data type in SymbolDictionary
        # Otherwise, throw an error
        elif root.value in {NT.IDENTIFIER, NT.INT_LITERAL, NT.STRING_LITERAL, NT.BOOL_LITERAL}:
            if root.value == NT.INT_LITERAL:
                root.expression_type = ET.INT
            elif root.value == NT.STRING_LITERAL:
                root.expression_type = ET.STRING
            elif root.value == NT.BOOL_LITERAL:
                root.expression_type = ET.BOOL
            elif root.value == NT.IDENTIFIER:
                
                # Check if identifier is in the SymbolDictionary
                if root.parameters[0] not in self.SymbolDictionary:
                    raise_undeclaredVariable_error(root.value)
                else:
                    root.expression_type = self.SymbolDictionary[root.parameters[0]][0]
            return
        
        # (Code block not yet final)
        if root.value == NT.DECLARATION:
            self.run(root.parameters[2])
        else:
            for x in root.parameters:
                self.run(x)

        # DECLARATION STATEMENT
        # Enter code for storing variables
        # Check if dictionary is empty
        # If empty, store node values in dictionary
        # If not empty, compare the value in the dictionary
        if root.value == NT.DECLARATION:
            if root.parameters[0].value == NT.INT_DATA_TYPE and root.parameters[2].expression_type != ET.INT:
                raise_type_error()
            elif root.parameters[0].value == NT.STRING_DATA_TYPE and root.parameters[2].expression_type != ET.STRING:
                raise_type_error()
            elif root.parameters[0].value == NT.BOOL_DATA_TYPE and root.parameters[2].expression_type != ET.BOOL:
                raise_type_error()
            else:
                if len(self.SymbolDictionary) == 0 or root.parameters[1] not in self.SymbolDictionary:
                    # Add values into SymbolTable

                    # (Code block not yet final)
                    self.SymbolDictionary[root.parameters[1].parameters[0]] = [root.parameters[0], root.parameters[2]]
                    
                    # self.SymbolTable.__add__(root.parameters[1])
                else:
                    # Find current identifier value in SymbolTable

                    # (Code block not yet final)
                    if root.parameters[1] in self.SymbolDictionary:
                        raise_identifier_error()
                    elif root.parameters[1] not in self.SymbolDictionary:
                        raise_undeclaredVariable_error(root.parameters[1])

                    # if root.parameters[1] in self.SymbolTable:
                    #     raise_identifier_error()
                    # elif root.parameters[1] not in self.SymbolTable:    
                    #     raise_undeclaredVariable_error(root.parameters[1])
            return

        # CHECK EXPRESSION (Code block not yet final)
        if root.parameters[0] == NT.INT_LITERAL:
            root.expression_type = ET.INT

        # EXPRESSIONS 
        if root.value in {NT.ADD, NT.SUBTRACT, NT.MULTIPLY, NT.DIVIDE}:
            if root.parameters[0].expression_type != ET.INT or root.parameters[1].expression_type != ET.INT:
                raise_type_error()
            else:
                root.expression_type = ET.INT

        # UNARY EXPRESSION
        elif root.value == NT.NEGATE:
            if root.parameters[0].expression_type != ET.INT:
                raise_type_error()
            else:
                root.expression_type = ET.INT
            
        # EQUALITY OPERATORS
        elif root.value in {NT.EQUAL, NT.NOT_EQUAL,}:
            if root.parameters[0].expression_type != root.parameters[1].expression_type:
                raise_type_error()
            else:
                root.expression_type = ET.BOOL
        # RELATIONAL OPERATORS      
        elif root.value in {NT.LESS, NT.MORE, NT.LESS_EQUAL, NT.MORE_EQUAL}:
            if root.parameters[0].expression_type != ET.INT or root.parameters[1].expression_type != ET.INT:
                raise_type_error()
            else:
                root.expression_type = ET.BOOL

        # LOGICAL OPERATORS
        elif root.value ==  NT.NOT:
            if root.parameters[0].expression_type != ET.BOOL:
                raise_type_error()
            else:
                root.expression_type = ET.BOOL
        elif root.value in {NT.AND, NT.OR}:
            if root.parameters[0].expression_type != ET.BOOL or root.parameters[1].expression_type != ET.BOOL:
                raise_type_error()
            else:
                root.expression_type = ET.BOOL

        # SELECTION STATEMENTS
        elif root.value in {NT.IF, NT.ELIF}:
            if root.parameters[0].expression_type != ET.BOOL:
                raise_type_error()

        # FOR LOOP
        elif root.value == NT.FOR:
            if root.parameters[1].expression_type != ET.BOOL:
                raise_type_error()

        # WHILE LOOP
        elif root.value == NT.WHILE:
            if root.parameters[0].expression_type != ET.BOOL:
                raise_type_error()

from Lib.Node import Node, NodeType as NT, ExpressionType as ET
from Lib.Token import Token
from Lib.ErrorHandler import *

class SemanticAnalyzer:
    def run(self, root: Node):

        # Added traversal function code for type checking
        # NOTE: Type checking for Assignment, Declaration and Input still pending

        if root == None: return

        elif root.value in {NT.IDENTIFIER, NT.INT_LITERAL, NT.STRING_LITERAL, NT.BOOL_LITERAL}:
            if root.value == NT.INT_LITERAL:
                root.expression_type = ET.INT
            if root.value == NT.STRING_LITERAL:
                root.expression_type = ET.STRING
            if root.value == NT.BOOL_LITERAL:
                root.expression_type = ET.BOOL
        
        for x in root.parameters:
            self.run(x)

        # EXPRESSIONS 
        if root.value in {NT.ADD, NT.SUBTRACT, NT.MULTIPLY, NT.DIVIDE}:
            if root.parameters[0].expression_type != ET.INT OR root.parameters[1].expression_type != ET.INT:
                raise_type_error()
            else:
                root.expression_type = ET.INT

        # UNARY EXPRESSION
        if root.value == NT.NEGATE:
            if root.parameters[0].expression_type != ET.INT:
                raise_type_error()
            else:
                root.expression_type = ET.INT
            
        # RELATIONAL OPERATORS
        if root.value in {NT.DOUBLE_EQUAL, NT.EQUAL, NT.NOT_EQUAL, NT.LESS, NT.MORE, NT.LESS_EQUAL, NT.MORE_EQUAL}:
            if root.parameters[0].expression_type != ET.INT OR root.parameters[1].expression_type != ET.INT:
                raise_type_error()
            else:
                root.expression_type = ET.INT

        # LOGICAL OPERATORS
        if root.value in {NT.AND, NT.OR, NT.NOT}:
            if root.parameters[0].expression_type != ET.BOOL OR root.parameters[1].expression_type != ET.BOOL:
                raise_type_error()
            else:
                root.expression_type = ET.BOOL

        # SELECTION STATEMENTS
        if root.value in {NT.IF, NT.ELIF}:
            if root.parameters[0].expression_type != ET.BOOL:
                raise_type_error()

        # FOR LOOP
        if root.value == NT.FOR:
            if root.parameters[1].expression_type != ET.BOOL:
                raise_type_error()

        # WHILE LOOP
        if root.value == NT.WHILE:
            if root.parameters[0].expression_type != ET.BOOL:
                raise_type_error()

    """
    Node(NT.MULTIPLY, [
    Node(NT.ADD, [
        Node(NT.INT_LITERAL, [3]),
        Node(NT.INT_LITERAL, [4])]),
    Node(NT.INT_LITERAL, [2])])

    """
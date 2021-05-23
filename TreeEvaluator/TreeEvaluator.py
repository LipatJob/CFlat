from Lib.Node import Node, NodeType as NT, ExpressionType as ET
from Lib.Token import Token

class SymbolTable:
    table = []

    def bind(self, identifier, value, data_type):
        self.table.append([identifier, value, data_type])

    def lookup(self, identifier):
        for item in self.table:
            if item[0] == identifier:
                return item[1]
        else:
            return False

class TreeEvaluator:
    symbol_table = SymbolTable()

    def run(self, root: Node):
        if root:
            program = self.evaluate(root)
            exec(program)

        return
    
    def evaluate(self, node):
        if node.value == NT.PROGRAM:
            program = ""

            for child in node.parameters:
                program = self.evaluate(child)
            
            return program

        if node.value == NT.STATEMENT:
            sProgram = ""

            for child in node.parameters:
                line = self.evaluate(child)
                if line:
                    sProgram += "\n" + line
            
            return sProgram

        if node.value == NT.BLOCK:
            pass

        if node.value in {NT.IDENTIFIER, NT.INT_LITERAL, NT.STRING_LITERAL, NT.BOOL_LITERAL}:
            return node.parameters[0]

        if node.value == NT.DECLARATION:
            id = self.evaluate(node.parameters[1])
            val = self.evaluate(node.parameters[2])
            type = node.parameters[0].value
            self.symbol_table.bind(id, val, type)

        if node.value == NT.ASSIGNMENT:
            pass

        if node.value == NT.PRINT:
            if node.parameters[0].value == NT.IDENTIFIER:
                return "print(\"" + str(self.symbol_table.lookup(self.evaluate(node.parameters[0]))) + "\")"
                
            return "print(\"" + str(self.evaluate(node.parameters[0])) + "\")"

        if node.value == NT.INPUT:
            pass

        if node.value == NT.FOR:
            pass

        if node.value == NT.WHILE:
            pass

        if node.value == NT.IF:
            pass

        if node.value == NT.NEGATE:
            pass

        if node.value == NT.ADD:
            return self.evaluate(node.parameters[0]) + self.evaluate(node.parameters[1])

        if node.value == NT.SUBTRACT:
            pass

        if node.value == NT.MULTIPLY:
            pass

        if node.value == NT.DIVIDE:
            pass

        if node.value == NT.EQUAL:
            pass

        if node.value == NT.AND:
            pass

        if node.value == NT.OR:
            pass

        if node.value == NT.NOT:
            pass

        if node.value == NT.DOUBLE_EQUAL:
            pass

        if node.value == NT.NOT_EQUAL:
            pass

        if node.value == NT.LESS:
            pass

        if node.value == NT.MORE:
            pass

        if node.value == NT.LESS_EQUAL:
            pass

        if node.value == NT.MORE_EQUAL:
            pass

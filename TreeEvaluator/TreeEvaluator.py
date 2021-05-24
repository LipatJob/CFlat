from Lib.Node import Node, NodeType as NT, ExpressionType as ET
from Lib.Token import Token

class SymbolTable:
    table = []

    def bind(self, identifier, value):
        self.table.append([identifier, value])

    def lookup(self, identifier):
        for item in self.table:
            if item[0] == identifier:
                return item[1]
        else:
            return False

    def assign(self, identifier, value):
        for item in self.table:
            if item[0] == identifier:
                item[1] = value
                return

class TreeEvaluator:
    symbol_table = SymbolTable()

    def run(self, root: Node):
        if root:
            program = self.evaluate(root)
            exec(program)

        return
    
    def evaluate(self, node, returnStatement = False):
        if node.value == NT.PROGRAM:
            program = ""

            for child in node.parameters:
                program = self.evaluate(child)
            
            return program

        if node.value in {NT.STATEMENT, NT.BLOCK}:
            sProgram = ""

            for child in node.parameters:
                line = self.evaluate(child)
                if line:
                    sProgram += "\n" + line
            
            return sProgram

        if node.value == NT.IDENTIFIER:
            if returnStatement:
                return node.parameters[0]

            return self.symbol_table.lookup(node.parameters[0])

        if node.value in {NT.INT_LITERAL, NT.BOOL_LITERAL}:
            return node.parameters[0]

        if node.value == NT.STRING_LITERAL:
            return "\"" + node.parameters[0] + "\""

        if node.value == NT.DECLARATION:
            id = self.evaluate(node.parameters[1], True)
            val = self.evaluate(node.parameters[2])
            self.symbol_table.bind(id, val)

        if node.value == NT.ASSIGNMENT:
            id = self.evaluate(node.parameters[0], True)
            val = self.evaluate(node.parameters[1])
            self.symbol_table.assign(id, val)

        if node.value == NT.PRINT:
            return "print(" + str(self.evaluate(node.parameters[0])) + ")"

        if node.value == NT.INPUT: # NOT DONE
            return "input()"

        if node.value == NT.WHILE:
            whileStatement = ""
            while self.evaluate(node.parameters[0]):
                whileStatement += "\n" + self.evaluate(node.parameters[1])
            return whileStatement

        if node.value == NT.FOR:
            forStatement = ""
            self.evaluate(node.parameters[0])
            while self.evaluate(node.parameters[1]):
                forStatement += "\n" + self.evaluate(node.parameters[3])
                self.evaluate(node.parameters[2])
            return forStatement

        if node.value in {NT.IF, NT.ELIF}:
            if (self.evaluate(node.parameters[0])):
                return self.evaluate(node.parameters[1])
            
            if node.parameters[2]:
                return self.evaluate(node.parameters[2])

        if node.value == NT.ELSE:
            return self.evaluate(node.parameters[0])

        if node.value == NT.NEGATE:
            return - self.evaluate(node.parameters[0])

        if node.value == NT.ADD:
            return self.evaluate(node.parameters[0]) + self.evaluate(node.parameters[1])

        if node.value == NT.SUBTRACT:
            return self.evaluate(node.parameters[0]) - self.evaluate(node.parameters[1])

        if node.value == NT.MULTIPLY:
            return self.evaluate(node.parameters[0]) * self.evaluate(node.parameters[1])

        if node.value == NT.DIVIDE:
            return int(self.evaluate(node.parameters[0]) / self.evaluate(node.parameters[1]))

        if node.value == NT.AND:
            if self.evaluate(node.parameters[0]) and self.evaluate(node.parameters[1]):
                return True
            else:
                return False

        if node.value == NT.OR:
            if self.evaluate(node.parameters[0]) or self.evaluate(node.parameters[1]):
                return True
            else:
                return False

        if node.value == NT.NOT:
            if not self.evaluate(node.parameters[0]):
                return True
            else:
                return False

        if node.value == NT.DOUBLE_EQUAL:
            if self.evaluate(node.parameters[0]) == self.evaluate(node.parameters[1]):
                return True
            else:
                return False

        if node.value == NT.NOT_EQUAL:
            if self.evaluate(node.parameters[0]) != self.evaluate(node.parameters[1]):
                return True
            else:
                return False

        if node.value == NT.LESS:
            if self.evaluate(node.parameters[0]) < self.evaluate(node.parameters[1]):
                return True
            else:
                return False

        if node.value == NT.MORE:
            if self.evaluate(node.parameters[0]) > self.evaluate(node.parameters[1]):
                return True
            else:
                return False

        if node.value == NT.LESS_EQUAL:
            if self.evaluate(node.parameters[0]) <= self.evaluate(node.parameters[1]):
                return True
            else:
                return False

        if node.value == NT.MORE_EQUAL:
            if self.evaluate(node.parameters[0]) >= self.evaluate(node.parameters[1]):
                return True
            else:
                return False

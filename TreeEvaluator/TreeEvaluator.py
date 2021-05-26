from Lib.Node import Node, NodeType as NT

class SymbolTable:
    table = []

    # Add new item to symbol table
    def bind(self, identifier, value, data_type):
        self.table.append([identifier, value, data_type])

    # Return value of an identifier
    def lookup(self, identifier):
        for item in self.table:
            if item[0] == identifier:
                return item[1]
        else:
            return False

    # Change value of an identifier
    def assign(self, identifier, value):
        for item in self.table:
            if item[0] == identifier:
                item[1] = value
                return

class TreeEvaluator:
    def __init__(self):
        self.printed_values = []
        self.symbol_table = SymbolTable()

    def output(self, value, end = "\n"):
        self.printed_values.append(value + end)
        print(value, end = end)

    def run(self, root: Node):
        if root:
            self.evaluate(root)
        
        return "".join(self.printed_values)
    
    # Recursive function
    def evaluate(self, node):
        if node.value in {NT.PROGRAM, NT.STATEMENT, NT.BLOCK}:
            for child in node.parameters:
                self.evaluate(child)

        ## VALUES

        if node.value in {NT.INT_LITERAL, NT.STRING_LITERAL, NT.BOOL_LITERAL}:
            return node.parameters[0]

        if node.value == NT.IDENTIFIER:
            return self.symbol_table.lookup(node.parameters[0])

        if node.value == NT.INPUT:
            return input()

        ## STATEMENTS

        if node.value == NT.DECLARATION:
            id = node.parameters[1].parameters[0]
            val = self.evaluate(node.parameters[2])
            type = node.parameters[0].value
            self.symbol_table.bind(id, val, type)

        if node.value == NT.ASSIGNMENT:
            id = node.parameters[0].parameters[0]
            val = self.evaluate(node.parameters[1])
            self.symbol_table.assign(id, val)

        if node.value == NT.PRINT:
            self.output(self.evaluate(node.parameters[0]))

        if node.value == NT.WHILE:
            while self.evaluate(node.parameters[0]):
                self.evaluate(node.parameters[1])

        if node.value == NT.FOR:
            self.evaluate(node.parameters[0])
            while self.evaluate(node.parameters[1]):
                self.evaluate(node.parameters[3])
                self.evaluate(node.parameters[2])

        if node.value in {NT.IF, NT.ELIF}:
            if (self.evaluate(node.parameters[0])):
                self.evaluate(node.parameters[1])
                return
            
            if node.parameters[2]:
                self.evaluate(node.parameters[2])

        if node.value == NT.ELSE:
            self.evaluate(node.parameters[0])

        ## OPERATORS

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

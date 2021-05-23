from Lib.Node import Node
from Lib.Token import Token

class TreeEvaluator:
    def run(self, root: Node, symbol_table = None):
        if root:
            self.traverse(root)

        return
    
    def traverse(self, node):
        print()
        print(node.value)

        if node.expression_type:
            print(node.expression_type)

        if node.parameters:
            for child in node.parameters:
                self.traverse(child)

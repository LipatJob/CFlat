from TreeEvaluator.TreeEvaluator import TreeEvaluator
from Lib.Token import *
from Lib.Token import TokenType as TT
from Lib.Node import Node, NodeType as NT, ExpressionType as ET

# int a = 1 + 2;
tree = Node(NT.PROGRAM, [
    Node(NT.STATEMENT, [
        Node(NT.DECLARATION, [
            Node(NT.IDENTIFIER, [Node(NT.STRING_LITERAL, [Node("a", [])])]),
            Node(NT.ADD, [
                Node(NT.INT_LITERAL, [Node(1, [])]),
                Node(NT.INT_LITERAL, [Node(2, [])])
            ])
        ], ET.INT)
    ])
])

evaluator = TreeEvaluator()
evaluator.run(tree)
from TreeEvaluator.TreeEvaluator import TreeEvaluator
from Lib.Token import *
from Lib.Token import TokenType as TT
from Lib.Node import Node, NodeType as NT, ExpressionType as ET
"""
# print("Hello world!");
tree = Node(NT.PROGRAM, [
    Node(NT.STATEMENT, [
        Node(NT.PRINT, [
            Node(NT.STRING_LITERAL, ["Hello world!"])
        ]),
        Node(NT.STATEMENT, [
            Node(NT.PRINT, [
                Node(NT.STRING_LITERAL, ["How are you?"])
            ])
        ])
    ])
])
"""
# int a = 1 + 2;
# print(a);
tree = Node(NT.PROGRAM, [
    Node(NT.STATEMENT, [
        Node(NT.DECLARATION, [
            Node(NT.INT_DATA_TYPE, []),
            Node(NT.IDENTIFIER, ["a"]),
            Node(NT.ADD, [
                Node(NT.INT_LITERAL, [1]),
                Node(NT.INT_LITERAL, [2])
            ])
        ], ET.INT),
        Node(NT.STATEMENT, [
            Node(NT.PRINT, [
                Node(NT.IDENTIFIER, ["a"])
            ])
        ])
    ])
])
"""
# for (i = 0; i < 10; i++) { <body> }
tree = Node(NT.PROGRAM, [
    Node(NT.STATEMENT, [
        Node(NT.FOR, [
            Node(NT.DECLARATION, [
                Node(NT.INT_DATA_TYPE, []),
                Node(NT.IDENTIFIER, ["i"]),
                Node(NT.INT_LITERAL, [0])
            ], ET.INT),
            Node(NT.LESS, [
                Node(NT.IDENTIFIER, ["i"]),
                Node(NT.INT_LITERAL, [10])
            ]),
            Node(NT.ASSIGNMENT, [
                Node(NT.IDENTIFIER, ["i"]),
                Node(NT.ADD, [
                    Node(NT.IDENTIFIER, ["i"]),
                    Node(NT.INT_LITERAL, [1])
                ])
            ]),
            Node(NT.BLOCK, [
                # <body>
            ])
        ])
    ])
])
"""

evaluator = TreeEvaluator()
evaluator.run(tree)
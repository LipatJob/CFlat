from TreeEvaluator.TreeEvaluator import TreeEvaluator
from Lib.Node import Node, NodeType as NT, ExpressionType as ET
"""
# print("Hello world!");
# print("How are you?");
tree = Node(NT.PROGRAM, [
    Node(NT.BLOCK, [
        Node(NT.STATEMENT, [
            Node(NT.PRINT, [
                Node(NT.STRING_LITERAL, ["Hello world!"])
            ])
        ]),
        Node(NT.STATEMENT, [
            Node(NT.PRINT, [
                Node(NT.STRING_LITERAL, ["How are you?"])
            ])
        ])
    ])
])

# int a = 2 - 1;
# set a = a + 3;
# print(a);
tree = Node(NT.PROGRAM, [
    Node(NT.BLOCK, [
        Node(NT.STATEMENT, [
            Node(NT.DECLARATION, [
                Node(NT.INT_DATA_TYPE, []),
                Node(NT.IDENTIFIER, ["a"]),
                Node(NT.SUBTRACT, [
                    Node(NT.INT_LITERAL, [2]),
                    Node(NT.INT_LITERAL, [1])
                ])
            ])
        ]),
        Node(NT.STATEMENT, [
            Node(NT.ASSIGNMENT, [
                Node(NT.IDENTIFIER, ["a"]),
                Node(NT.ADD, [
                    Node(NT.IDENTIFIER, ["a"]),
                    Node(NT.INT_LITERAL, [3])
                ])
            ])
        ]), 
        Node(NT.STATEMENT, [
            Node(NT.PRINT, [
                Node(NT.IDENTIFIER, ["a"])
            ])
        ])
    ])
])

# for (int i = 0; i < 10; set i = i + 1) { print(i); }
tree = Node(NT.PROGRAM, [
    Node(NT.BLOCK, [
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
                    Node(NT.STATEMENT, [
                        Node(NT.PRINT, [
                            Node(NT.IDENTIFIER, ["i"])
                        ])
                    ])
                ])
            ])
        ])
    ])
])

# int i = 0;
# while(i < 5) { 
# print(i);
# set i = i + 1;
# }
tree = Node(NT.PROGRAM, [
    Node(NT.BLOCK, [
        Node(NT.STATEMENT, [
            Node(NT.DECLARATION, [
                Node(NT.INT_DATA_TYPE, []),
                Node(NT.IDENTIFIER, ["i"]),
                Node(NT.INT_LITERAL, [0])
            ])
        ]), 
        Node(NT.STATEMENT, [
            Node(NT.WHILE, [
                Node(NT.LESS, [
                    Node(NT.IDENTIFIER, ["i"]),
                    Node(NT.INT_LITERAL, [5])
                ]),
                Node(NT.BLOCK, [
                    Node(NT.STATEMENT, [
                        Node(NT.PRINT, [Node(NT.IDENTIFIER, ["i"])])
                    ]), 
                    Node(NT.STATEMENT, [
                        Node(NT.ASSIGNMENT, [
                            Node(NT.IDENTIFIER, ["i"]),
                            Node(NT.ADD, [
                                Node(NT.IDENTIFIER, ["i"]),
                                Node(NT.INT_LITERAL, [1])
                            ])
                        ])
                    ])
                ])
            ])
        ])
    ])
])

# if (10 == 10) { print(1); }
# elif (True) { print(2); }
# else { print(3); }
tree = Node(NT.PROGRAM, [
    Node(NT.BLOCK, [
        Node(NT.STATEMENT, [
            Node(NT.IF, [
                Node(NT.DOUBLE_EQUAL, [
                    Node(NT.INT_LITERAL, [10]),
                    Node(NT.INT_LITERAL, [10])
                ]),
                Node(NT.BLOCK, [
                    Node(NT.STATEMENT, [
                        Node(NT.PRINT, [Node(NT.INT_LITERAL, [1])])
                    ])
                ]),
                Node(NT.ELIF, [
                    Node(NT.BOOL_LITERAL, [True]),
                    Node(NT.BLOCK, [
                        Node(NT.STATEMENT, [
                            Node(NT.PRINT, [Node(NT.INT_LITERAL, [2])])
                        ])
                    ]),
                    Node(NT.ELSE, [
                        Node(NT.BLOCK, [
                            Node(NT.STATEMENT, [
                                Node(NT.PRINT, [Node(NT.INT_LITERAL, [3])])
                            ])
                        ])
                    ])
                ])
            ])
        ])
    ])
])
"""
# print("Enter a number:");
# int x = input();
# print(x);
tree = Node(NT.PROGRAM, [
    Node(NT.BLOCK, [
        Node(NT.STATEMENT, [
            Node(NT.PRINT, [
                Node(NT.STRING_LITERAL, ["Enter a number:"])
            ])
        ]),
        Node(NT.STATEMENT, [
            Node(NT.DECLARATION, [
                Node(NT.INT_DATA_TYPE, []),
                Node(NT.IDENTIFIER, ["x"]),
                Node(NT.INPUT, [])
            ])
        ]),
        Node(NT.STATEMENT, [
            Node(NT.PRINT, [
                Node(NT.IDENTIFIER, ["x"])
            ])
        ])
    ])
])


evaluator = TreeEvaluator()
evaluator.run(tree)
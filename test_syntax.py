from SyntaxAnalyzer.SyntaxAnalyzer import SyntaxAnalyzer
from Lib.Token import *
from Lib.Token import TokenType as TT

tokens = [
    Token(TT.MINUS, "-"),
    Token(TT.INT_LITERAL, "1"),
    Token(TT.PLUS,"+"),
    Token(TT.INT_LITERAL, "1"),
    Token(TT.STAR,"*"),
    Token(TT.INT_LITERAL, "1"),
    Token(TT.MINUS,"-"),
    Token(TT.INT_LITERAL, "1"),
    Token(TT.SEMI_COLON, ";"),
]

analyzer = SyntaxAnalyzer()

root = analyzer.run(tokens)
print("----------")
analyzer.print_tree(root)
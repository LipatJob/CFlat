from SyntaxAnalyzer.SyntaxAnalyzer import SyntaxAnalyzer
from Lib.Token import Token


tokens = [
    Token("-", "-"),
    Token("literal", "1"),
    Token("+","+"),
    Token("literal", "1"),
    Token("*","*"),
    Token("literal", "1"),
    Token("-","-"),
    Token("literal", "1"),
    Token(";", ";"),
]

analyzer = SyntaxAnalyzer()

root = analyzer.run(tokens)
print("----------")
analyzer.print_tree(root)
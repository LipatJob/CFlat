from LexicalAnalyzer.LexicalAnalyzer import LexicalAnalyzer
from SemanticAnalyzer.SemanticAnalyzer import  SemanticAnalyzer
from SyntaxAnalyzer.SyntaxAnalyzer import SyntaxAnalyzer

def __main__():
    lexer = LexicalAnalyzer()
    parser = SyntaxAnalyzer()
    semanticAnalyzer = SemanticAnalyzer()

    file_name = ""

    tokens = lexer.run(file_name)
    tree = parser.run(tokens)
    semanticAnalyzer.run(tree)

__main__()
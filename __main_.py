from LexicalAnalyzer.LexicalAnalyzer import LexicalAnalyzer
from SemanticAnalyzer.SemanticAnalyzer import  SemanticAnalyzer
from SyntaxAnalyzer.SyntaxAnalyzer import SyntaxAnalyzer
from TreeEvaluator.TreeEvaluator import TreeEvaluator

def __main__():
    lexer = LexicalAnalyzer()
    parser = SyntaxAnalyzer()
    semanticAnalyzer = SemanticAnalyzer()
    evaluator = TreeEvaluator()

    file_name = ""

    tokens = lexer.run(file_name)
    tree = parser.run(tokens)
    symbol_table = semanticAnalyzer.run(tree)
    evaluator.run(tree, symbol_table)

__main__()
from LexicalAnalyzer.LexicalAnalyzer import LexicalAnalyzer
from SemanticAnalyzer.SemanticAnalyzer import  SemanticAnalyzer
from SyntaxAnalyzer.SyntaxAnalyzer import SyntaxAnalyzer
from TreeEvaluator.TreeEvaluator import TreeEvaluator

def __main__():
    lexer = LexicalAnalyzer()
    parser = SyntaxAnalyzer()
    semanticAnalyzer = SemanticAnalyzer()
    evaluator = TreeEvaluator()

    file_name = "fib.cf"

    tokens = lexer.run(file_name)
    tree = parser.run(tokens)
    semanticAnalyzer.run(tree)
    evaluator.run(tree)

if __name__ == "__main__":
    __main__()
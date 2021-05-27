from LexicalAnalyzer.LexicalAnalyzer import LexicalAnalyzer
from SemanticAnalyzer.SemanticAnalyzer import  SemanticAnalyzer
from SyntaxAnalyzer.SyntaxAnalyzer import SyntaxAnalyzer
from TreeEvaluator.TreeEvaluator import TreeEvaluator

def __main__():
    lexer = LexicalAnalyzer()
    parser = SyntaxAnalyzer()
    semanticAnalyzer = SemanticAnalyzer()
    evaluator = TreeEvaluator()

    file_name = "./Tests/Working/testcase_5.cf"

    tokens = lexer.run(file_name)
    tree = parser.run(tokens)
    semanticAnalyzer.run(tree)
    evaluator.run(tree)

__main__()
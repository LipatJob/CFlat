from LexicalAnalyzer.LexicalAnalyzer import LexicalAnalyzer
from SyntaxAnalyzer.SyntaxAnalyzer import SyntaxAnalyzer
from SemanticAnalyzer.SemanticAnalyzer import SemanticAnalyzer 
from TreeEvaluator.TreeEvaluator import TreeEvaluator
import Lib.OutputFormatter as Oformatter
lexer = LexicalAnalyzer()
parser = SyntaxAnalyzer()
analyzer = SemanticAnalyzer()
evaluator = TreeEvaluator()


file_name = "program.cf"

tokens = lexer.run(file_name)
tree = parser.run(tokens)
symbol_table = analyzer.run(tree)
evaluated_symbol_table = evaluator.run(tree)

Oformatter.display_evaluated_symbol_table(evaluator.symbol_table)

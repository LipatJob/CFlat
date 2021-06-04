from LexicalAnalyzer.LexicalAnalyzer import LexicalAnalyzer
from SyntaxAnalyzer.SyntaxAnalyzer import SyntaxAnalyzer
from SemanticAnalyzer.SemanticAnalyzer import SemanticAnalyzer 
import Lib.OutputFormatter as Oformatter
lexer = LexicalAnalyzer()
parser = SyntaxAnalyzer()
analyzer = SemanticAnalyzer()


file_name = "program.cf"

tokens = lexer.run(file_name)
tree = parser.run(tokens)
symbol_table = analyzer.run(tree)

Oformatter.display_semantic_symbol_table(symbol_table)

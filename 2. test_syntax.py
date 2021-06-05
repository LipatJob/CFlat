from Lib import OutputFormatter
from LexicalAnalyzer.LexicalAnalyzer import LexicalAnalyzer
from SyntaxAnalyzer.SyntaxAnalyzer import SyntaxAnalyzer
import Lib.OutputFormatter as Oformatter
lexer = LexicalAnalyzer()
parser = SyntaxAnalyzer()

file_name = "syntax_program.cf"

tokens = lexer.run(file_name)
tree = parser.run(tokens)

Oformatter.print_tree(tree)
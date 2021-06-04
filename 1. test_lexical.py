from Lib import OutputFormatter
from LexicalAnalyzer.LexicalAnalyzer import LexicalAnalyzer
from SyntaxAnalyzer.SyntaxAnalyzer import SyntaxAnalyzer
import Lib.OutputFormatter as Oformatter
lexer = LexicalAnalyzer()
parser = SyntaxAnalyzer()

file_name = "program.cf"

tokens = lexer.run(file_name)

Oformatter.display_tokens(tokens)

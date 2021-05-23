from LexicalAnalyzer.LexicalAnalyzer import LexicalAnalyzer
from SyntaxAnalyzer.SyntaxAnalyzer import SyntaxAnalyzer
from pprint import pprint
lexer = LexicalAnalyzer()
parser = SyntaxAnalyzer()

file_name = "syntax_program.txt"

tokens = lexer.run(file_name)

print("TOKENS:")
pprint(tokens)
print("END OF TOKENS")

tree = parser.run(tokens)

parser.print_tree(tree)

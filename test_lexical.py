from LexicalAnalyzer.LexicalAnalyzer import LexicalAnalyzer
from Lib.Token import *

analyzer = LexicalAnalyzer()
root = analyzer.run("kk.txt")
for i in root:
    print(i)
import glob
import unittest
from LexicalAnalyzer.LexicalAnalyzer import LexicalAnalyzer
from SemanticAnalyzer.SemanticAnalyzer import  SemanticAnalyzer
from SyntaxAnalyzer.SyntaxAnalyzer import SyntaxAnalyzer
from TreeEvaluator.TreeEvaluator import TreeEvaluator

def run_compiler(file_name):
        lexer = LexicalAnalyzer()
        parser = SyntaxAnalyzer()
        semanticAnalyzer = SemanticAnalyzer()
        evaluator = TreeEvaluator()

        print(file_name)

        tokens = lexer.run(file_name)
        tree = parser.run(tokens)
        semanticAnalyzer.run(tree)
        evaluator.run(tree)

class TestSyntaxAnalayzer(unittest.TestCase):
    def test1(self):
        filenames = glob.glob("Tests/SyntaxAnalyzer/testcase*.cf")
        for filename in filenames:
            with self.subTest(filename=filename):
                self.assertRaises(Exception, run_compiler, filename)

class TestSemanticAnalyzer(unittest.TestCase):
    def test1(self):
        filenames = glob.glob("Tests/SemanticAnalyzer/testcase*.cf")
        for filename in filenames:
            with self.subTest(filename=filename):
                self.assertRaises(Exception, run_compiler, filename)

class TestLexicalAnalyzer(unittest.TestCase):
    def test1(self):
        filenames = glob.glob("Tests/LexicalAnalyzer/testcase*.cf")
        for filename in filenames:
            with self.subTest(filename=filename):
                self.assertRaises(Exception, run_compiler, filename)

class TestWorking(unittest.TestCase):
    def test1(self):
        filenames = glob.glob("Tests/Working/testcase*.cf")
        for filename in filenames:
            with self.subTest(filename=filename):
                self.assertRaises(Exception, run_compiler, filename)
        
unittest.main()
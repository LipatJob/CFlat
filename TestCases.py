import glob
import unittest
from unittest.mock import patch 
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
        return evaluator.run(tree)

class TestSyntaxAnalayzer(unittest.TestCase):
    @patch("builtins.input")
    def test1(self, mocked_input):
        test_inputs = [
        ]

        filenames = glob.glob("Tests/SyntaxAnalyzer/testcase*.cf")
        filenames.sort()
        for test_input, filename in zip(test_inputs, filenames):
            with self.subTest(filename=filename):
                mocked_input.side_effect = test_input
                self.assertRaises(Exception, run_compiler, filename)

class TestSemanticAnalyzer(unittest.TestCase):
    @patch("builtins.input")
    def test1(self, mocked_input):
        test_inputs = [
        ]

        filenames = glob.glob("Tests/SemanticAnalyzer/testcase*.cf")
        filenames.sort()
        for test_input, filename in zip(test_inputs, filenames):
            with self.subTest(filename=filename):
                mocked_input.side_effect = test_input
                self.assertRaises(Exception, run_compiler, filename)

class TestLexicalAnalyzer(unittest.TestCase):
    @patch("builtins.input")
    def test1(self, mocked_input):
        test_inputs = [
        ]

        filenames = glob.glob("Tests/LexicalAnalyzer/testcase*.cf")
        filenames.sort()
        for test_input, filename in zip(test_inputs, filenames):
            with self.subTest(filename=filename):
                mocked_input.side_effect = test_input
                self.assertRaises(Exception, run_compiler, filename)

class TestWorking(unittest.TestCase):
    

    @patch("builtins.input")
    def test1(self, mocked_input):
        test_inputs = [
        ]

        expected_outputs = [
            '"Hello world!"\n"Have a good day!"\n'
        ]

        filenames = glob.glob("Tests/Working/testcase*.cf")
        filenames.sort()
        for test_input, expected_output, filename in zip(test_inputs, expected_outputs, filenames):
            with self.subTest(filename=filename):
                mocked_input.side_effect = test_input
                self.assertEquals(expected_output, run_compiler(filename))
        
unittest.main()
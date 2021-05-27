import glob
import unittest
from unittest.mock import patch 
from LexicalAnalyzer.LexicalAnalyzer import LexicalAnalyzer
from SemanticAnalyzer.SemanticAnalyzer import  SemanticAnalyzer
from SyntaxAnalyzer.SyntaxAnalyzer import SyntaxAnalyzer
from TreeEvaluator.TreeEvaluator import TreeEvaluator
import Lib.TestCaseParser as InOut
def run_compiler(file_name):
        lexer = LexicalAnalyzer()
        parser = SyntaxAnalyzer()
        semanticAnalyzer = SemanticAnalyzer()
        evaluator = TreeEvaluator()


        tokens = lexer.run(file_name)
        tree = parser.run(tokens)

        semanticAnalyzer.run(tree)
        return evaluator.run(tree)

class TestSyntaxAnalayzer(unittest.TestCase):
    @patch("builtins.input")
    def test1(self, mocked_input):
        with open("Tests/SyntaxAnalyzer/input_output.txt") as f:
            filenames, test_inputs, expected_outputs = InOut.parse(f.read())

        for test_input, filename in zip(test_inputs, filenames):
            with self.subTest(filename=filename):
                mocked_input.side_effect = test_input
                self.assertRaises(Exception, run_compiler, "Tests/SyntaxAnalyzer/"+filename)
        print(f"Syntax Analyzer: Executed {len(filenames)} test cases")

class TestSemanticAnalyzer(unittest.TestCase):
    @patch("builtins.input")
    def test1(self, mocked_input):
        with open("Tests/SemanticAnalyzer/input_output.txt") as f:
            filenames, test_inputs, expected_outputs = InOut.parse(f.read())

        for test_input, filename in zip(test_inputs, filenames):
            with self.subTest(filename=filename):
                mocked_input.side_effect = test_input
                self.assertRaises(Exception, run_compiler, "Tests/SemanticAnalyzer/"+filename)
        print(f"Semantic Analyzer: Executed {len(filenames)} test cases")

class TestLexicalAnalyzer(unittest.TestCase):
    @patch("builtins.input")
    def test1(self, mocked_input):
        with open("Tests/LexicalAnalyzer/input_output.txt") as f:
            filenames, test_inputs, expected_outputs = InOut.parse(f.read())

        for test_input, filename in zip(test_inputs, filenames):
            with self.subTest(filename=filename):
                mocked_input.side_effect = test_input
                self.assertRaises(Exception, run_compiler, "Tests/LexicalAnalyzer/"+filename)
        print(f"Lexical Analyzer: Executed {len(filenames)} test cases")

class TestWorking(unittest.TestCase):
    @patch("builtins.input")
    def test1(self, mocked_input):
        with open("Tests/Working/input_output.txt") as f:
            filenames, test_inputs, expected_outputs = InOut.parse(f.read())

        for test_input, expected_output, filename in zip(test_inputs, expected_outputs, filenames):
            with self.subTest(filename=filename):
                mocked_input.side_effect=test_input

                actual = run_compiler("Tests/Working/"+filename)
                self.assertEquals(expected_output, actual)
        print(f"Working: Executed {len(filenames)} test cases")
        
unittest.main()
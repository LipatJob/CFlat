import glob
import unittest
from unittest.mock import patch
from LexicalAnalyzer.LexicalAnalyzer import LexicalAnalyzer
from SemanticAnalyzer.SemanticAnalyzer import SemanticAnalyzer
from SyntaxAnalyzer.SyntaxAnalyzer import SyntaxAnalyzer
from TreeEvaluator.TreeEvaluator import TreeEvaluator
import Lib.TestCaseParser as InOut
import Lib.TestCaseParser2 as TestParser
from Lib.ErrorHandler import *
from pprint import pprint


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
    def test_syntax_analyzer(self, mocked_input):
        filenames = glob.glob(
            "Tests/SyntaxAnalyzer/**/testcase*.cf", recursive=True)
        count = 0
        for filename in filenames:
            with open(filename) as f:
                test_case = TestParser.parse(f.read())
                if not test_case:
                    continue

                inputs, outputs = test_case
            with self.subTest(filename=filename):
                mocked_input.side_effect = inputs
                self.assertRaises(SyntaxError, run_compiler, filename)
                count += 1
        print(f"Syntax Analyzer: Executed {count} test cases")


class TestSemanticAnalyzer(unittest.TestCase):
    @patch("builtins.input")
    def test_semantic_analyzer(self, mocked_input):
        filenames = glob.glob(
            "Tests/SemanticAnalyzer/**/testcase*.cf", recursive=True)
        count = 0
        for filename in filenames:
            with open(filename) as f:
                test_case = TestParser.parse(f.read())
                if not test_case:
                    continue

                inputs, outputs = test_case
            with self.subTest(filename=filename):
                mocked_input.side_effect = inputs
                self.assertRaises(SemanticError, run_compiler, filename)
                count += 1
        print(f"Semantic Analyzer: Executed {count} test cases")


class TestLexicalAnalyzer(unittest.TestCase):
    @patch("builtins.input")
    def test_lexical_analyzer(self, mocked_input):
        filenames = glob.glob(
            "Tests/LexicalAnalyzer/**/testcase*.cf", recursive=True)
        count = 0
        for filename in filenames:
            with open(filename) as f:
                test_case = TestParser.parse(f.read())
                if not test_case:
                    continue

                inputs, outputs = test_case
            with self.subTest(filename=filename):
                mocked_input.side_effect = inputs
                self.assertRaises(SyntaxError, run_compiler, filename)
                count += 1
        print(f"Lexical Analyzer: Executed {count} test cases")


class TestWorking(unittest.TestCase):
    @patch("builtins.input")
    def test_working(self, mocked_input):
        with open("Tests/Working/input_output.txt") as f:
            filenames, test_inputs, expected_outputs = InOut.parse(f.read())

        for test_input, expected_output, filename in zip(test_inputs, expected_outputs, filenames):
            with self.subTest(filename=filename):
                mocked_input.side_effect = test_input

                actual = run_compiler("Tests/Working/"+filename)

                self.assertEqual(expected_output, actual)
        print(f"Working: Executed {len(filenames)} test cases")


unittest.main()

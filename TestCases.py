from Lib.Token import Token
import glob
from typing import List
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
from Lib import OutputFormatter
import os


class CompilerTestCase(unittest.TestCase):
    def run_working_example(self, mocked_input, filenames):
        count = 0
        for filename in filenames:
            # get expected inputs and outputs from test case
            with open(filename) as f:
                test_case = TestParser.parse(f.read())
                if not test_case:
                    continue
                inputs, expected_output = test_case

            # Create subtest
            with self.subTest(filename=filename):
                # Mock inputs as side effect
                mocked_input.side_effect = inputs

                print("Running Test Case:",filename)

                # run compiler and expect error
                actual_output = self.run_compiler(filename, 
                                        display_tokens=False,
                                        display_tree=True,
                                        display_symbol_table=False)

                # Compare expected output with actual output
                self.assertEqual(actual_output, expected_output)

                print("Success!")
                print()

                count += 1
        return count

    def run_counter_example(self, mocked_input, filenames, errorType):
        count = 0
        for filename in filenames:
            # get expected inputs and outputs from test case
            with open(filename) as f:
                test_case = TestParser.parse(f.read())
                if not test_case:
                    continue
                inputs, outputs = test_case
            # Create subtest
            with self.subTest(filename=filename):
                # Mock inputs as side effect
                mocked_input.side_effect = inputs

                print("Running Test Case:",filename)
                # run compiler and expect error
                with self.assertRaises(errorType) as err:
                    self.run_compiler(filename)

                # Display error
                print(os.path.basename(filename)+":", err.exception)
                print("Success!")
                print()
                count += 1
        return count

    def run_compiler(self, file_name, display_tokens = False, display_tree = False, display_symbol_table = False):
        lexer = LexicalAnalyzer()
        parser = SyntaxAnalyzer()
        semanticAnalyzer = SemanticAnalyzer()
        evaluator = TreeEvaluator()

        tokens = lexer.run(file_name)
        tree = parser.run(tokens)
        symbol_table = semanticAnalyzer.run(tree)

        if display_tokens:
            self.display_tokens(tokens)
        
        if display_tree:
            self.display_tree(tree)

        if display_symbol_table:
            pass

        return evaluator.run(tree)

    def display_tokens(self, tokens: List['Token']):
        print("--"*20)
        print("Tokens:")
        for token in tokens:
            print(f"{token.type:20}{token.value}")
        print("--"*20)
        


    def display_tree(self, tree):
        OutputFormatter.print_tree(tree)

    def display_symbol_table(self, symbol_table):
        pass


class TestSyntaxAnalayzer(CompilerTestCase):
    @patch("builtins.input")
    def test_syntax_analyzer(self, mocked_input):
        # Get all test case files
        filenames = glob.glob(
            "Tests/SyntaxAnalyzer/**/testcase*.cf", recursive=True)

        count = self.run_counter_example(mocked_input, filenames, SyntaxError)

        # Display how many test cases ran
        print(f"Syntax Analyzer: Executed {count} test cases")


class TestSemanticAnalyzer(CompilerTestCase):
    @patch("builtins.input")
    def test_semantic_analyzer(self, mocked_input):
        filenames = glob.glob(
            "Tests/SemanticAnalyzer/**/testcase*.cf", recursive=True)

        count = self.run_counter_example(
            mocked_input, filenames, SemanticError)

        print(f"Semantic Analyzer: Executed {count} test cases")


class TestLexicalAnalyzer(CompilerTestCase):
    @patch("builtins.input")
    def test_lexical_analyzer(self, mocked_input):
        filenames = glob.glob(
            "Tests/LexicalAnalyzer/**/testcase*.cf", recursive=True)

        count = self.run_counter_example(mocked_input, filenames, Exception)

        print(f"Lexical Analyzer: Executed {count} test cases")


class TestWorking(CompilerTestCase):
    @patch("builtins.input")
    def test_working(self, mocked_input):
        filenames = glob.glob(
            "Tests/Working/**/testcase*.cf", recursive=True)

        count = self.run_working_example(mocked_input, filenames)

        print(f"Working: Executed {count} test cases")


unittest.main()

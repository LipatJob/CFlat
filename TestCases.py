import glob
import os
import unittest
from pprint import pprint
from typing import List
from unittest.case import skip
from unittest.mock import patch

import Lib.TestCaseParser2 as TestParser
from LexicalAnalyzer.LexicalAnalyzer import LexicalAnalyzer
from Lib import OutputFormatter
from Lib.ErrorHandler import *
from Lib.Token import Token
from SemanticAnalyzer.SemanticAnalyzer import SemanticAnalyzer
from SyntaxAnalyzer.SyntaxAnalyzer import SyntaxAnalyzer
from TreeEvaluator.TreeEvaluator import TreeEvaluator

DISPLAY_TOKENS = True
DISPLAY_TREE = False
DISPLAY_SYMBOL_TABLE = False
DISPLAY_EVALUATED_TABLE = False

class CompilerTestCase(unittest.TestCase):
    def run_working_example(self, mocked_input, filenames):
        count = 0
        for filename in filenames:
            # get expected inputs and outputs from test case
            with open(filename) as f:
                test_case = TestParser.parse(f.read())
                if not test_case:
                    continue
                inputs, expected_output, description = test_case

            # Create subtest
            with self.subTest(filename=filename):
                # Mock inputs as side effect
                mocked_input.side_effect = inputs

                print("-"*50)
                print(f">> Test: {count}")
                print(">> File:", filename)
                print(">> Description:")
                if len(description) > 0:
                    print(description)
                    print()
                print(">> Output:")
                # run compiler and expect error
                actual_output = self.run_compiler(filename,
                                                  display_tokens=DISPLAY_TOKENS,
                                                  display_tree=DISPLAY_TREE,
                                                  display_symbol_table=DISPLAY_SYMBOL_TABLE,
                                                  display_evaluated_table=DISPLAY_EVALUATED_TABLE)

                # Compare expected output with actual output
                self.assertEqual(actual_output, expected_output)
                print(">> Remarks: Success!")
                print("-"*50)
                print()
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
                inputs, outputs, description = test_case
            # Create subtest
            with self.subTest(filename=filename):
                # Mock inputs as side effect
                mocked_input.side_effect = inputs

                print("-"*50)
                print(f">> Test: {count}")
                print(">> File:", filename)
                print(">> Description:")
                if len(description) > 0:
                    print(description)
                    print()
                print(">> Output:")
                # run compiler and expect error
                with self.assertRaises(errorType) as err:
                    self.run_compiler(filename, display_tokens=DISPLAY_TOKENS,
                                                  display_tree=DISPLAY_TREE,
                                                  display_symbol_table=DISPLAY_SYMBOL_TABLE,
                                                  display_evaluated_table=DISPLAY_EVALUATED_TABLE)
                # Display error
                print(err.exception)
                print(">> Remarks: Success!")
                print("-"*50)
                print()
                print()

                count += 1
        return count

    def run_compiler(self, file_name, display_tokens=False, display_tree=False, display_symbol_table=False, display_evaluated_table=False):
        lexer = LexicalAnalyzer()
        parser = SyntaxAnalyzer()
        semanticAnalyzer = SemanticAnalyzer()
        evaluator = TreeEvaluator()

        tokens = lexer.run(file_name)
        if display_tokens:
            self.display_tokens(tokens)

        tree = parser.run(tokens)
        if display_tree:
            self.display_tree(tree)

        symbol_table = semanticAnalyzer.run(tree)
        if display_symbol_table:
            self.display_symbol_table(symbol_table)

        output = evaluator.run(tree)
        if display_evaluated_table:
            OutputFormatter.display_evaluated_symbol_table(evaluator.symbol_table)

        return output


    def display_tokens(self, tokens: List['Token']):
        OutputFormatter.display_tokens(tokens)

    def display_tree(self, tree):
        OutputFormatter.print_tree(tree)

    def display_symbol_table(self, symbol_table):
        OutputFormatter.display_semantic_symbol_table(symbol_table)

    def display_evaluated_symbol_table(self, symbol_table):
        OutputFormatter.display_evaluated_symbol_table(symbol_table)

class TestSyntaxAnalayzer(CompilerTestCase):
    #@skip("Test case disabled")
    @patch("builtins.input")
    def test_syntax_analyzer(self, mocked_input):
        # Get all test case files
        filenames = glob.glob(
            "Tests/SyntaxAnalyzer/**/testcase*.cf", recursive=True)

        count = self.run_counter_example(mocked_input, filenames, SyntaxError)

        # Display how many test cases ran
        print(f"Syntax Analyzer: Executed {count} test cases")


class TestSemanticAnalyzer(CompilerTestCase):
    #@skip("Test case disabled")
    @patch("builtins.input")
    def test_semantic_analyzer(self, mocked_input):
        filenames = glob.glob(
            "Tests/SemanticAnalyzer/**/testcase*.cf", recursive=True)

        count = self.run_counter_example(
            mocked_input, filenames, SemanticError)

        print(f"Semantic Analyzer: Executed {count} test cases")


class TestLexicalAnalyzer(CompilerTestCase):
    # @skip("Test case disabled")
    @patch("builtins.input")
    def test_lexical_analyzer(self, mocked_input):
        filenames = glob.glob(
            "Tests/LexicalAnalyzer/**/testcase*.cf", recursive=True)

        count = self.run_counter_example(mocked_input, filenames, TokenError)

        print(f"Lexical Analyzer: Executed {count} test cases")


class TestWorking(CompilerTestCase):
    #@skip("Test case disabled")
    @patch("builtins.input")
    def test_working(self, mocked_input):
        filenames = glob.glob(
            "Tests/Working/**/testcase*.cf", recursive=True)

        count = self.run_working_example(mocked_input, filenames)

        print(f"Working: Executed {count} test cases")


if __name__ == '__main__':
    unittest.main()

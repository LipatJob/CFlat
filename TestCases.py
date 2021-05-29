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

                # run compiler and expect error
                actual_output = self.run_compiler(filename)

                # Compare expected output with actual output
                self.assertEquals(actual_output, expected_output)

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

                # run compiler and expect error
                with self.assertRaises(errorType) as err:
                    self.run_compiler(filename)

                # Display error
                print(os.path.basename(filename)+":", err.exception)
                count += 1
        return count

    def run_compiler(self, file_name):
        lexer = LexicalAnalyzer()
        parser = SyntaxAnalyzer()
        semanticAnalyzer = SemanticAnalyzer()
        evaluator = TreeEvaluator()

        tokens = lexer.run(file_name)
        tree = parser.run(tokens)

        semanticAnalyzer.run(tree)
        return evaluator.run(tree)

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

        count = self.run_counter_example(mocked_input, filenames, SemanticError)

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
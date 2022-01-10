#!/usr/bin/env python3
import unittest
from apps.stax import StaxEngine

class TestStaxEngine(unittest.TestCase):
    def test_input_string(self):
        se = StaxEngine()
        test_value = 'alskdjfhaiuhflaweuhflsd'
        pipeline = [
            { 'processor': 'Input String', 'parameters': { 'string': test_value } },
            { 'processor': 'View' }
        ]
        for res in se.submit_pipeline(pipeline):
            self.assertEqual(res, test_value)

    def test_read_file_utf8_decode(self):
        se = StaxEngine()
        pipeline = [
            { 'processor': 'Input String', 'parameters': { 'string': 'apps/stax/tests/braille.txt' } },
            { 'processor': 'Read File' },
            { 'processor': 'Stream to String', 'parameters': { 'encoding': 'UTF=8' } },
            { 'processor': 'View' }
        ]

        answer = "⠗⠑⠛⠜⠙ ⠁ ⠊⠕⠋⠋⠔⠤⠝⠁⠊⠇ ⠁⠎ ⠹⠑ ⠙⠑⠁⠙⠑⠌ ⠏⠊⠑⠊⠑ ⠕⠋ ⠊⠗⠕⠝⠍⠕⠝⠛⠻⠹"
        for res in se.submit_pipeline(pipeline):
            self.assertEqual(res.strip(), answer)

    def test_read_file_xor_write_file(self):
        se = StaxEngine()
        pipeline = [
            { 'processor': 'Input String', 'parameters': { 'string': 'apps/stax/tests/xored.txt' } },
            { 'processor': 'Read File' },
            { 'processor': 'XOR', 'parameters': {'xor': '0xa5' } },
            { 'processor': 'Write File' },
            { 'processor': 'Read File' },
            { 'processor': 'Stream to String', 'parameters': {'encoding': 'UTF=8' } },
            { 'processor': 'View' }
        ]
        answer = "You passed the xor test."
        for res in se.submit_pipeline(pipeline):
            self.assertEqual(res, answer)

    def test_variable_storage_and_recall(self):
        se = StaxEngine()
        pipeline = [
            { 'processor': 'Input String', 'parameters': { 'string': 'testing' } },
            { 'processor': 'Store Variable', 'parameters': { 'name': 'z' } },
            { 'processor': 'Input Number', 'parameters': { 'number': 8.1 } },
            { 'processor': 'Store Variable', 'parameters': { 'name': 'y' } },
            { 'processor': 'Load All Variables' },
            { 'processor': 'Template Transform', 'parameters': { 'template': 'I am testing if {z} is testing and {y} is 8.1.'} },
            { 'processor': 'View' }
        ]
        answer = 'I am testing if testing is testing and 8.1 is 8.1.'
        for res in se.submit_pipeline(pipeline):
            self.assertEqual(res, answer)

    def test_shell_command(self):
        se = StaxEngine()
        pipeline = [
            { 'processor': 'Input String', 'parameters': { 'string': 'face me or debase me' } },
            { 'processor': 'Shell Command', 'parameters': { 'command': '/usr/bin/uuencode --base64 -'} },
            { 'processor': 'View' }
        ]
        answer = """begin-base64 664 -
dGVzdA==
====
"""
        for res in se.submit_pipeline(pipeline):
            self.assertEqual(res, answer)

if __name__ == '__main__':
    unittest.main()

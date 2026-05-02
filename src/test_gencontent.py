import unittest
from gencontent import extract_title

class TestGenContent(unittest.TestCase):
    def test_extract_title(self):

        self.assertEqual(extract_title("# Hello World"), "Hello World")
        with self.assertRaises(Exception):
            extract_title("## Hello World")
        
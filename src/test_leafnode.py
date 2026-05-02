import unittest

from htmlnode import LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    
    def test_leaf_to_html_h1(self):
        node1 = LeafNode("h1", "Heading 1")
        self.assertEqual(node1.to_html(), "<h1>Heading 1</h1>")
    
    def test_leaf_to_html_b(self):
        node = LeafNode("b", "bold text")
        self.assertEqual(node.to_html(), "<b>bold text</b>")

import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode(props={"href": "https://www.google.com"})
        node2 = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        node3 = HTMLNode(props=None)
        self.assertEqual(node1.props_to_html(), ' href="https://www.google.com"')
        self.assertEqual(node2.props_to_html(), ' href="https://www.google.com" target="_blank"')
        self.assertEqual(node3.props_to_html(), "")

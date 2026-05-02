import unittest 

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_empty_url(self):
        node = TextNode("This node has an empty url", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_new_texttype(self):
        node = TextNode("this node and a italic text type", TextType.ITALIC)
        self.assertEqual(node.text_type, TextType.ITALIC)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    if __name__ == "__main__":
        unittest.main()

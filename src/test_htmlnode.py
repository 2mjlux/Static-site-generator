import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        #node = TextNode("This is a text node", TextType.BOLD)
        #node2 = TextNode("This is a text node", TextType.BOLD)
        #self.assertEqual(node, node2)

    def test_not_props(self):
        #node = TextNode("This is a text node", TextType.BOLD)
        #node2 = TextNode("This is a text node", TextType.ITALIC)
        #self.assertNotEqual(node, node2)

    def test_not_props2(self):
        #node = TextNode("This is a text node", TextType.BOLD)
        #node2 = TextNode("This is a not text node", TextType.BOLD)
        #self.assertNotEqual(node, node2)

    def test_props2(self):
        #node = TextNode("This is a text node", TextType.BOLD, None)
        #node2 = TextNode("This is a text node", TextType.BOLD)
        #self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()


import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_normal(self):
        test_props = {"href": "https://www.google.com", "target": "_blank", }
        node = HTMLNode(None, None, None, test_props)
        self.assertEqual(
            node.props_to_html(),
            'href="https://www.google.com" target="_blank"'
        )

    def test_props_none(self):
        node = HTMLNode(None, None, None, None)
        self.assertEqual(node.props_to_html(), '')

    def test_props_empty(self):
        node = HTMLNode(None, None, None)
        self.assertEqual(node.props_to_html(), '')


if __name__ == "__main__":
    unittest.main()

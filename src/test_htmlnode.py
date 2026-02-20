import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://google.com"})
        self.assertEqual(node.to_html(), '<a href="https://google.com">Click me!</a>')

    class TestLeafNode(unittest.TestCase):
        def test_leaf_no_tag_returns_value(self):
            node = LeafNode(None, "just text")
            self.assertEqual(node.to_html(), "just text")

    def test_leaf_missing_value_raises(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_missing_tag_raises(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("span", "x")]).to_html()

    def test_parent_missing_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_parent_empty_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_parent_multiple_children(self):
        parent = ParentNode("p", [
            LeafNode("b", "Bold"),
            LeafNode(None, " Normal "),
            LeafNode("i", "Italic"),
        ])
        self.assertEqual(parent.to_html(), "<p><b>Bold</b> Normal <i>Italic</i></p>")

if __name__ == "__main__":
    unittest.main()

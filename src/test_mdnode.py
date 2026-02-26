import unittest
from mdnode import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle",
                        TextType.TEXT
                        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode('This is text with a ', TextType.TEXT),
                                     TextNode("bolded phrase", TextType.BOLD),
                                     TextNode(" in the middle", TextType.TEXT)
                                     ]
                         )

    def test_delim_error(self):
        node = TextNode("This has an **unclosed bold", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_non_TEXT(self):
        node = TextNode("hi", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("hi", TextType.BOLD)])

    def test_multiples(self):
        node = TextNode("a **b** c **d** e", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("a ", TextType.TEXT),
                                     TextNode("b", TextType.BOLD),
                                     TextNode(" c ", TextType.TEXT),
                                     TextNode("d", TextType.BOLD),
                                     TextNode(" e", TextType.TEXT)
                                     ]
                         )

    def test_no_delimiter(self):
        node = TextNode("just plain text", TextType.TEXT)
        # note that split_nodes_delimiter is told what delimiter/type pair it’s looking
        # for via its arguments, not by inspecting the node’s TextType
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("just plain text", TextType.TEXT)])

    def test_delimiter_at_start(self):
        node = TextNode("**bold** then", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("bold", TextType.BOLD),
            TextNode(" then", TextType.TEXT),
        ])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a text with a [test link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual([("test link", "https://i.imgur.com/zjjcJKZ.png")], matches)


if __name__ == "__main__":
    unittest.main()

import unittest
from mdnode import split_nodes_delimiter
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


if __name__ == "__main__":
    unittest.main()

import unittest
from mdnode import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link
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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another"
            " ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_image_start_text_end(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) is an image and another"
            " ![second image](https://i.imgur.com/3elNhQu.png) here",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is an image and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes(self):
        node1 = TextNode("Node with ![image 1](url1)", TextType.TEXT)
        node2 = TextNode("Node with ![image 2](url2)", TextType.TEXT)
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("Node with ", TextType.TEXT),
                TextNode("image 1", TextType.IMAGE, "url1"),
                TextNode("Node with ", TextType.TEXT),
                TextNode("image 2", TextType.IMAGE, "url2")
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [linktext1](https://i.imgur.com/zjjcJKZ.png) and "
            "another [linktext2](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("linktext1", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "linktext2", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_link_start_text_end(self):
        node = TextNode(
            "[linktext1](https://i.imgur.com/zjjcJKZ.png) is a link and another"
            " [linktext2](https://i.imgur.com/3elNhQu.png) here",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("linktext1", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is a link and another ", TextType.TEXT),
                TextNode(
                    "linktext2", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_multiple_nodes(self):
        node1 = TextNode("Node with [link 1](url1)", TextType.TEXT)
        node2 = TextNode("Node with [link 2](url2)", TextType.TEXT)
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                TextNode("Node with ", TextType.TEXT),
                TextNode("link 1", TextType.LINK, "url1"),
                TextNode("Node with ", TextType.TEXT),
                TextNode("link 2", TextType.LINK, "url2")
            ],
            new_nodes,
        )

    # 1. Put these nodes in a list: [node1, node2]
    # 2. Pass that list to split_nodes_link
    # 3. What do you expect the resulting list to look like?
    #    (Hint: It should have 4 TextNodes total)


if __name__ == "__main__":
    unittest.main()

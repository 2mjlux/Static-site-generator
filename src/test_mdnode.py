import unittest
from mdnode import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    BlockType,
    block_to_block_type,
    markdown_to_html_node
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
        # note that split_nodes_delimiter is told what delimiter/type pair it's looking
        # for via its arguments, not by inspecting the node's TextType
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

    def test_split_images_initial_BOLd(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another"
            " ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.BOLD,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
               TextNode(
                    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and"
                    " another ![second image](https://i.imgur.com/3elNhQu.png)",
                    TextType.BOLD,
                ),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode("This is text with no image nor a link.", TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is text with no image nor a link.", TextType.TEXT,)],
            new_nodes,
        )

    def test_split_images_no_text(self):
        node = TextNode("![img1](url1)![img2](url2)", TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "url1"),
                TextNode("img2", TextType.IMAGE, "url2"),
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

    def test_split_links_initial_BOLd(self):
        node = TextNode(
            "This is text with an [link 1](https://i.imgur.com/zjjcJKZ.png) and another"
            " [link 2](https://i.imgur.com/3elNhQu.png)",
            TextType.BOLD,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
               TextNode(
                    "This is text with an [link 1](https://i.imgur.com/zjjcJKZ.png) and"
                    " another [link 2](https://i.imgur.com/3elNhQu.png)",
                    TextType.BOLD,
                ),
            ],
            new_nodes,
        )

    def test_split_no_links(self):
        node = TextNode("This is text with no image nor a link.", TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is text with no image nor a link.", TextType.TEXT,)],
            new_nodes,
        )

    def test_split_links_no_text(self):
        node = TextNode("[link1](url1)[link2](url2)", TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "url1"),
                TextNode("link2", TextType.LINK, "url2"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_complete(self):
        text = ("This is **text** with an _italic_ word and a `code block` and an "
                "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
                "[link](https://boot.dev)")
        textnodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE,
                         "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            textnodes
        )

    def test_text_to_textnodes_orderchange(self):
        text = "One **bold** then one [link](https://boot.dev) then _italic_"
        textnodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("One ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" then one ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" then ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            textnodes
        )


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is"
                " the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_whitespace_empty_blocks(self):
        md = "  # Heading  \n\n\n\nSome text.  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["# Heading", "Some text."]
        )

    def test_block_to_block_type_h6(self):
        self.assertEqual(block_to_block_type("###### Title"), BlockType.HEADING)

    def test_block_to_block_type_h_invalid(self):
        # 7 hashes should not match
        self.assertEqual(block_to_block_type("####### Title"), BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        self.assertEqual(block_to_block_type("```code here```"), BlockType.CODE)

    def test_block_to_block_type_code_multiline(self):
        self.assertEqual(block_to_block_type("```\ncode here\n```"), BlockType.CODE)

    def test_block_to_block_type_code_no_closing(self):
        self.assertEqual(block_to_block_type("```no closing"), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote_multiline(self):
        self.assertEqual(block_to_block_type(">line1\n>line2"), BlockType.QUOTE)

    def test_block_to_block_type_quote_missing_prefix(self):
        self.assertEqual(block_to_block_type(">line1\nline2"), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered(self):
        self.assertEqual(block_to_block_type("- item1\n- item2"),
                         BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_missing_prefix(self):
        self.assertEqual(block_to_block_type("- item1\nitem2"), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered(self):
        self.assertEqual(block_to_block_type("1. item\n2. item\n3. item"),
                         BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_wrong_start(self):
        # Must start at 1
        self.assertEqual(block_to_block_type("0. item\n1. item"), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_not_incrementing(self):
        self.assertEqual(block_to_block_type("1. item\n3. item"), BlockType.PARAGRAPH)


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is"
            " another paragraph with <i>italic</i> text and <code>code</code> here</p>"
            "</div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with"
            " inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
## A heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>A heading</h2></div>")

    def test_blockquote(self):
        md = """
> This is a quote
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a quote</blockquote></div>")

    def test_blockquote_multiline(self):
        md = """
>line one
>line two
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>line one line two</blockquote></div>")

    def test_blockquote_inline_markdown(self):
        md = """
>This is **bold** and _italic_ text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is <b>bold</b> and <i>italic</i> text</blockquote>"
            "</div>",
        )

    def test_unordered_list(self):
        md = """
- first item
- second item
- third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>first item</li><li>second item</li><li>third item</li></ul>"
            "</div>",
        )

    def test_unordered_list_single_item(self):
        md = """
- only item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>only item</li></ul></div>")

    def test_unordered_list_inline_markdown(self):
        md = """
- **bold** item
- item with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><b>bold</b> item</li><li>item with <code>code</code></li>"
            "</ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. first item
2. second item
3. third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first item</li><li>second item</li><li>third item</li></ol>"
            "</div>",
        )

    def test_ordered_list_single_item(self):
        md = """
1. only item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>only item</li></ol></div>")

    def test_ordered_list_inline_markdown(self):
        md = """
1. **bold** item
2. item with _italic_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li><b>bold</b> item</li><li>item with <i>italic</i></li></ol>"
            "</div>",
        )


if __name__ == "__main__":
    unittest.main()

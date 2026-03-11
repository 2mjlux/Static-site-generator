from enum import Enum
from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import ParentNode
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    # delimiters = ["**", "_", "`"]
    # this project uses "_" as sole delimiter for italic text (ignore the "*" delimiter)
    # LINK and IMAGE handled later
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            if delimiter in node.text:
                parts = node.text.split(delimiter)
                if len(parts) % 2 == 0:
                    raise Exception("2nd delimiter missing")
                new_node = []
                for i, part in enumerate(parts):
                    if part == "":
                        continue
                    elif i % 2 == 0:
                        new_node.append(TextNode(part, TextType.TEXT))
                    else:
                        new_node.append(TextNode(part, text_type))
                new_nodes.extend(new_node)
            else:
                new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not node.text:
            continue
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        extracted_images = extract_markdown_images(node.text)
        if extracted_images == []:
            new_nodes.append(node)
            continue
        for alt_text, url in extracted_images:
            sections = original_text.split(f"![{alt_text}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not node.text:
            continue
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        extracted_links = extract_markdown_links(node.text)
        if extracted_links == []:
            new_nodes.append(node)
            continue
        for link_text, url in extracted_links:
            sections = original_text.split(f"[{link_text}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    old_nodes = [TextNode(text, TextType.TEXT)]
    delim_bold_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
    delim_italic_nodes = split_nodes_delimiter(delim_bold_nodes, "_", TextType.ITALIC)
    delim_code_nodes = split_nodes_delimiter(delim_italic_nodes, "`", TextType.CODE)
    split_image_nodes = split_nodes_image(delim_code_nodes)
    split_link_nodes = split_nodes_link(split_image_nodes)
    return split_link_nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    blocks = [block for block in blocks if block != ""]
    return blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in block.splitlines()):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in block.splitlines()):
        return BlockType.UNORDERED_LIST
    elif all(line.startswith(f"{i}. ") for i, line in enumerate(
             block.splitlines(), start=1)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def text_to_children(text):
    htmlnodes = []
    textnodes = text_to_textnodes(text)
    for textnode in textnodes:
        htmlnode = text_node_to_html_node(textnode)
        htmlnodes.append(htmlnode)
    return htmlnodes


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph_text = " ".join([line.strip() for line in lines])
    return ParentNode("p", text_to_children(paragraph_text))


def heading_to_html_node(block):
    level = len(block) - len(block.lstrip('#'))
    text = block.lstrip('#').strip()
    return ParentNode(f"h{level}", text_to_children(text))


def quote_to_html_node(block):
    clean_lines = []
    textlines = block.split("\n")
    for line in textlines:
        clean_line = line.lstrip(">").strip()
        clean_lines.append(clean_line)
    clean_quote = " ".join(clean_lines)
    return ParentNode("blockquote", text_to_children(clean_quote))


def code_to_html_node(block):
    clean_block = block[3:-3].strip() + "\n"
    text_node = TextNode(clean_block, TextType.TEXT)
    code_leaf = text_node_to_html_node(text_node)
    code_tag_node = ParentNode("code", [code_leaf])
    pre_tag_node = ParentNode("pre", [code_tag_node])
    return pre_tag_node


def ulist_to_html_node(block):
    html_items = []
    lines = block.split("\n")
    for line in lines:
        text = line[2:]
        # 1. Convert the text of THIS line into children nodes (for bold/italic/etc)
        children = text_to_children(text)
        # 2. Create a single <li> ParentNode for this specific item
        html_items.append(ParentNode("li", children))
    # 3. Return the final <ul> containing all our <li> items
    return ParentNode("ul", html_items)


def olist_to_html_node(block):
    html_items = []
    lines = block.split("\n")
    for line in lines:
        text = line.split(" ", 1)
        # 1. Convert the text of THIS line into children nodes (for bold/italic/etc)
        children = text_to_children(text[1])
        # 2. Create a single <li> ParentNode for this specific item
        html_items.append(ParentNode("li", children))
    # 3. Return the final <ul> containing all our <li> items
    return ParentNode("ol", html_items)


def block_to_html_node(block):
    # dispatcher function
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    else:
        raise Exception("No blocktype identified")


def markdown_to_html_node(markdown):
    children_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        htmlnode = block_to_html_node(block)
        children_nodes.append(htmlnode)
    return ParentNode("div", children_nodes)

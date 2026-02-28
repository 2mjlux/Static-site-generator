from textnode import TextType, TextNode
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    # delimiters = ["**", "*", "_", "`"]
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

from textnode import TextType, TextNode


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

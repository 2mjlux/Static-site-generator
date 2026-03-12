## Static Site Generator

A Markdown-to-HTML converter written in Python.

## Usage

```bash
# Run the program
python3 src/main.py

# Run tests
python3 -m unittest discover -s src
```

## The Big Picture

The code converts Markdown text to HTML through a three-stage pipeline:

```
Markdown string → [TextNode] → [HTMLNode] → HTML string
```

### `htmlnode.py` — Output Representation

`HTMLNode` (and its subclasses) represent actual HTML elements:

- `LeafNode`: Elements with no children (like `<b>text</b>` or `<img>`). Calls `to_html()` to produce the final string.
- `ParentNode`: Elements that contain other elements (like `<div><p>...</p></div>`). Recursively calls `to_html()` on all children.

### `textnode.py` — Intermediate Representation

`TextNode` represents parsed markdown text with semantic meaning before any rendering decision is made:

- `text`: The actual content (e.g., "click here")
- `text_type`: What kind of text it is (`TextType` enum: TEXT, BOLD, ITALIC, CODE, LINK, IMAGE)
- `url`: Optional URL for links/images

The `text_node_to_html_node()` function bridges the two representations:

| TextType | Becomes |
| --- | --- |
| `TEXT` | `LeafNode(None, text)` → raw text |
| `BOLD` | `LeafNode("b", text)` → `<b>text</b>` |
| `ITALIC` | `LeafNode("i", text)` → `<i>text</i>` |
| `CODE` | `LeafNode("code", text)` → `<code>text</code>` |
| `LINK` | `LeafNode("a", text, {"href": url})` → `<a href="...">text</a>` |
| `IMAGE` | `LeafNode("img", "", {"src": url, "alt": text})` → `<img ...>` |

### `mdnode.py` — Parsing Logic

This module handles all parsing, in two phases:

**Inline parsing** (within a line of text):

- `split_nodes_delimiter(nodes, delimiter, text_type)` — splits TEXT nodes on a delimiter (`**` for bold, `_` for italic, `` ` `` for code); non-TEXT nodes pass through unchanged.
- `split_nodes_image` / `split_nodes_link` — extract `![alt](url)` and `[text](url)` patterns.
- `text_to_textnodes(text)` — runs all splitters in sequence to produce a flat list of typed `TextNode`s from a raw markdown string.

**Block parsing** (document structure):

- `markdown_to_blocks(markdown)` — splits on `\n\n` into blocks, stripping whitespace and empty entries.
- `block_to_block_type(block)` — classifies a block as one of: PARAGRAPH, HEADING, CODE, QUOTE, UNORDERED_LIST, ORDERED_LIST.
- `markdown_to_html_node(markdown)` — top-level function that ties everything together, returning a `<div>` `ParentNode` containing the full document.

## Structure of Python files

Ex post, a better structure would have been as follows:

- **copystatic.py** — copying static assets (images, CSS) to the output directory
- **markdown_blocks.py** — parsing markdown into block-level nodes
- **inline_markdown.py** — parsing inline markdown (bold, italic, etc.)
- **htmlnode.py** — the HTML node classes and their .to_html() methods
- **gencontent.py** — orchestrating the generation of full HTML pages from markdown templates

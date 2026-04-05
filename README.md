## The Big Picture by the great Boots himself:

You build a program that takes **Markdown content** and **a template**, and produces a **fully deployable static website**.

### The Data Flow

```
Markdown files (content/)
        |
        v
  Parse Markdown
  into a tree of
  TextNode objects
        |
        v
  Convert to a tree of
  HTMLNode objects
        |
        v
  Render to an HTML string
        |
        v
  Inject into template.html
  (replacing {{ Title }} and {{ Content }})
        |
        v
  Write finished .html files
  to docs/
```

* * *

### The Layers

**1\. Text parsing (`textnode.py`, `inline_markdown.py`)**
Raw Markdown text (e.g. `**bold**`, `_italic_`, `` `code` ``) is split into `TextNode` objects, each carrying a type (bold, italic, link, image, etc.).

**2\. Block parsing (`markdown_blocks.py`)**
The full Markdown document is split into blocks (paragraphs, headings, lists, code blocks, quotes). Each block type is converted into the appropriate `HTMLNode` tree.

**3\. HTML node rendering (`htmlnode.py`)**
`HTMLNode` objects know how to render themselves to raw HTML strings via `to_html()`. Leaf nodes hold text; parent nodes hold children.

**4\. Page generation (`gencontent.py`)**
`generate_page` reads a Markdown file, converts it to HTML, injects it into the template, rewrites `href="/` and `src="/` to use the configured `basepath`, and writes the result to the output directory.

`generate_pages_recursive` walks the entire `content/` directory tree and calls `generate_page` for every file it finds.

**5\. Static file copying (`copystatic.py`)**
CSS, images, and other assets are copied from `static/` directly into `docs/`.

**6\. Entry point (`main.py`)**
Reads an optional CLI argument for the `basepath` (defaulting to `/`), wipes the `docs/` directory, copies static assets, then triggers recursive page generation.

**7\. Build scripts**

- `main.sh` runs the generator locally with `basepath = /` for development.
- `build.sh` runs it with `basepath = /REPO_NAME/` for GitHub Pages deployment.

* * *

### Why the basepath matters

GitHub Pages serves your site from `https://USERNAME.github.io/REPO_NAME/`, not from `/`. Without rewriting `href="/` and `src="/` to include the repo name, all your links and images would point to the wrong place on the live site.

* * *

That is the full system: a pipeline from raw Markdown all the way to a live, publicly accessible website. Well done building it from scratch.

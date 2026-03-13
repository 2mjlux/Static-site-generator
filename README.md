## The Big Picture

A static site generator is a pipeline:  read -> transform -> write.
In concrete terms this can be implemented as follows:

**Markdown string -> `TextNode` -> `HTMLNode` -> HTML string**.

The 3 stages are:

### 1. INPUT:
The Mardown files are read.  Static assets like images and CSS are copied separately to an output directory.

### 2. PROCESSING:
The processing is subdivided in parsing and rendering.


The **parsing** is subdivided in:


- parsing of _blocks_, for blocktypes like heading, quote or list, and
- parsing of _inline markdown_, which is basically word formatting like bold and italic, but also inserting like images and links.


**Rendering** is the stage where a `TextNode` is converted into a `HTMLNode`, typically a `LeafNode` for elements with no children and a `ParentNode` for nested structures that have children.

### 3. OUTPUT:
A generate_content function is used to generate the full HTML page, i.e. the `HTMLNode`(s) are converted into proper HTML readable by a web-browser.

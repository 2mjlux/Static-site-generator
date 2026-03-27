import os
from mdnode import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            h1_header = line[2:].strip()
            return h1_header
    raise Exception("No h1 header identified")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        content_md = f.read()
    with open(template_path, "r") as t:
        template = t.read()
    content_html_node = markdown_to_html_node(content_md)
    content_html = content_html_node.to_html()
    title = extract_title(content_md)
    template = template.replace("{{ Title }}", title).replace("{{ Content }}",
                                                              content_html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as d:
        d.write(template)

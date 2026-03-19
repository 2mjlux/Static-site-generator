import os
import shutil
from gencontent import generate_page


def is_markdown_file(filepath):
    _, ext = os.path.splitext(filepath)
    return ext.lower() in {'.md', '.markdown', '.mdown', '.mkd'}


def generate_pages_recursive(from_path, template_path, dest_path):
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.mkdir(dest_path)
    pages_to_generate = os.listdir(from_path)
    for page in pages_to_generate:
        filepath = os.path.join(from_path, page)
        if os.path.isfile(filepath) and is_markdown_file(filepath):
            md_file = str(page)
            root, _ = os.path.splitext(md_file)
            html_file = root + ".html"
            file_destination = os.path.join(dest_path, html_file)
            generate_page(filepath, template_path, file_destination)
        elif os.path.isdir(filepath):
            dir_destination = os.path.join(dest_path, page)
            generate_pages_recursive(filepath, template_path, dir_destination)
        else:
            continue

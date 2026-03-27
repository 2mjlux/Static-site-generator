import os
import shutil
from gencontent import generate_page


def is_markdown_file(filepath):
    _, ext = os.path.splitext(filepath)
    return ext.lower() in {'.md', '.markdown', '.mdown', '.mkd'}


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if os.path.exists(dest_dir_path):
        shutil.rmtree(dest_dir_path)
    os.mkdir(dest_dir_path)
    pages_to_generate = os.listdir(dir_path_content)
    for page in pages_to_generate:
        filepath = os.path.join(dir_path_content, page)
        if os.path.isfile(filepath) and is_markdown_file(filepath):
            md_file = str(page)
            root, _ = os.path.splitext(md_file)
            html_file = root + ".html"
            file_destination = os.path.join(dest_dir_path, html_file)
            generate_page(filepath, template_path, file_destination, basepath)
        elif os.path.isdir(filepath):
            dir_destination = os.path.join(dest_dir_path, page)
            generate_pages_recursive(filepath, template_path, dir_destination, basepath)
        else:
            continue

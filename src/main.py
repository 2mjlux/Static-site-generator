from copystatic import copystatic
from genpagesrecur import generate_pages_recursive
import sys


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    generate_pages_recursive("content/", "template.html", "docs/", basepath)
    copystatic("./static", "./docs")


main()

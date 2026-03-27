from copystatic import copystatic
from genpagesrecur import generate_pages_recursive
import sys


basepath = "/"
if len(sys.argv) > 1:
    basepath = sys.argv[1]


def main():
    generate_pages_recursive("content/", "template.html", "public/", basepath)
    copystatic("./static", "./public")


main()

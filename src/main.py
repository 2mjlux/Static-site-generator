from copystatic import copystatic
from genpagesrecur import generate_pages_recursive


def main():
    generate_pages_recursive("content/", "template.html", "public/")
    copystatic("./static", "./public")


main()

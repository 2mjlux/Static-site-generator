from copystatic import copystatic
from gencontent import generate_page


def main():

    copystatic("./static", "./public")
    generate_page("content/index.md", "template.html", "public/index.html")


main()

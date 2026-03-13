import unittest
from gencontent import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_h1_single_whitespaces(self):
        md = "#  h1 title "
        title = extract_title(md)
        self.assertEqual("h1 title", title)

    def test_h1_multiline_middle(self):
        md = """
bla
bla
# h1 title
bla
"""
        title = extract_title(md)
        self.assertEqual("h1 title", title)

    def test_no_h1_raises(self):
        md = "## Not an h1\nJust some text"
        with self.assertRaises(Exception):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()

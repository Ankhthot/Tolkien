import unittest
from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_with_whitespace(self):
        self.assertEqual(extract_title("#   Tolkien Fan Club  "), "Tolkien Fan Club")

    def test_no_h1_raises(self):
        with self.assertRaises(ValueError):
            extract_title("## No h1 here")

    def test_h1_among_other_lines(self):
        md = "Some text\n# The Title\nMore text"
        self.assertEqual(extract_title(md), "The Title")


if __name__ == "__main__":
    unittest.main()
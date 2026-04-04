import unittest
from block_markdown import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_newlines(self):
        md = """Block one



Block two


Block three"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block one", "Block two", "Block three"])

    def test_markdown_to_blocks_single_block(self):
        md = "Just one block with no separators"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one block with no separators"])

if __name__ == "__main__":
    unittest.main()
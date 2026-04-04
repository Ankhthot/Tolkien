from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_children
from textnode import TextType, TextNode


class BlockType:
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]


def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    is_ordered = True
    for i, line in enumerate(lines):
        if not line.startswith(f"{i + 1}. "):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            text = " ".join(block.split("\n"))
            children.append(ParentNode("p", text_to_children(text)))
        elif block_type == BlockType.HEADING:
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break
            text = block[level + 1:]
            children.append(ParentNode(f"h{level}", text_to_children(text)))
        elif block_type == BlockType.CODE:
            text = block[3:-3].strip("\n") + "\n"
            code_node = LeafNode("code", text)
            children.append(ParentNode("pre", [code_node]))
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            text = " ".join(line.lstrip(">").strip() for line in lines)
            children.append(ParentNode("blockquote", text_to_children(text)))
        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            items = [ParentNode("li", text_to_children(line[2:])) for line in lines]
            children.append(ParentNode("ul", items))
        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            items = [ParentNode("li", text_to_children(line.split(". ", 1)[1])) for line in lines]
            children.append(ParentNode("ol", items))
    return ParentNode("div", children)
from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: no closing delimiter '{delimiter}'")
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        remaining = node.text
        for alt, url in images:
            sections = remaining.split(f"![{alt}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining = sections[1]
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        remaining = node.text
        for anchor, url in links:
            sections = remaining.split(f"[{anchor}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            remaining = sections[1]
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

from htmlnode import LeafNode

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        if text_node.text_type == TextType.TEXT:
            children.append(LeafNode(None, text_node.text))
        elif text_node.text_type == TextType.BOLD:
            children.append(LeafNode("b", text_node.text))
        elif text_node.text_type == TextType.ITALIC:
            children.append(LeafNode("i", text_node.text))
        elif text_node.text_type == TextType.CODE:
            children.append(LeafNode("code", text_node.text))
        elif text_node.text_type == TextType.LINK:
            children.append(LeafNode("a", text_node.text, {"href": text_node.url}))
        elif text_node.text_type == TextType.IMAGE:
            children.append(LeafNode("img", "", {"src": text_node.url, "alt": text_node.text}))
    return children
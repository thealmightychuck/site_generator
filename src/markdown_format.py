from textnode import TextNode, TextType
import re
from enum import Enum


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    result = ()
    result = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return result

def extract_markdown_links(text):
    result = ()
    result = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return result

def split_nodes_image(old_nodes):
        section = []
        result = []
        for node in old_nodes:
            remaining_text = node.text
            extracted_images = extract_markdown_images(node.text)
            if len(extracted_images) == 0:
                result.append(node)
                continue
            for alt_text, url in extracted_images:
                section = remaining_text.split(f"![{alt_text}]({url})", 1)
                if section[0] != "":
                    result.append(TextNode(section[0], TextType.TEXT))
                result.append(TextNode(alt_text, TextType.IMAGE, url))
                remaining_text = section[1]
            if remaining_text != "":
                result.append(TextNode(remaining_text, TextType.TEXT))
        return result

def split_nodes_link(old_nodes):
        section = []
        result = []
        for node in old_nodes:
            remaining_text = node.text
            extracted_images = extract_markdown_links(node.text)
            if len(extracted_images) == 0:
                result.append(node)
                continue
            for text, url in extracted_images:
                section = remaining_text.split(f"[{text}]({url})", 1)
                if section[0] != "":
                    result.append(TextNode(section[0], TextType.TEXT))
                result.append(TextNode(text, TextType.LINK, url))
                remaining_text = section[1]
            if remaining_text != "":
                result.append(TextNode(remaining_text, TextType.TEXT))
        return result

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
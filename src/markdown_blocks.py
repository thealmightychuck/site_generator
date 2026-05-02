from enum import Enum
from markdown_format import text_to_textnodes
from textnode import TextType, text_node_to_html_node, TextNode
from htmlnode import ParentNode

def markdown_to_blocks(markdown):
    result = []
    md_list = markdown.split("\n\n")
    for item in md_list:
        item = item.strip()
        if item != "":
            result.append(item)
    return result

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown_text):
    lines = markdown_text.split("\n")
    if markdown_text.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) >= 3 and markdown_text.startswith("```\n") and markdown_text.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("-") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
           return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    node_list = []
    result = markdown_to_blocks(markdown=markdown)
    for ans in result:
        n = 0
        block_type = block_to_block_type(ans)
        if block_type == BlockType.HEADING:
            for char in ans:
                if char != '#':
                    break
                n += 1
            new_ans = ans[n+1:]
            tag = f"h{n}"
            children = text_to_children(new_ans)
            node = ParentNode(tag, children)
            node_list.append(node)

        if block_type == BlockType.PARAGRAPH:
            new_ans = ans.replace("\n", " ")
            children = text_to_children(new_ans)
            node = ParentNode("p", children)
            node_list.append(node)

        if block_type == BlockType.QUOTE:
            lines = ans.split("\n")
            cleaned = [line.lstrip(">").strip() for line in lines]
            new_ans = " ".join(cleaned)
            children = text_to_children(new_ans)
            node = ParentNode("blockquote", children)
            node_list.append(node)
        
        if block_type == BlockType.UNORDERED_LIST:
            lines = ans.split("\n")
            li_nodes = []
            for line in lines:
                line = line[2:]
                children = text_to_children(line)
                node = ParentNode("li", children)
                li_nodes.append(node)
            uo_list = ParentNode("ul", li_nodes)
            node_list.append(uo_list)
        
        if block_type == BlockType.ORDERED_LIST:
            lines = ans.split("\n")
            li_nodes = []
            for line in lines:
                line = line[3:]
                children = text_to_children(line)
                node = ParentNode("li", children)
                li_nodes.append(node)
            ol_list = ParentNode("ol", li_nodes)
            node_list.append(ol_list)
        
        if block_type == BlockType.CODE:
            code_string = ans[3:-3]
            code_string = code_string.lstrip("\n")
            code_obj = TextNode(text=code_string, text_type=TextType.TEXT)
            node = text_node_to_html_node(code_obj)
            code_parent = ParentNode("code", [node])
            pre_parent = ParentNode("pre", [code_parent])
            node_list.append(pre_parent)

    return ParentNode("div", node_list)

def text_to_children(text):
    results = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        child = text_node_to_html_node(node)
        results.append(child)
    return results


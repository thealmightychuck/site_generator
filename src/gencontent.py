from markdown_blocks import markdown_to_html_node
import os
from pathlib import Path
def extract_title(markdown):
    split_markdown = markdown.split('\n')
    for line in split_markdown:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("no h1 found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(from_path, "r") as file:
        content = file.read()
    
    with open(template_path, "r") as file:
        template = file.read()
    
    markdown_content = markdown_to_html_node(content)
    html_string = markdown_content.to_html()

    title = extract_title(content)

    final_html = template.replace("{{ Content }}",html_string).replace("{{ Title }}", title)
    final_html = final_html.replace('href="/', 'href="' + basepath)
    final_html = final_html.replace('src="/', 'src="' + basepath)
    
    with open(dest_path, 'w') as file:
        file.write(final_html)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        if Path(entry).suffix == ".md":
            source_path = Path(os.path.join(dir_path_content, entry))
            new_path = Path(os.path.join(dest_dir_path, entry))
            new_path = new_path.with_suffix(".html")
            generate_page(source_path, template_path, new_path, basepath)
        if Path(os.path.join(dir_path_content, entry)).is_dir():
            new_dir_path = os.path.join(dir_path_content, entry)
            new_dest_dir_path = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(new_dir_path, template_path, new_dest_dir_path, basepath)


import os
import shutil
from copystatic import copy_files_recursive
from gencontent import extract_title, generate_page, generate_pages_recursive
import sys

dir_path_static = "./static"
dir_path_public = "./docs"
template = "./content/"
default_basepath = "/"

def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print("Deleting public directory")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory")
    copy_files_recursive(dir_path_static, dir_path_public)
    generate_pages_recursive("./content/", "./template.html", "./docs/", basepath)

main()

from pathlib import Path
from export.converter import update_all_files
import argparse
import json

"""
This script processes ChatGPT conversation.json file to markdown files with a YAML front matter. 

The script is designed to be run as a command-line interface (CLI), allowing the user to
specify the input JSON file and output directory.

Run at the root folder:
    source venv/bin/activate    
    python -m export.main /path/to/conversations.json /path/to/output_directory 

"""


def main():
    parser = argparse.ArgumentParser(
        description="Process conversation config from a JSON file and create Obsidian-friendly markdown files.")
    parser.add_argument("input_file", type=Path, help="Path to the input conversations JSON file.")
    parser.add_argument("output_dir", type=Path, help="Directory to save the output files.")
    args = parser.parse_args()
    if not args.input_file.exists():
        print(f"Error: The input file '{args.input_file}' does not exist.")
        return
    with args.input_file.open("r", encoding="utf-8") as file:
        conversations_data = json.load(file)
    update_all_files(conversations_data, args.output_dir)


if __name__ == "__main__":
    main()

import json
import os
import re
import yaml
from pathlib import Path


def extract_json(text: str) -> dict:
    # Extract JSON code block using regex
    match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
    if match:
        json_str = match.group(1)
        data = json.loads(json_str)
        return data
    else:
        print("No valid JSON found.")
        return {}


def parse_file(file: Path) -> dict:
    with file.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    metadata = {}
    content = ''

    if lines and lines[0].strip() == '---':
        try:
            end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == '---')
            front_matter = ''.join(lines[1:end])
            metadata = yaml.safe_load(front_matter) or {}
            content = ''.join(lines[end + 1:])
        except StopIteration:
            # No closing '---' found
            content = ''.join(lines)
    else:
        content = ''.join(lines)

    return {'metadata': metadata, 'content': content}


def find_files_by_id(directory: Path, target_id: str) -> Path:
    """
    Finds files in a given directory (not in the subdirectories) whose names contain a specific ID
    in the format "title[id]".

    Args:
        directory (str): The path to the directory to search.
        target_id (str): The specific ID to look for in the filenames.
    """
    # Regex to match filenames like "title[id]"
    # It captures the ID inside the square brackets.
    # The 'r' before the string indicates a raw string, which is good for regex.
    # r"\[(\d+)\]" looks for literal '[' then captures one or more digits (\d+)
    # then looks for literal ']'.
    # The captured digits are the ID.
    filename_pattern = re.compile(r"\[([^\]]+)\]")

    with os.scandir(directory) as entries:
        for entry in entries:
            entry: os.DirEntry
            if entry.is_file():
                match = filename_pattern.search(entry.name)
                if match:
                    file_id = match.group(1)
                    if file_id == target_id:
                        return Path(os.path.join(directory, entry.name))


def find_files_by_id_all_subs(directory: Path, target_id: str) -> Path:
    """
    Finds files in a given directory (including all its subdirectories) whose names contain a specific ID
    in the format "title[id]".

    Args:
        directory (str): The path to the directory to search.
        target_id (str): The specific ID to look for in the filenames.
    """
    filename_pattern = re.compile(r"\[([^\]]+)\]")

    # Walk through all files and directories in the given path
    for root, _, files in os.walk(directory):
        for filename in files:
            # Search for the pattern in the current filename
            match = filename_pattern.search(filename)
            if match:
                # If a match is found, extract the ID
                file_id = match.group(1) # group(1) refers to the first captured group (the ID)
                if file_id == target_id:
                    # Construct the full path to the found file
                    full_path = os.path.join(root, filename)
                    return Path(full_path)

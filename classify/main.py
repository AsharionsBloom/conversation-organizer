import os
import json
from pathlib import Path

from classify.llm_classifier import classify_all_files
from classify.llm_models import Gemini


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Process the existing markdown conversations using Gemini.")
    parser.add_argument("folder_path", type=Path, help="Folder containing markdown files to classify.")
    args = parser.parse_args()

    # Get the directory where the script is located
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    root_dir = os.path.dirname(script_dir)

    with open(os.path.join(root_dir, 'config', 'user_tags.json'), "r") as f:
        tag_dict = json.load(f)

    def gemini():
        with open(os.path.join(root_dir, 'config', 'gemini.json'), "r") as file:
            config = json.load(file)
        api_key = config["api_key"]
        api_url = config["api_url"]
        return Gemini(api_key, api_url)

    classify_all_files(args.folder_path, gemini(), tag_dict)


if __name__ == "__main__":
    main()

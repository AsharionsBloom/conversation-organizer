from pathlib import Path
import yaml
from llm_models import LLM
from common.utils import parse_file, extract_json


def llm_classifier(file: Path, llm: LLM, tags_with_descriptions: dict) -> None:
    file_content = parse_file(file)
    metadata = file_content["metadata"]
    content = file_content["content"]
    # Files marked with delete are not processed by the LLM
    if not metadata["delete"]:
        prompt = (
            "Read this text: "
            f"\n===\n"
            f"\n{content}\n"
            f"\n===\n"
            "Return ONLY in the format of a json with two fields, like this: "
            '{"title":  <you think of a good title for the text>,'
            '"tags":'
            f"<choose (be very conservative) the most fitting tags from here: \n{tags_with_descriptions.keys()}>"
        )
        # Tries a finite amount of times at most with the prompt
        number_of_trials = 10
        for _ in range(number_of_trials):
            response = llm.response_from(prompt)
            print(f"response: {response}")
            if response is not None:
                data = extract_json(response)
                print(data)
                if "title" in data and "tags" in data:
                    metadata.update(data)
                    with file.open("w", encoding="utf-8") as file:
                        file.write("---\n")
                        yaml.dump(metadata, file, sort_keys=False)
                        file.write("---\n")
                        file.write(f"# {data['title']}\n\n")
                        file.write(content)
                    return None
        print(f"No valid return from the LLM after {number_of_trials} calls.")


def process_all_files(folder_path: Path, llm: LLM, tags_with_descriptions: dict) -> None:
    for file in folder_path.glob("*.md"):
        llm_classifier(file, llm, tags_with_descriptions)

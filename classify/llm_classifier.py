from pathlib import Path
import yaml
from classify.llm_models import LLM
from common.utils import parse_file, extract_json, update_yaml_list


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
            "Return ONLY in the format of a json, like this: "
            '{"tags":'
            "<choose (very conservatively) up to 3 tags that characterize the text best, "
            "from this list only: "
            f"\n{tags_with_descriptions.keys()}>"
        )
        # Tries a finite amount of times at most with the prompt
        number_of_trials = 2
        for _ in range(number_of_trials):
            response = llm.response_from(prompt)
            if response is not None:
                data = extract_json(response)
                if data.get("tags", []):
                    updated_metadata = update_yaml_list(metadata, "tags", data["tags"])
                    with file.open("w", encoding="utf-8") as file:
                        file.write("---\n")
                        yaml.dump(updated_metadata, file, sort_keys=False)
                        file.write("---\n")
                        file.write(content)
                    print(f"{data} for {file.name} ")
                    return None
        print(f"No valid return from the LLM after {number_of_trials} calls.")


def classify_all_files(folder_path: Path, llm: LLM, tags_with_descriptions: dict) -> None:
    for file in folder_path.glob("*.md"):
        llm_classifier(file, llm, tags_with_descriptions)

import json
import os

from utils import convert_latex_to_markdown, sanitize_title
from datetime import datetime
from pathlib import Path
import yaml


def extract_message_parts(message):
    """
    Extracts the main text content from a message.

    Special handling is included for system tool messages:
    - canmore.update_textdoc: returns the 'replacement' field (code update)
    - canmore.create_textdoc: returns the 'content' field (full new doc)

    If decoding fails or the message is normal, falls back to raw text.
    """
    content = message.get("content")
    if not content or content.get("content_type") != "text":
        return []

    parts = content.get("parts", [])
    if not parts:
        return []

    text = parts[0]
    recipient = message.get("recipient")

    if recipient == "canmore.create_textdoc":
        try:
            doc = json.loads(text)
            lang = doc.get("type", "").split("/")[-1]
            content = doc.get('content', '')
            return [f"```{lang}\n{content}\n```"]
        except (json.JSONDecodeError, TypeError):
            pass
    if recipient == "canmore.update_textdoc":
        try:
            parsed = json.loads(text)
            updates = parsed.get("updates", [])
            if updates and "replacement" in updates[0]:
                content = updates[0]["replacement"]
                return [f"```\n{content}\n```"]
        except json.JSONDecodeError:
            pass
    return [text]


def get_author_name(message):
    author = message.get("author", {}).get("role", "")
    if author == "assistant":
        meta = message.get("metadata", {})
        model_slug = meta.get("model_slug")
        return model_slug
    elif author == "system":
        return "Custom user info"
    return author


def get_conversation_messages(conversation):
    messages = []
    current_node = conversation.get("current_node")
    mapping = conversation.get("mapping", {})
    while current_node:
        node = mapping.get(current_node, {})
        message = node.get("message") if node else None
        if message:
            parts = extract_message_parts(message)
            author = get_author_name(message)
            if author != "tool":
                # Exclude system messages unless explicitly marked
                if parts and len(parts[0]) > 0:
                    if author != "system" or message.get("metadata", {}).get("is_user_system_message"):
                        messages.append({"author": author, "text": parts[0]})
        current_node = node.get("parent") if node else None
    return messages[::-1]


def create_file_name_id(conversation_id):
    return f"{conversation_id}.md"


def create_file_name_tile_and_id(title, conversation_id):
    sanitized_title = sanitize_title(title)
    short_id = conversation_id[:4]
    return f"{sanitized_title} [{short_id}].md"


def conversation_info(conversation):
    messages = get_conversation_messages(conversation)
    conversation_id = conversation.get("id")
    create_time = datetime.fromtimestamp(conversation.get("create_time")).isoformat(timespec="seconds")
    update_time = datetime.fromtimestamp(conversation.get("update_time")).isoformat(timespec="seconds")
    conversation_title = conversation.get("title")
    is_archived = conversation.get("is_archived")

    # Each message is a dictionary: {'author': 'user' or 'ChatGPT', 'text': 'text'}
    total_length = sum(len(s['text']) for s in messages)

    data = {
        "id": conversation_id,
        "create_time": create_time,
        "update_time": update_time,
        "original_title": conversation_title,
        "turns": len(messages),
        "characters": total_length,
        "archive": is_archived
    }
    return data


def get_file_metadata(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    if lines[0].strip() == '---':
        # Find where the front matter ends
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == '---')
        front_matter = ''.join(lines[1:end])
        metadata = yaml.safe_load(front_matter)
    else:
        print("No YAML frontmatter found")
        metadata = {}
    return metadata


def write_to_file(metadata: dict, messages: list, file_path: Path):
    with file_path.open("w", encoding="utf-8") as file:
        file.write("---\n")
        yaml.dump(metadata, file, sort_keys=False)
        file.write("---\n")
        for message in messages:
            file.write(f"**{message['author']}**\n\n")
            file.write(f"{message['text']}\n\n")
        # print(f"File created: {file_path}")


def update_file(conversation, output_dir: Path):
    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    data = conversation_info(conversation)
    file_name = create_file_name_id(data["id"])
    file_path: Path = output_dir / file_name
    messages = get_conversation_messages(conversation)
    if os.path.exists(file_path):
        metadata = get_file_metadata(file_path)
        new_update_time = datetime.fromisoformat(data['update_time'])
        if type(metadata['update_time']) == str:
            old_update_time = datetime.fromisoformat(metadata['update_time'])
        else:
            old_update_time = metadata['update_time']
        if new_update_time > old_update_time:
            print("update")
            # If a file in marked delete but on the web-end, it got modified,
            # then we add a delete_time that was the old update_time
            if "delete" in metadata:
                if metadata["delete"]:
                    metadata["delete_time"] = metadata["update_time"]
            metadata.update(data)
            write_to_file(metadata, messages, file_path)
    else:
        write_to_file(data, messages, file_path)


def update_all_files(conversations_data, output_dir: Path):
    for conversation in conversations_data:
        update_file(conversation, output_dir)

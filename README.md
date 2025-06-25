# ChatGPT Conversation Organizer

This tool converts your official ChatGPT `conversations.json` export into individual Markdown (`.md`) files suitable for use with [Obsidian](https://obsidian.md/).
Each file includes YAML front matter with metadata and conversation statistics.

### ✨ Features

**Conversion highlights:**

* Splits each conversation into a standalone Markdown file

* Supports updating existing notes when a new `conversations.json` export is downloaded and converted
  *(Tip: use Git to track and review changes over time)*


* Supports rendering of:
  * Search tool results with URLs
  * Canvas code
  * LaTeX blocks for display in Obsidian



> ⚠️ Currently, images and audio content in conversations are **not supported** by the converter.




**Classification module (optional):**

* Uses an LLM (e.g., Google Gemini or Ollama-backed models) to auto-assign user-defined tags

Note: Configuration files are not tracked in version control.

   * Store your model API info and keys in `config/gemini.json` or `config/ollama.json`.

   * User tags with descriptions go in `config/user_tags.json`.

---

### 🔧 Installation

1. Clone or download this repository.
2. From the project root, run:

   ```bash
   pip install -e .
   ```
3. Run the converter using:
   ```bash
   python -m export.main /path/to/conversation.json /path/to/folder/
   ```


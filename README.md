# ChatGPT Conversation Organizer

This tool converts your official ChatGPT `conversations.json` export into individual Markdown (`.md`) files suitable for use with [Obsidian](https://obsidian.md/),
where plugins like Dataview and Smart Connections offer better organization and search than the native ChatGPT app or web interface.

---

### ✨ Features

**Conversion highlights:**

* Converts each conversation into a standalone Markdown file, with YAML front matter containing metadata and conversation statistics
* Re-converting a newer `conversations.json` export updates existing notes in-place—no duplication
* Automatically includes a link to the original ChatGPT conversation
* Renders:

  * Search tool results with URLs
  * Canvas code
  * LaTeX blocks compatible with Obsidian display

*Tip: Use Git to track and review local changes over time.*

> ⚠️ Currently, images, videos and audio content in conversations are **not supported**.

---

**Classification module (optional):**

* Uses an LLM (e.g., Google Gemini or Ollama-backed models) to auto-assign tags from a user-defined tag list.

**Note:** Configuration files are not tracked in version control.

* Store model API info and keys in `config/gemini.json` or `config/ollama.json`
* Store tag definitions (with descriptions) in `config/user_tags.json`

---

### 🔧 Installation

1. Clone or download this repository.

2. From the project root, install the package:

   ```bash
   pip install -e .
   ```

3. Run the converter with:

   ```bash
   python -m export.main /path/to/conversations.json /path/to/output_folder/
   ```

---

**Contributions and collaborators are welcome!**

import re
import string
import unicodedata


def convert_latex_delimiters_excluding_backticks(text):
    """
    Converts LaTeX inline and display math delimiters, but excludes
    any matches that are found within backticks (`...`).
    """

    # Regex patterns for math delimiters
    inline_math_pattern = r'\\\(\s*(.*?)\s*\\\)'
    display_math_pattern = r'\\\[\s*(.*?)\s*\\\]'

    # Combined pattern:
    # 1. `([^`]*?)`   : Matches any content within backticks (captures the content).
    #                    The `[^`]*?` ensures it's non-greedy and doesn't cross backticks.
    # 2. |             : OR
    # 3. (inline_math_pattern) : Matches the inline math pattern (captures the whole pattern).
    # 4. |             : OR
    # 5. (display_math_pattern): Matches the display math pattern (captures the whole pattern).
    # Using re.DOTALL allows `.` to match newlines, important for multiline display math.
    combined_pattern = rf"`([^`]*?)`|({inline_math_pattern})|({display_math_pattern})"

    def replacer(match):
        # Group 1: Content inside backticks
        if match.group(1) is not None:
            return f"`{match.group(1)}`"  # Return the whole backtick block unchanged

        # Group 2: Full inline math match (e.g., '\(x^2\)')
        # Group 3: Content inside inline math (e.g., 'x^2')
        elif match.group(2) is not None:
            return f"${match.group(3)}$"  # Convert inline math

        # Group 4: Full display math match (e.g., '\[E=mc^2\]')
        # Group 5: Content inside display math (e.g., 'E=mc^2')
        elif match.group(4) is not None:
            return f"$${match.group(5)}$$"  # Convert display math

        # This case shouldn't be reached if the patterns are mutually exclusive and comprehensive
        return match.group(0)  # Fallback: return the full match unchanged

    return re.sub(combined_pattern, replacer, text, flags=re.DOTALL)


def sanitize_title(title):
    title = unicodedata.normalize("NFKC", title)
    title = re.sub(r'[<>:"/\\|?*\x00-\x1F\s]', '_', title)
    # Strip leading/trailing spaces
    title = title.strip()
    # Remove trailing period (just one, if present)
    title = title.strip('.')
    return title[:140]


def read_file(file):
    """
    :param file: path to the txt file that stores conversations
    :return: a set of non-empty lines
    """
    with open(file, "r") as f:
        content = set(line.strip() for line in f if line.strip())
    return content


def clean_text(text):
    cleaned_text = "".join(char for char in text if char in string.printable)
    return re.sub(r"citeturn0search(\d+)", r"(See ref \1)", cleaned_text)

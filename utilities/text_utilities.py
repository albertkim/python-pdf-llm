import re

def clean_messy_string(text: str) -> str:
    if not text:
        return ""
    cleaned_text = text.replace(
        "\r\n", "\n"
    )  # Replace Windows newlines with Unix newlines
    cleaned_text = cleaned_text.replace("\t", "")  # Replace tabs with spaces
    cleaned_text = cleaned_text.replace("\\t", " ")  # Replace escaped tabs with spaces
    cleaned_text = "\n".join(
        " ".join(line.split())  # Remove consecutive spaces
        for line in cleaned_text.split("\n")
    )
    cleaned_text = re.sub(r"\n+", "\n", cleaned_text)  # Remove consecutive newlines
    return cleaned_text

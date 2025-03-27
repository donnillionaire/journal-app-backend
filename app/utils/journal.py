import re

# Helper function to clean and tokenize text
def tokenize_and_clean(text: str) -> list:
    # Remove punctuation and special characters
    text = re.sub(r"[^\w\s]", "", text.lower())
    # Split into words
    return text.split()

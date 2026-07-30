import re

def clean_text(text):
    """
    Cleans extracted PDF text.
    """

    # Remove tabs
    text = text.replace("\t", " ")

    # Remove multiple spaces
    text = re.sub(r" +", " ", text)

    # Remove 3 or more newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text
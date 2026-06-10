import re


def extract_email(text):

    match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    if match:
        return match.group(0)

    return ""


def extract_phone(text):

    match = re.search(
        r'\+?\d[\d\s\-]{8,15}',
        text
    )

    if match:
        return match.group(0)

    return ""
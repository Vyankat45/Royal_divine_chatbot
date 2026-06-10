import re

LEAD_KEYWORDS = [
    "buy",
    "purchase",
    "order",
    "quotation",
    "quote",
    "price",
    "supplier",
    "bulk"
]


def is_lead(question):

    question = question.lower()

    return any(
        keyword in question
        for keyword in LEAD_KEYWORDS
    )


def extract_quantity(question):

    match = re.search(
        r"(\d+)\s*(kg|kgs|kilogram|kilograms|ton|tons|tonne)",
        question.lower()
    )

    if match:
        return match.group(0)

    return ""


def extract_country(question):

    countries = [
        "india",
        "uae",
        "dubai",
        "saudi arabia",
        "oman",
        "qatar",
        "kuwait",
        "bahrain",
        "usa",
        "canada",
        "uk",
        "australia"
    ]

    question = question.lower()

    for country in countries:

        if country in question:
            return country.title()

    return ""
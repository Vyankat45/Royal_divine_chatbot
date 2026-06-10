import re


def extract_quantity_value(question):

    match = re.search(
        r"(\d+)\s*(kg|kgs|kilogram|kilograms|ton|tons|tonne)",
        question.lower()
    )

    if not match:
        return None, None

    quantity = int(match.group(1))
    unit = match.group(2)

    return quantity, unit


def is_below_moq(question):

    quantity, unit = extract_quantity_value(question)

    if quantity is None:
        return False

    # KG orders
    if unit in [
        "kg",
        "kgs",
        "kilogram",
        "kilograms"
    ]:
        return quantity < 100

    # Ton orders
    if unit in [
        "ton",
        "tons",
        "tonne"
    ]:
        return quantity < 1

    return False
from app.products import PRODUCTS


def detect_product(question):

    question = question.lower()

    for product in PRODUCTS:

        if product in question:
            return product

    return None
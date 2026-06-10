def get_search_filter(question: str):
    PRODUCTS = [
    "almond",
    "cashew",
    "dates",
    "pistachio",
    "walnuts",
    "peanuts",
    "turmeric",
    "cinnamon",
    "apple",
    "barley"
]
    for product in PRODUCTS:
        if product in question.lower():
            return {
                "product_name": product
            }
    else:
        return None
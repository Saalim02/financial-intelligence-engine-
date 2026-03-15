# utils/column_classifier.py

import re
from config.metric_rules import (
    REVENUE_KEYWORDS,
    COST_KEYWORDS,
    PROFIT_KEYWORDS,
    QUANTITY_KEYWORDS,
    PRICE_KEYWORDS
)

def normalize(col_name):
    return col_name.lower().replace(" ", "_")

def match_keywords(column, keywords):
    column = normalize(column)
    for word in keywords:
        if re.search(rf"\b{word}\b", column):
            return True
    return False

def classify_column(column):
    if match_keywords(column, REVENUE_KEYWORDS):
        return "revenue"

    if match_keywords(column, COST_KEYWORDS):
        return "cost"

    if match_keywords(column, PROFIT_KEYWORDS):
        return "profit"

    if match_keywords(column, QUANTITY_KEYWORDS):
        return "quantity"

    if match_keywords(column, PRICE_KEYWORDS):
        return "price"

    return "unknown"

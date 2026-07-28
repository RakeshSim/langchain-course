import logging

from langchain.tools import tool

logger = logging.getLogger(__name__)

_CATALOG = {"laptop": 1299.99, "headphones": 149.95, "keyboard": 89.50}
_DISCOUNT_TIERS = {"bronze": 5, "silver": 12, "gold": 23}


@tool
def get_product_price(product: str) -> float:
    """Look up the price of a product in the catalog."""
    logger.debug("get_product_price(product=%r)", product)

    key = product.strip().lower()
    if key not in _CATALOG:
        available = ", ".join(sorted(_CATALOG))
        raise ValueError(
            f"Unknown product '{product}'. Available products: {available}"
        )

    return _CATALOG[key]


@tool
def apply_discount(price: float, discount_tier: str) -> float:
    """Apply a discount tier to a price and return the final price.
    Available tiers: bronze, silver, gold."""
    logger.debug("apply_discount(price=%r, discount_tier=%r)", price, discount_tier)

    if price < 0:
        raise ValueError(f"price must not be negative, got {price}")

    tier = discount_tier.strip().lower()
    if tier not in _DISCOUNT_TIERS:
        available = ", ".join(sorted(_DISCOUNT_TIERS))
        raise ValueError(
            f"Unknown discount tier '{discount_tier}'. Available tiers: {available}"
        )

    discount = _DISCOUNT_TIERS[tier]
    return round(price * (1 - discount / 100), 2)

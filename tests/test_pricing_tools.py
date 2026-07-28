import pytest

from agent_under_hood.tools.pricing import apply_discount, get_product_price


def test_get_product_price_known_product():
    assert get_product_price.invoke({"product": "laptop"}) == 1299.99


def test_get_product_price_is_case_and_whitespace_insensitive():
    assert get_product_price.invoke({"product": "  Laptop "}) == 1299.99


def test_get_product_price_unknown_product_raises():
    with pytest.raises(ValueError, match="Unknown product"):
        get_product_price.invoke({"product": "smartphone"})


def test_apply_discount_gold_tier():
    assert apply_discount.invoke({"price": 1299.99, "discount_tier": "gold"}) == 1000.99


def test_apply_discount_unknown_tier_raises():
    with pytest.raises(ValueError, match="Unknown discount tier"):
        apply_discount.invoke({"price": 100.0, "discount_tier": "platinum"})


def test_apply_discount_negative_price_raises():
    with pytest.raises(ValueError, match="must not be negative"):
        apply_discount.invoke({"price": -50.0, "discount_tier": "bronze"})

import re
from typing import Any, Callable

from playwright.sync_api import Page, expect

Snap = Callable[[str], None]




def add_to_cart(page: Page, product_name: str, snap: Snap) -> None:
    item = page.locator('[data-test="inventory-item"]').filter(has_text=product_name)
    item.get_by_role("button", name="Add to cart").click()
    # Wait for the cart badge so the screenshot shows the updated page.
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")
    snap("product_added_to_cart")


def open_cart(page: Page, snap: Snap) -> None:
    page.locator('[data-test="shopping-cart-link"]').click()
    expect(page).to_have_url(re.compile(r".*/cart\.html"))
    snap("cart_page")


def fill_customer_info(page: Page, customer: dict[str, str], snap: Snap) -> None:
    page.locator('[data-test="firstName"]').fill(customer["first_name"])
    page.locator('[data-test="lastName"]').fill(customer["last_name"])
    page.locator('[data-test="postalCode"]').fill(customer["postal_code"])
    snap("customer_info_entered")
    page.locator('[data-test="continue"]').click()

# ---------- tests ----------

def test_tc01_successful_login(
    page: Page,
    base_url: str,
    valid_user: dict[str, str],
    test_data: dict[str, Any],
    snap: Snap,
) -> None:
    page.goto(base_url)
    snap("login_page")
    page.locator('[data-test="username"]').fill(valid_user["username"])
    page.locator('[data-test="password"]').fill(valid_user["password"])
    snap("credentials_entered")
    page.locator('[data-test="login-button"]').click()

    expect(page).to_have_url(re.compile(r".*/inventory\.html"))
    expect(page.locator('[data-test="title"]')).to_have_text(
        test_data["expected"]["inventory_title"]
    )
    snap("products_page")

def test_tc02_product_details(
    logged_in_page: Page,
    default_product: dict[str, str],
    test_data: dict[str, Any],
    snap: Snap,
) -> None:
    page = logged_in_page
    items = page.locator('[data-test="inventory-item"]')
    expect(items).to_have_count(test_data["expected"]["inventory_item_count"])

    page.locator('[data-test="inventory-item-name"]').filter(
        has_text=default_product["name"]
    ).click()

    expect(page).to_have_url(re.compile(r".*/inventory-item\.html"))
    expect(page.locator('[data-test="inventory-item-name"]')).to_have_text(
        default_product["name"]
    )
    expect(page.locator('[data-test="inventory-item-price"]')).to_have_text(
        default_product["price"]
    )
    expect(page.locator('[data-test="inventory-item-desc"]')).to_be_visible()
    snap("product_details_page")

def test_tc03_add_product_to_cart(
    logged_in_page: Page, product: dict[str, str], snap: Snap
) -> None:
    # `product` is parameterized in conftest.py: runs once per product in the JSON.
    page = logged_in_page
    add_to_cart(page, product["name"], snap)

    open_cart(page, snap)
    expect(page.locator('[data-test="inventory-item-name"]')).to_have_text(
        product["name"]
    )
    expect(page.locator('[data-test="inventory-item-price"]')).to_have_text(
        product["price"]
    )

def test_tc04_checkout_navigation(
    logged_in_page: Page,
    default_product: dict[str, str],
    customer: dict[str, str],
    test_data: dict[str, Any],
    snap: Snap,
) -> None:
    page = logged_in_page
    add_to_cart(page, default_product["name"], snap)
    open_cart(page, snap)
    page.locator('[data-test="checkout"]').click()
    expect(page).to_have_url(re.compile(r".*/checkout-step-one\.html"))
    snap("checkout_info_page")

    fill_customer_info(page, customer, snap)

    expect(page).to_have_url(re.compile(r".*/checkout-step-two\.html"))
    expect(page.locator('[data-test="title"]')).to_have_text(
        test_data["expected"]["overview_title"]
    )
    expect(page.locator('[data-test="inventory-item-name"]')).to_have_text(
        default_product["name"]
    )
    snap("checkout_overview_page")
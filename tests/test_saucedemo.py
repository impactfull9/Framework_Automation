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
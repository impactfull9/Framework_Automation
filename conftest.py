import itertools
import json
import re
import shutil
from pathlib import Path
from typing import Any, Callable
import logging 

import pytest
from playwright.sync_api import Page, expect

TEST_DATA_FILE = Path(__file__).parent / "testdata" / "test_data.json"
SCREENSHOT_DIR = Path(__file__).parent / "screenshots"
logger = logging.getLogger("saucedemo")


def _load_test_data() -> dict[str, Any]:
    with TEST_DATA_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Any test that has a `product` argument runs once per product in the JSON."""
    if "product" in metafunc.fixturenames:
        products = _load_test_data()["products"]
        metafunc.parametrize("product", products, ids=[p["id"] for p in products])


@pytest.fixture(scope="session")
def test_data() -> dict[str, Any]:
    return _load_test_data()


@pytest.fixture(scope="session")
def base_url(test_data: dict[str, Any]) -> str:
    return test_data["base_url"]


@pytest.fixture
def valid_user(test_data: dict[str, Any]) -> dict[str, str]:
    return test_data["users"]["valid"]


@pytest.fixture
def customer(test_data: dict[str, Any]) -> dict[str, str]:
    return test_data["customer"]


@pytest.fixture
def default_product(test_data: dict[str, Any]) -> dict[str, str]:
    return test_data["products"][0]


@pytest.fixture
def snap(page: Page, request: pytest.FixtureRequest) -> Callable[[str], None]:
    """Call snap("label") to save a numbered full-page screenshot for this test.

    Files go to screenshots/<test name>/01_label.png, 02_label.png, ...
    """
    folder_name = re.sub(r"[^\w.-]+", "_", request.node.name).strip("_")
    folder = SCREENSHOT_DIR / folder_name
    folder.mkdir(parents=True, exist_ok=True)
    for old_file in folder.glob("*.png"):  # clear leftovers from earlier runs
        try:
            old_file.unlink()
        except OSError:
            pass  # locked by OneDrive/Explorer; it will just be overwritten
    counter = itertools.count(1)

    def _snap(label: str) -> None:
        page.screenshot(path=str(folder / f"{next(counter):02d}_{label}.png"), full_page=True)

    return _snap

@pytest.fixture
def logged_in_page(
    page: Page,
    base_url: str,
    valid_user: dict[str, str],
    snap: Callable[[str], None],
) -> Page:
    """A page that is already logged in and sitting on the inventory page."""
    page.goto(base_url)
    snap("login_page")
    page.locator('[data-test="username"]').fill(valid_user["username"])
    page.locator('[data-test="password"]').fill(valid_user["password"])
    snap("credentials_entered")
    page.locator('[data-test="login-button"]').click()
    expect(page).to_have_url(re.compile(r".*/inventory\.html"))
    snap("inventory_page")
    return page

# ---------- logging of test results ----------

def _short_reason(report: pytest.TestReport) -> str:
    crash = getattr(report.longrepr, "reprcrash", None)
    if crash:
        return crash.message.splitlines()[0]
    return str(report.longrepr)[:300]


def pytest_runtest_logstart(nodeid: str, location: Any) -> None:
    logger.info("START   %s", nodeid)


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    if report.when == "call":
        if report.passed:
            logger.info("PASSED  %s", report.nodeid)
        elif report.failed:
            logger.error(
                "FAILED  %s | %s | screenshot and trace are in test-results/",
                report.nodeid,
                _short_reason(report),
            )
    elif report.failed:  # problem in setup or teardown
        logger.error(
            "ERROR   %s (%s) | %s", report.nodeid, report.when, _short_reason(report)
        )
    elif report.skipped and report.when == "setup":
        logger.warning("SKIPPED %s", report.nodeid)

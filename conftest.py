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
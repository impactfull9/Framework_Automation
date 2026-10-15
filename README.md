# SauceDemo Test Automation

End-to-end tests for https://www.saucedemo.com/ using **Python, pytest and Playwright**, with **uv** for dependency management.

## What is covered

| ID   | Scenario                                                            |
|------|---------------------------------------------------------------------|
| TC01 | Successful login and navigation to the Products page                |
| TC02 | Product list is displayed and a product's details page is correct   |
| TC03 | Add a product to the cart and verify it in the cart (per product)   |
| TC04 | Cart to checkout, enter customer info, reach the checkout overview  |
| TC05 | Complete purchase and verify the order confirmation                 |

TC03 runs once for every product listed in the test data file.

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
- Windows PowerShell (commands below work the same on other shells)

## Setup

```powershell
uv sync
uv run playwright install chromium
```

## Running the tests

```powershell
uv run pytest                          # headless
uv run pytest --headed                 # watch the browser
uv run pytest --headed --slowmo 2000   # watch, slowed down (ms per action)
uv run pytest -v                       # show test names
uv run pytest -k tc01                  # run one test
uv run pytest -k "tc03 and bike-light" # one product for TC03
```

A ready-to-copy list of commands is in `commands.py`.

## Project structure

```
.
├── conftest.py            shared fixtures, test data loading, screenshots helper
├── commands.py            copy-paste command reference
├── pyproject.toml         dependencies and pytest configuration
├── testdata/
│   └── test_data.json     URL, credentials, customer, products, expected texts
├── tests/
│   └── test_saucedemo.py  the test cases
├── screenshots/           step-by-step screenshots (created on run)
└── test-results/          failure screenshots and traces (created on run)
```

## Test data

All data lives in `testdata/test_data.json`. To add a product, append an object to the `products` list:

```json
{ "id": "bolt-tshirt", "name": "Sauce Labs Bolt T-Shirt", "price": "$15.99" }
```

No code changes are needed; TC03 will run for it automatically.

## Reports and evidence

| What                         | Where                                         | When                 |
|------------------------------|-----------------------------------------------|----------------------|
| Step-by-step screenshots     | `screenshots/<test name>/01_..., 02_...`      | Every run, every test |
| Failure screenshot           | `test-results/<test folder>/test-failed-1.png`| Failed tests only    |
| Playwright trace             | `test-results/<test folder>/trace.zip`        | Failed tests only    |

Open a trace with:

```powershell
uv run playwright show-trace test-results\<test folder>\trace.zip
```

`test-results/` is cleared at the start of every run. `screenshots/` is overwritten per test.

## Configuration

Defaults are set in `pyproject.toml` under `[tool.pytest.ini_options]`: Chromium, screenshots on failure (full page), traces retained on failure, output folder `test-results`.



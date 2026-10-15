# Project Notes

## How the files fit together

**`testdata/test_data.json`**: all test data (URL, login, customer, products, expected texts). Tests contain no hardcoded values.

**`conftest.py`**: shared setup that pytest loads automatically. It:
- loads the JSON and exposes it as fixtures (`test_data`, `valid_user`, `customer`, `default_product`)
- parameterizes any test that has a `product` argument, once per product in the JSON
- provides `base_url` from the JSON
- provides `snap`, which saves numbered full-page screenshots per test
- provides `logged_in_page`, a page that is already logged in

**`tests/test_saucedemo.py`**: the test cases, plus small helpers for repeated steps (`add_to_cart`, `open_cart`, `fill_customer_info`).

**`pyproject.toml`**: dependencies, and the pytest defaults so `uv run pytest` is enough.

**`conftest.py` vs the test file:** `conftest.py` prepares what tests need; the test file checks that the application works. Anything shared goes in `conftest.py`; anything specific to one scenario stays in the test file.

## Why fixtures --> 

A fixture is setup code written once and handed to any test that names it as an argument. This removes repeated steps (for example login), keeps tests short, and gives each test a fresh state. A fixture with `scope="session"` runs once per run (used for loading the JSON).

## Playwright features used

- Sync API with the `page` fixture (browser opened and closed automatically)
- Locators: `data-test` attributes, `filter(has_text=...)`, `get_by_role`
- Auto-waiting (no sleeps anywhere)
- `expect()` assertions that retry until true: `to_have_url`, `to_have_text`, `to_have_count`, `to_be_visible`
- Screenshots (`full_page=True`) and tracing (`retain-on-failure`)
- `--headed` and `--slowmo` for visible runs

## pytest features used

- Fixtures and fixture scopes
- `conftest.py`
- Parameterization via the `pytest_generate_tests` hook with custom ids
- The `request` fixture (current test name)
- Overriding a plugin fixture (`base_url`)
- Config in `pyproject.toml` (`addopts`, `testpaths`)
- Selection flags: `-k`, `--lf`, `-x`, `-v`, `--collect-only`

## Test IDs

Test IDs include the browser name, for example `test_tc03_add_product_to_cart[bike-light-chromium]`. Run `uv run pytest --collect-only -q` to see exact names, or use `-k` to avoid typing them.

## Troubleshooting

| Problem | Fix |
|---|---|
| `uv add` fails with "Access is denied" on `.venv` | Project is in a OneDrive folder. Move it outside OneDrive, or set `UV_PROJECT_ENVIRONMENT` to a folder outside it. |
| `Fixture 'test_data' ... unexpected scope value ''` | A fixture decorator in `conftest.py` is malformed. It must be `@pytest.fixture(scope="session")`. |
| `FileExistsError` for a screenshots folder | Use the `snap` fixture that creates the folder with `exist_ok=True`. |
| "not found" when running a test by exact ID | Include the browser suffix, e.g. `[chromium]` or `[bike-light-chromium]`, or use `-k`. |
| `Executable doesn't exist` | Run `uv run playwright install chromium`. |
| No tests collected | Files must start with `test_` and live in `tests/`; check with `--collect-only -q`. |
| No failure screenshot | Check `addopts` in `pyproject.toml`; look inside the subfolders of `test-results/`. |

## Possible next steps

Page Object Model, centralized configuration, logging, HTML/Allure reporting, timestamped artifact folders.


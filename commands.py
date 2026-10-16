# ---------- RUN TESTS ----------

# run all tests (no browser window)
r'''
uv run pytest
'''

# run all tests and watch the browser
r'''
uv run pytest --headed
'''

# watch the browser, slowed down (increase 2000 to go slower)
r'''
uv run pytest --headed --slowmo 2000
'''

# run with test names shown
r'''
uv run pytest -v
'''

# list the tests without running them
r'''
uv run pytest --collect-only -q
'''


# ---------- RUN SPECIFIC TESTS ----------

# one test (tc01 to tc05)
r'''
uv run pytest -k tc01
'''

# add-to-cart test for one product (backpack or bike-light)
r'''
uv run pytest -k "tc03 and bike-light"
'''

# one exact test
r'''
uv run pytest "tests/test_saucedemo.py::test_tc01_successful_login[chromium]"
'''

# re-run only the tests that failed last time
r'''
uv run pytest --lf
'''

# stop at the first failure
r'''
uv run pytest -x
'''


# ---------- SCREENSHOTS AND TRACES ----------

# open the step-by-step screenshots folder
r'''
explorer screenshots
'''

# open the failure screenshots and traces folder
r'''
explorer test-results
'''

# find trace files
r'''
Get-ChildItem test-results -Recurse -Filter trace.zip -Name
'''

# open a trace (replace FOLDER_NAME with the folder printed by the command above)
r'''
uv run playwright show-trace test-results\FOLDER_NAME\trace.zip
'''


# ---------- SHOW A FAILURE ON PURPOSE ----------

# step 1: in testdata/test_data.json change "Products" to "Productz" under inventory_title
# step 2: run TC01
r'''
uv run pytest -k tc01
'''

# step 3: open the failure screenshot and trace
r'''
explorer test-results
'''

# step 4: change "Productz" back to "Products" in testdata/test_data.json


# ---------- SETUP ----------

# install all packages (new machine)
r'''
uv sync
'''

# install the Chromium browser
r'''
uv run playwright install chromium
'''

# open the recordings folder
r'''
explorer recordings
'''

# list the recordings
r'''
Get-ChildItem recordings -Name
'''
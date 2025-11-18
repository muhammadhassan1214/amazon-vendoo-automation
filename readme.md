# Amazon → Vendoo Automation

Automates scraping product data from Amazon Seller Central and uploading it to Vendoo.

This repository contains a Selenium-based automation that:
- Reads ASINs from data/amazon-asins.csv
- Logs into Amazon Seller Central, searches each ASIN, extracts title, UPC, images and price
- Downloads product images to images/<ASIN>/
- Logs into Vendoo and creates a new listing using the scraped data and images
- Marks processed ASINs in data/done_asins.txt

---

Table of Contents
- Project structure
- Quick start (setup & run)
- Environment variables
- How it works (high-level flow)
- Important implementation notes
- Troubleshooting & common issues
- Development notes & next steps

Project structure

- src/
  - main.py                # Entry point (MainApp)
  - core/
    - amazon_scraper.py    # Amazon scraping page object (inherits BasePage)
    - vendoo_uploader.py   # Vendoo page object (inherits BasePage)
    - locators.py          # All Selenium locators for Amazon & Vendoo
  - utils/
    - base_page.py         # BasePage class with common Selenium helpers
    - static.py            # Small helpers (CSV reading, image download, file ops)
- data/
  - amazon-asins.csv       # Input CSV (expected ASIN in column index 6)
  - done_asins.txt         # Processed ASINs appended here
- images/                  # Downloaded images per ASIN
- requirements.txt         # Python dependencies

Quick start (setup & run)

1) Create a virtual environment and install dependencies

For Windows PowerShell:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt
```

2) Configure environment variables
- Create a .env file in the project root (see Environment variables section)

3) Prepare input CSV
- Place your amazon-asins.csv under the data/ folder. The code expects the ASIN to be present in column index 6 (the 7th column).

4) Run the script

```powershell
python -m src.main
```

Or directly:

```powershell
python src\main.py
```

Notes: the script will open Chrome and prompt for 2FA during Amazon login (it waits for you to press Enter after entering the 2FA code).

Environment variables

Create a `.env` file with at least:

- VENDOO_USERNAME=your_vendoo_email
- VENDOO_PASSWORD=your_vendoo_password

How it works (high-level flow)

1. main.py -> MainApp initializes a Chrome driver via BasePage.get_undetected_driver()
2. The app logs into Amazon Seller Central and navigates to the Add Products / search area
3. It reads ASINs from data/amazon-asins.csv and skips ASINs already listed in data/done_asins.txt
4. For each ASIN:
   - Search product in Seller Central
   - Open the product page in a new tab and extract title, UPC, images and price
   - Download all images to images/<ASIN>/
   - (On first product) log into Vendoo in a new tab
   - Create a new Vendoo listing, set title, price, notes, upload images
   - Mark ASIN as done and delete the temporary image folder

Important implementation notes

- BasePage
  - `src/utils/base_page.py` defines `BasePage` class which centralizes common Selenium helpers (click, input, wait, navigation, driver creation, etc.).
  - `get_undetected_driver(headless=False, max_retries=3)` returns a configured Chrome webdriver instance or `None` on failure.
  - AmazonScraper and VendooUploader inherit from `BasePage` so they can use helper methods directly (e.g., `click_element`, `input_element`).

- CSV format
  - The code expects the ASIN to be in column index 6 (7th column) of `data/amazon-asins.csv`. If your CSV layout differs, update `src/utils/static.py::read_csv_data()` accordingly.

- Image uploads
  - VendooUploader expects to `send_keys` a newline separated list of absolute file paths to the images input element. Ensure the browser session has access to the local filesystem paths.

Troubleshooting & common issues

1) AttributeError: module 'selectors' has no attribute 'SelectSelector'
   - Symptom: occurs while importing standard library modules (e.g. http.server, xmlrpc) or when launching some tools (PyCharm debugger). Root cause: a local module or file named `selectors.py` (or package named `selectors`) is shadowing Python's standard library `selectors` module.
   - Fixes to try:
     - Search the repository for a file named `selectors.py` and rename it -> `git mv selectors.py utils/selectors.py` or similar.
     - Remove stray compiled bytecode that may remain: delete any `__pycache__/selectors*.pyc` files and any top-level `selectors.pyc` files.
     - Run `python -c "import selectors; print(selectors.__file__)"` to see which file Python is importing. It should point to your Python installation's `selectors.py` in the standard library (e.g. .../lib/selectors.py). If it points to a project file, rename or remove that file.
     - After renaming/removing, restart the environment / IDE to clear import caches.

2) Chrome driver fails to start
   - Ensure Chrome is installed and `webdriver_manager` can download a chromedriver compatible with your Chrome version.
   - If the profile folder under `src/utils/chrome-dir` is corrupted, try removing it and letting the script recreate it.
   - If headless mode is required on your environment, call `BasePage.get_undetected_driver(headless=True)`.

3) Vendoo login does not complete
   - Check `.env` variables and that the Vendoo login flow hasn't changed (locators in `src/core/locators.py`).
   - Add extra waits or increase timeouts in `login_to_vendoo_account()` if your network is slow.

4) Images not found / upload fails
   - Verify image URLs are valid and that `requests` is allowed to fetch them from your environment.
   - Ensure Vendoo's file input accepts multiple file paths via newline in your browser/OS configuration.

Development notes & next steps

- Tests: there are currently no automated tests. Add unit tests for `src/utils/static.py` and simple integration smoke tests that mock the browser.
- Error handling: improve retry/backoff for network and driver operations.
- Config: move timeouts and other constants to a central config object or TOML/JSON file.
- Logging: consider adding file logging and per-run log file names for easier debugging.

If you want, I can also:
- Convert the existing `BasePage` module into a separate package-style class file (it's already a class — I can adapt call sites if you had a previous module-level API).
- Add a small CLI wrapper to accept a CSV path and other options.
- Add automated unit tests for `static.py` and linting.

---

Last updated: generated by repository analysis.


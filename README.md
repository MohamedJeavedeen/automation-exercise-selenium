# AutomationExercise Login/Logout Framework

Python + Selenium + Pytest framework using the Page Object Model (POM).

## Structure

```
automation_framework/
├── config/
│   ├── config.ini          # browser, base URL, timeouts, report paths
│   ├── credentials.env     # YOUR login/password (never commit this)
│   └── config_reader.py    # single source of truth for reading config
├── pages/
│   ├── base_page.py        # shared Selenium actions (click, type, wait, screenshot...)
│   ├── login_page.py       # login page locators + actions
│   └── home_page.py        # home page locators + logout action
├── tests/
│   └── test_login_logout.py
├── utils/
│   ├── driver_factory.py   # builds the WebDriver (Chrome via webdriver-manager)
│   └── logger.py           # rotating file + console logger
├── reports/                # HTML report generated after each run
├── screenshots/            # auto-captured on any failure
├── logs/                   # automation.log
├── conftest.py             # driver fixture + failure-screenshot hook
├── pytest.ini
└── requirements.txt
```

## One-time setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Open `config/credentials.env` and put in your real credentials:

```
APP_USERNAME=your_email@example.com
APP_PASSWORD=your_actual_password
```

This file is git-ignored — it will never be committed, and the tests
never read it any other way.

## Run the tests

```bash
pytest
```

This automatically:
- Launches Chrome (auto-managed by `webdriver-manager`, no manual driver download needed)
- Logs every action to `logs/automation.log`
- Generates `reports/report.html` (self-contained, open it in any browser)
- On any failure, saves a screenshot to `screenshots/`

Run only the login flow:
```bash
pytest -m login
```

Run headless (edit `config/config.ini`, set `headless = true`), useful for CI.

## Design notes

- **Page Object Model**: every page is a class inheriting `BasePage`.
  Tests never call Selenium directly — only page methods. If the UI
  changes, you touch one locator in one page class, not every test.
- **Config vs credentials separation**: `config.ini` is safe to commit
  (no secrets). `credentials.env` never is.
- **Logging**: every page action logs at DEBUG/INFO, failures log at
  ERROR with a screenshot path, so a failed CI run is debuggable without
  re-running it.
- **Extending it**: add new pages under `pages/`, new tests under
  `tests/`, and reuse `BasePage` helpers. To add Firefox/Edge, extend
  `DriverFactory.get_driver()` only.

## Known locator note

Locators for `login_page.py` / `home_page.py` are based on
automationexercise.com's `data-qa` attributes and nav structure, which
have been stable across the site's history. If the site's markup ever
changes, update the locator constants at the top of the relevant page
class — nothing else in the framework needs to change.

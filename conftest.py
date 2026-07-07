"""
conftest.py
-----------
Shared pytest fixtures and hooks for the whole test suite:

- `driver` fixture: creates a fresh browser per test, quits it afterwards.
- `pytest_runtest_makereport`: on failure, grabs a screenshot and (if
  pytest-html is active) embeds it directly into the HTML report.
"""

import os
import pytest

from utils.driver_factory import DriverFactory
from utils.logger import get_logger
from config.config_reader import ConfigReader

log = get_logger(__name__)


@pytest.fixture(scope="function")
def driver():
    log.info("===== TEST SETUP: starting browser =====")
    drv = DriverFactory.get_driver()
    yield drv
    log.info("===== TEST TEARDOWN: closing browser =====")
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    After each test phase (setup/call/teardown), check if it failed.
    If it did, take a screenshot using the test's `driver` fixture (if
    present) and attach it to the pytest-html report.
    """
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver", None)
        if driver_fixture is not None:
            screenshot_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                ConfigReader.get_screenshot_dir(),
            )
            os.makedirs(screenshot_dir, exist_ok=True)
            file_name = f"FAILED_{item.name}.png"
            file_path = os.path.join(screenshot_dir, file_name)
            try:
                driver_fixture.save_screenshot(file_path)
                log.error(f"Test failed. Screenshot saved: {file_path}")

                # Embed into pytest-html report if the plugin is active
                try:
                    import pytest_html

                    extra.append(pytest_html.extras.image(file_path))
                except ImportError:
                    pass
            except Exception as e:
                log.error(f"Could not capture failure screenshot: {e}")

    report.extra = extra


def pytest_configure(config):
    """Ensure required directories exist before the run starts."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for directory in (
        ConfigReader.get_log_dir(),
        ConfigReader.get_screenshot_dir(),
        ConfigReader.get_report_dir(),
    ):
        os.makedirs(os.path.join(base_dir, directory), exist_ok=True)

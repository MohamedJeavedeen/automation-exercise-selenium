"""
test_login_logout.py
---------------------
End-to-end flow:
  1. Open the login page
  2. Log in with valid credentials
  3. Verify the page title
  4. Log out
  5. (Driver cleanup handled by the `driver` fixture in conftest.py)
"""

import pytest

from pages.login_page import LoginPage
from pages.home_page import HomePage
from config.config_reader import ConfigReader
from utils.logger import get_logger

log = get_logger(__name__)


@pytest.mark.smoke
@pytest.mark.login
def test_login_verify_title_and_logout(driver):
    login_page = LoginPage(driver)
    home_page = HomePage(driver)

    # Step 1: open login page
    login_page.open_login_page()

    # Step 2: log in with valid credentials (from config/credentials.env)
    username = ConfigReader.get_username()
    password = ConfigReader.get_password()
    login_page.login(username, password)

    # Step 3: assert login succeeded, then verify page title
    assert home_page.is_logged_in(), (
        "Login did not succeed - 'Logged in as' text not found on home page"
    )
    log.info(f"Logged in as: {home_page.get_logged_in_username()}")

    actual_title = home_page.get_title()
    assert actual_title == HomePage.EXPECTED_TITLE, (
        f"Title mismatch. Expected '{HomePage.EXPECTED_TITLE}', "
        f"got '{actual_title}'"
    )

    # Step 4: log out
    home_page.logout()
    assert not home_page.is_logged_in(), "User is still logged in after logout"

    log.info("Login -> verify title -> logout flow completed successfully")

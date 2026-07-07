"""
home_page.py
------------
Page Object for the home page (https://automationexercise.com/) after a
successful login. Also owns the logout action, since "Logout" lives in
the top nav of this same page.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HomePage(BasePage):

    # ---- Locators ----
    LOGGED_IN_AS_TEXT = (By.XPATH, "//a[contains(text(),'Logged in as')]")
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href='/logout']")

    EXPECTED_TITLE = "Automation Exercise"

    def is_logged_in(self):
        return self.is_displayed(self.LOGGED_IN_AS_TEXT)

    def get_logged_in_username(self):
        full_text = self.get_text(self.LOGGED_IN_AS_TEXT)
        # Text looks like "Logged in as <username>"
        return full_text.replace("Logged in as", "").strip()

    def logout(self):
        self.log.info("Logging out")
        self.click(self.LOGOUT_LINK)

"""
login_page.py
--------------
Page Object for https://automationexercise.com/login

NOTE ON LOCATORS: these match automationexercise.com's long-standing DOM
structure (used across most public tutorials/repos for this site). Sites
do change over time -- if a locator ever fails, open browser DevTools,
inspect the element, and update ONLY the locator constant here. Nothing
in the test layer should need to change.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.config_reader import ConfigReader


class LoginPage(BasePage):

    # ---- Locators ----
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-qa='login-button']")
    LOGIN_ERROR_MSG = (By.CSS_SELECTOR, "form[action='/login'] p")

    LOGIN_URL_PATH = "/login"

    def open_login_page(self):
        base_url = ConfigReader.get_base_url()
        self.open(f"{base_url}{self.LOGIN_URL_PATH}")
        return self

    def enter_email(self, email):
        self.type_text(self.EMAIL_INPUT, email)
        return self

    def enter_password(self, password):
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        self.click(self.LOGIN_BUTTON)
        return self

    def login(self, email, password):
        """Convenience method composing the full login action."""
        self.log.info(f"Attempting login with email: {email}")
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self):
        return self.get_text(self.LOGIN_ERROR_MSG)

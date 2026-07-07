"""
base_page.py
------------
Every page object inherits from BasePage. It holds the driver, explicit
wait, and the low-level actions (click, type, get text, etc.) so
individual page classes only describe locators + business actions,
never raw Selenium calls.
"""

import os
from datetime import datetime

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
)

from config.config_reader import ConfigReader
from utils.logger import get_logger


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, ConfigReader.get_explicit_wait())
        self.log = get_logger(self.__class__.__name__)

    def open(self, url):
        self.log.info(f"Navigating to URL: {url}")
        self.driver.get(url)

    def _wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def _wait_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        try:
            element = self._wait_clickable(locator)
            element.click()
            self.log.debug(f"Clicked on element: {locator}")
        except (TimeoutException, ElementClickInterceptedException) as e:
            self.log.error(f"Failed to click element {locator}: {e}")
            self.take_screenshot(f"click_failed_{locator[1]}")
            raise

    def type_text(self, locator, text):
        try:
            element = self._wait_visible(locator)
            element.clear()
            element.send_keys(text)
            self.log.debug(f"Typed '{text}' into element: {locator}")
        except TimeoutException as e:
            self.log.error(f"Failed to type into element {locator}: {e}")
            self.take_screenshot(f"type_failed_{locator[1]}")
            raise

    def get_text(self, locator):
        element = self._wait_visible(locator)
        text = element.text
        self.log.debug(f"Read text '{text}' from element: {locator}")
        return text

    def is_displayed(self, locator, timeout_ok=True):
        try:
            return self._wait_visible(locator).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False if timeout_ok else self._raise_not_found(locator)

    def get_title(self):
        title = self.driver.title
        self.log.info(f"Page title: {title}")
        return title

    def get_current_url(self):
        return self.driver.current_url

    def take_screenshot(self, name):
        screenshot_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            ConfigReader.get_screenshot_dir(),
        )
        os.makedirs(screenshot_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(screenshot_dir, f"{name}_{timestamp}.png")
        self.driver.save_screenshot(filepath)
        self.log.info(f"Screenshot saved: {filepath}")
        return filepath

    @staticmethod
    def _raise_not_found(locator):
        raise NoSuchElementException(f"Element not found: {locator}")

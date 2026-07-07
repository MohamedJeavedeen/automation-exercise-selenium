"""
driver_factory.py
------------------
Responsible only for creating a configured WebDriver instance.
Keeping this separate means adding a new browser (Firefox, Edge, etc.)
or switching to a grid/remote driver later touches only this file.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from config.config_reader import ConfigReader
from utils.logger import get_logger

log = get_logger(__name__)


class DriverFactory:

    @staticmethod
    def get_driver():
        browser = ConfigReader.get_browser().lower()
        log.info(f"Initializing WebDriver for browser: {browser}")

        if browser == "chrome":
            options = ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-extensions")
            if ConfigReader.is_headless():
                #options.add_argument("--headless=new")
                options.add_argument("--window-size=1920,1080")

            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

        else:
            raise ValueError(
                f"Unsupported browser '{browser}'. Add support for it in "
                f"DriverFactory.get_driver()."
            )

        driver.implicitly_wait(ConfigReader.get_implicit_wait())
        log.info("WebDriver initialized successfully")
        return driver

"""
config_reader.py
-----------------
Central place to read framework configuration (config.ini) and
credentials (credentials.env). Nothing else in the framework should
open these files directly -- everything goes through this module so
there's a single source of truth.
"""

import configparser
import os
from dotenv import load_dotenv

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.ini")
CREDENTIALS_FILE = os.path.join(CONFIG_DIR, "credentials.env")

_config = configparser.ConfigParser()
_config.read(CONFIG_FILE)

load_dotenv(CREDENTIALS_FILE)


class ConfigReader:

    @staticmethod
    def get_base_url():
        return _config.get("ENVIRONMENT", "base_url")

    @staticmethod
    def get_browser():
        return _config.get("ENVIRONMENT", "browser")

    @staticmethod
    def get_implicit_wait():
        return _config.getint("ENVIRONMENT", "implicit_wait")

    @staticmethod
    def get_explicit_wait():
        return _config.getint("ENVIRONMENT", "explicit_wait")

    @staticmethod
    def is_headless():
        return _config.getboolean("ENVIRONMENT", "headless")

    @staticmethod
    def get_report_dir():
        return _config.get("REPORTS", "report_dir")

    @staticmethod
    def get_screenshot_dir():
        return _config.get("REPORTS", "screenshot_dir")

    @staticmethod
    def get_log_dir():
        return _config.get("REPORTS", "log_dir")

    @staticmethod
    def get_username():
        username = os.getenv("APP_USERNAME")
        if not username:
            raise ValueError(
                "APP_USERNAME not found. Set it in config/credentials.env"
            )
        return username

    @staticmethod
    def get_password():
        password = os.getenv("APP_PASSWORD")
        if not password:
            raise ValueError(
                "APP_PASSWORD not found. Set it in config/credentials.env"
            )
        return password

"""
conftest.py — Shared pytest fixtures for Digipay E2E Test Suite
Initialises headless Chrome WebDriver and exposes URL / auth helpers.
"""

import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ─────────────────────────────────────────────────────────────────────────────
# Configuration – override with environment variables in GitHub Actions
# ─────────────────────────────────────────────────────────────────────────────
BASE_URL = os.environ.get(
    "DIGIPAY_BASE_URL",
    "https://harishbalaji826-ops.github.io/digipay-Web/"
)
BACKEND_URL = os.environ.get(
    "DIGIPAY_BACKEND_URL",
    "https://digipay-backend.railway.app"
)
ADMIN_PHONE = os.environ.get("ADMIN_PHONE", "9999999999")
DEFAULT_TIMEOUT = int(os.environ.get("SELENIUM_TIMEOUT", "20"))


# ─────────────────────────────────────────────────────────────────────────────
# WebDriver factory
# ─────────────────────────────────────────────────────────────────────────────
def build_driver() -> webdriver.Chrome:
    """Build and return a headless Chrome WebDriver."""
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--disable-extensions")
    opts.add_argument("--disable-infobars")
    opts.add_argument("--ignore-certificate-errors")
    opts.add_argument("--allow-insecure-localhost")
    # Suppress console noise
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    opts.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
    })

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(5)
    return driver


# ─────────────────────────────────────────────────────────────────────────────
# Session-scoped driver  (reused across entire test session for speed)
# ─────────────────────────────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def driver():
    d = build_driver()
    yield d
    d.quit()


# ─────────────────────────────────────────────────────────────────────────────
# Function-scoped driver  (fresh browser for isolation-sensitive tests)
# ─────────────────────────────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def fresh_driver():
    d = build_driver()
    yield d
    d.quit()


# ─────────────────────────────────────────────────────────────────────────────
# Helper: navigate to landing page
# ─────────────────────────────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def landing(driver):
    driver.get(BASE_URL)
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    return driver


# ─────────────────────────────────────────────────────────────────────────────
# Helper: open login portal (clicks Sign In on landing)
# ─────────────────────────────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def login_portal(driver):
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='login-nav-button']")))
    btn.click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='phone-input']")))
    return driver


# ─────────────────────────────────────────────────────────────────────────────
# Shared constants accessible from test modules
# ─────────────────────────────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def app_config():
    return {
        "base_url": BASE_URL,
        "backend_url": BACKEND_URL,
        "admin_phone": ADMIN_PHONE,
        "timeout": DEFAULT_TIMEOUT,
    }

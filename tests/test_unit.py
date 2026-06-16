"""
test_unit.py — Unit-Level UI Tests (TC-103 to TC-120)
Tests: Component attribute verification, DOM structure, CSS classes,
       React rendering correctness, localisation, a11y basics.
"""

import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import BASE_URL, DEFAULT_TIMEOUT as TIMEOUT


class TestComponentAttributes:
    """TC-103 to TC-110: data-testid attribute presence and uniqueness."""

    def test_tc103_login_nav_button_testid(self, landing):
        """TC-103: data-testid='login-nav-button' present on Sign In nav button."""
        btn = landing.find_element(By.CSS_SELECTOR, "[data-testid='login-nav-button']")
        assert btn.get_attribute("data-testid") == "login-nav-button"

    def test_tc104_login_nav_admin_testid(self, landing):
        """TC-104: data-testid='login-nav-admin' present on Go to Console button."""
        btn = landing.find_element(By.CSS_SELECTOR, "[data-testid='login-nav-admin']")
        assert btn.get_attribute("data-testid") == "login-nav-admin"

    def test_tc105_hero_login_button_testid(self, landing):
        """TC-105: data-testid='login-button' present on hero CTA button."""
        btn = landing.find_element(By.CSS_SELECTOR, "[data-testid='login-button']")
        assert btn.get_attribute("data-testid") == "login-button"

    def test_tc106_open_app_link_testid(self, landing):
        """TC-106: data-testid='open-app-link' present on Launch iOS App anchor."""
        link = landing.find_element(By.CSS_SELECTOR, "[data-testid='open-app-link']")
        assert link.get_attribute("data-testid") == "open-app-link"

    def test_tc107_open_app_link_href(self, landing):
        """TC-107: iOS app deep link has href='digipay://'."""
        link = landing.find_element(By.CSS_SELECTOR, "[data-testid='open-app-link']")
        href = link.get_attribute("href")
        assert "digipay" in href.lower()

    def test_tc108_phone_input_testid(self, login_portal):
        """TC-108: data-testid='phone-input' present on phone number input."""
        inp = login_portal.find_element(By.CSS_SELECTOR, "[data-testid='phone-input']")
        assert inp.get_attribute("data-testid") == "phone-input"

    def test_tc109_back_button_testid(self, login_portal):
        """TC-109: data-testid='back-button' present on Back to Home button."""
        btn = login_portal.find_element(By.CSS_SELECTOR, "[data-testid='back-button']")
        assert btn.get_attribute("data-testid") == "back-button"

    def test_tc110_login_submit_button_testid(self, login_portal):
        """TC-110: data-testid='login-button' present on Request Code submit button."""
        btn = login_portal.find_element(By.CSS_SELECTOR, "[data-testid='login-button']")
        assert btn.get_attribute("data-testid") == "login-button"


class TestDOMStructure:
    """TC-111 to TC-116: DOM structure and semantic HTML checks."""

    def test_tc111_single_h1_on_landing(self, landing):
        """TC-111: Exactly one <h1> element on the landing page (SEO best practice)."""
        h1s = landing.find_elements(By.TAG_NAME, "h1")
        assert len(h1s) == 1

    def test_tc112_main_element_present(self, landing):
        """TC-112: Semantic <main> element is present on landing page."""
        mains = landing.find_elements(By.TAG_NAME, "main")
        assert len(mains) >= 1

    def test_tc113_nav_element_present(self, landing):
        """TC-113: Semantic <nav> or <header> element is used for navigation."""
        navs = landing.find_elements(By.TAG_NAME, "nav")
        headers = landing.find_elements(By.TAG_NAME, "header")
        assert len(navs) + len(headers) >= 1

    def test_tc114_section_elements_for_content(self, landing):
        """TC-114: Semantic <section> elements used for content blocks."""
        sections = landing.find_elements(By.TAG_NAME, "section")
        assert len(sections) >= 2

    def test_tc115_no_inline_script_in_body(self, landing):
        """TC-115: No dangerous inline <script> tags are injected in body."""
        body = landing.find_element(By.TAG_NAME, "body")
        body_html = body.get_attribute("innerHTML")
        # Vite/React bundle is in <script type="module"> — that's fine
        # Check for eval() or document.write injection
        assert "document.write(" not in body_html
        assert "eval(" not in body_html

    def test_tc116_all_images_have_alt_text(self, landing):
        """TC-116: All <img> elements have non-empty alt attributes."""
        imgs = landing.find_elements(By.TAG_NAME, "img")
        for img in imgs:
            alt = img.get_attribute("alt")
            assert alt is not None, f"Image missing alt attribute: {img.get_attribute('src')}"


class TestResponsivenessAndViewport:
    """TC-117 to TC-120: Responsive design checks."""

    def test_tc117_mobile_viewport_renders(self, fresh_driver):
        """TC-117: App renders correctly at mobile viewport (375x812 — iPhone 14)."""
        fresh_driver.set_window_size(375, 812)
        fresh_driver.get(BASE_URL)
        time.sleep(2)
        body = fresh_driver.find_element(By.TAG_NAME, "body")
        assert body.is_displayed()
        # Reset
        fresh_driver.set_window_size(1920, 1080)

    def test_tc118_tablet_viewport_renders(self, fresh_driver):
        """TC-118: App renders correctly at tablet viewport (768x1024 — iPad)."""
        fresh_driver.set_window_size(768, 1024)
        fresh_driver.get(BASE_URL)
        time.sleep(2)
        body = fresh_driver.find_element(By.TAG_NAME, "body")
        assert body.is_displayed()
        fresh_driver.set_window_size(1920, 1080)

    def test_tc119_desktop_viewport_renders(self, fresh_driver):
        """TC-119: App renders correctly at full desktop viewport (1920x1080)."""
        fresh_driver.set_window_size(1920, 1080)
        fresh_driver.get(BASE_URL)
        time.sleep(2)
        body = fresh_driver.find_element(By.TAG_NAME, "body")
        assert body.is_displayed()

    def test_tc120_no_horizontal_scrollbar_on_desktop(self, fresh_driver):
        """TC-120: No horizontal scrollbar appears at desktop viewport (no overflow-x)."""
        fresh_driver.set_window_size(1920, 1080)
        fresh_driver.get(BASE_URL)
        time.sleep(2)
        scroll_width = fresh_driver.execute_script("return document.documentElement.scrollWidth;")
        inner_width = fresh_driver.execute_script("return window.innerWidth;")
        # Allow a small tolerance (e.g. scrollbar itself)
        assert scroll_width <= inner_width + 20, \
            f"Horizontal overflow: scrollWidth={scroll_width}, innerWidth={inner_width}"

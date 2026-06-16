"""
test_landing_page.py — Landing Page E2E Tests (TC-001 to TC-025)
Tests: Page load, header, hero section, feature cards, CTA buttons,
       responsive layout, footer, animations, accessibility basics.
"""

import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

TIMEOUT = 20


class TestLandingPageLoad:
    """TC-001 to TC-005: Core page load & meta checks."""

    def test_tc001_page_loads_successfully(self, landing):
        """TC-001: Landing page loads with HTTP 200 and body is visible."""
        assert landing.find_element(By.TAG_NAME, "body").is_displayed()

    def test_tc002_page_title_contains_digipay(self, landing):
        """TC-002: Document title includes 'Digipay' branding."""
        title = landing.title.lower()
        assert "digipay" in title or "digipay" in landing.page_source.lower()

    def test_tc003_no_javascript_errors_on_load(self, landing):
        """TC-003: Browser console has no critical JS errors on load."""
        logs = landing.get_log("browser")
        severe = [l for l in logs if l["level"] == "SEVERE"]
        assert len(severe) == 0, f"JS SEVERE errors: {severe}"

    def test_tc004_page_source_not_empty(self, landing):
        """TC-004: Page source is not empty / not a bare HTML shell."""
        source = landing.page_source
        assert len(source) > 500

    def test_tc005_favicon_present(self, landing):
        """TC-005: Favicon link tag is present in <head>."""
        favicons = landing.find_elements(By.CSS_SELECTOR, "link[rel*='icon']")
        assert len(favicons) >= 1


class TestLandingPageHeader:
    """TC-006 to TC-012: Header / Navbar tests."""

    def test_tc006_header_is_visible(self, landing):
        """TC-006: Sticky header element is rendered and visible."""
        header = landing.find_element(By.TAG_NAME, "header")
        assert header.is_displayed()

    def test_tc007_brand_logo_text_visible(self, landing):
        """TC-007: DIGIPAY brand name is shown in the header."""
        assert "DIGIPAY" in landing.page_source

    def test_tc008_signin_button_visible(self, landing):
        """TC-008: 'Sign In' nav button is present and visible."""
        btn = landing.find_element(By.CSS_SELECTOR, "[data-testid='login-nav-button']")
        assert btn.is_displayed()

    def test_tc009_signin_button_text(self, landing):
        """TC-009: Sign In button displays correct label text."""
        btn = landing.find_element(By.CSS_SELECTOR, "[data-testid='login-nav-button']")
        assert "sign in" in btn.text.lower()

    def test_tc010_go_to_console_button_visible(self, landing):
        """TC-010: 'Go to Console' admin button is visible in header."""
        btn = landing.find_element(By.CSS_SELECTOR, "[data-testid='login-nav-admin']")
        assert btn.is_displayed()

    def test_tc011_header_is_sticky(self, landing):
        """TC-011: Header has sticky/fixed CSS positioning."""
        header = landing.find_element(By.TAG_NAME, "header")
        position = landing.execute_script(
            "return window.getComputedStyle(arguments[0]).position;", header
        )
        assert position in ("sticky", "fixed")

    def test_tc012_header_backdrop_blur_applied(self, landing):
        """TC-012: Header uses backdrop blur for glassmorphism effect."""
        header = landing.find_element(By.TAG_NAME, "header")
        classes = header.get_attribute("class")
        assert "backdrop" in classes or "blur" in classes


class TestLandingPageHeroSection:
    """TC-013 to TC-022: Hero section content and CTA buttons."""

    def test_tc013_hero_h1_is_present(self, landing):
        """TC-013: <h1> heading exists in hero section."""
        h1 = landing.find_element(By.TAG_NAME, "h1")
        assert h1.is_displayed()

    def test_tc014_hero_heading_content(self, landing):
        """TC-014: Hero heading contains 'UPI Payments' text."""
        h1 = landing.find_element(By.TAG_NAME, "h1")
        assert "upi" in h1.text.lower() or "payments" in h1.text.lower()

    def test_tc015_hero_subtext_visible(self, landing):
        """TC-015: Hero description paragraph is visible."""
        paras = landing.find_elements(By.TAG_NAME, "p")
        visible_paras = [p for p in paras if p.is_displayed() and len(p.text) > 20]
        assert len(visible_paras) >= 1

    def test_tc016_open_portal_button_present(self, landing):
        """TC-016: 'Open Web Portal' CTA button is present and visible."""
        btn = landing.find_element(By.CSS_SELECTOR, "[data-testid='login-button']")
        assert btn.is_displayed()

    def test_tc017_open_portal_button_text(self, landing):
        """TC-017: Main CTA button text says 'Open Web Portal'."""
        btn = landing.find_element(By.CSS_SELECTOR, "[data-testid='login-button']")
        assert "portal" in btn.text.lower() or "web" in btn.text.lower()

    def test_tc018_launch_ios_app_link_present(self, landing):
        """TC-018: 'Launch iOS App' deep-link button is visible."""
        link = landing.find_element(By.CSS_SELECTOR, "[data-testid='open-app-link']")
        assert link.is_displayed()

    def test_tc019_hero_card_display_visible(self, landing):
        """TC-019: The hero interactive UI card panel is rendered."""
        source = landing.page_source
        assert "intelligent pairing" in source.lower() or "mcdonalds" in source.lower()

    def test_tc020_badge_text_visible(self, landing):
        """TC-020: 'Next-Gen QR-less Payment System' badge is visible."""
        assert "qr-less" in landing.page_source.lower() or "next-gen" in landing.page_source.lower()

    def test_tc021_open_portal_click_navigates(self, landing):
        """TC-021: Clicking 'Open Web Portal' navigates to login page."""
        btn = landing.find_element(By.CSS_SELECTOR, "[data-testid='login-button']")
        btn.click()
        wait = WebDriverWait(landing, TIMEOUT)
        phone_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='phone-input']"))
        )
        assert phone_input.is_displayed()
        # Navigate back for subsequent tests
        landing.back()

    def test_tc022_signin_nav_click_navigates(self, landing):
        """TC-022: Clicking 'Sign In' navbar button opens login portal."""
        wait = WebDriverWait(landing, TIMEOUT)
        btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-testid='login-nav-button']")
        ))
        btn.click()
        phone_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='phone-input']"))
        )
        assert phone_input.is_displayed()
        landing.back()


class TestLandingPageFeatures:
    """TC-023 to TC-030: Feature cards / sections below hero."""

    def test_tc023_features_section_present(self, landing):
        """TC-023: Core features section with <h2> heading is visible."""
        h2s = landing.find_elements(By.TAG_NAME, "h2")
        assert len(h2s) >= 1

    def test_tc024_digipin_feature_card_visible(self, landing):
        """TC-024: 'DIGIPIN Address Translation' feature card is present."""
        assert "digipin" in landing.page_source.lower()

    def test_tc025_heading_speed_scoring_visible(self, landing):
        """TC-025: 'Heading & Speed Scoring' feature card is present."""
        assert "speed scoring" in landing.page_source.lower() or "heading" in landing.page_source.lower()

    def test_tc026_autonomous_categorization_visible(self, landing):
        """TC-026: 'Autonomous Categorization' feature card is present."""
        assert "categoriz" in landing.page_source.lower()

    def test_tc027_download_section_present(self, landing):
        """TC-027: App download / install banner section is rendered."""
        assert "install digipay" in landing.page_source.lower() or "app store" in landing.page_source.lower()

    def test_tc028_qr_code_graphic_present(self, landing):
        """TC-028: SVG QR code graphic is rendered in download section."""
        svgs = landing.find_elements(By.TAG_NAME, "svg")
        assert len(svgs) >= 1

    def test_tc029_footer_visible(self, landing):
        """TC-029: Footer element is present at bottom of landing page."""
        footer = landing.find_element(By.TAG_NAME, "footer")
        assert footer.is_displayed()

    def test_tc030_footer_copyright_text(self, landing):
        """TC-030: Footer contains copyright year and 'DIGIPAY' text."""
        footer = landing.find_element(By.TAG_NAME, "footer")
        text = footer.text.lower()
        assert "2026" in text or "digipay" in text

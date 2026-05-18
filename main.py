import os

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load credentials
load_dotenv()

USERNAME = os.getenv("ERP_USERNAME")
PASSWORD = os.getenv("ERP_PASSWORD")

TARGET_RESULT = "SP2026"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    # Open ERP directly
    page.goto("https://erpportal.bitmesra.ac.in")

    print("ERP opened.")

    # Fill login
    page.fill("#j_username", USERNAME)
    page.fill("#password-1", PASSWORD)

    page.get_by_role("button", name="Login").click()

    print("Login submitted.")

    page.wait_for_timeout(3000)

    # Navigate menus
    page.get_by_text("Academic Functions").click()

    page.wait_for_timeout(1000)

    page.get_by_text("University Exam/Result").click()

    page.wait_for_timeout(1000)

    page.get_by_text("Autonomous Student Result").click()

    print("Result page opened.")

    page.wait_for_timeout(3000)

    # Read page content
    page_text = page.inner_text("body")

    if TARGET_RESULT in page_text:
        print(f"\n{TARGET_RESULT} RESULT FOUND!")
    else:
        print(f"\n{TARGET_RESULT} not available yet.")

    input("\nPress Enter to close browser...")

    browser.close()
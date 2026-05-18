import os

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load environment variables
load_dotenv()

USERNAME = os.getenv("ERP_USERNAME")
PASSWORD = os.getenv("ERP_PASSWORD")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context()

    page = context.new_page()

    page.goto("https://www.bitmesra.ac.in/")

    print("BIT Mesra website opened.")
    print("Click ERP manually...")

    erp_page = context.wait_for_event("page")

    erp_page.wait_for_load_state()

    print("\nERP login page loaded.")

    # Fill credentials
    erp_page.fill("#j_username", USERNAME)
    erp_page.fill("#password-1", PASSWORD)

    print("Credentials filled.")

    # Click login button
    erp_page.get_by_role("button", name="Login").click()

    print("Login button clicked.")

    # Wait 10 seconds
    erp_page.wait_for_timeout(10000)

    input("\nObserve what happens, then press Enter to close browser...")
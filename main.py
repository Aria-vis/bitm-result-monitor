import os

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load credentials
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

    # Login
    erp_page.fill("#j_username", USERNAME)
    erp_page.fill("#password-1", PASSWORD)

    erp_page.get_by_role("button", name="Login").click()

    print("Login submitted.")

    # Wait for dashboard
    erp_page.wait_for_load_state()

    # Small stabilization delay
    erp_page.wait_for_timeout(3000)

    print("Dashboard loaded.")

    # Open Academic Functions
    erp_page.get_by_text("Academic Functions").click()

    print("Academic Functions opened.")

    erp_page.wait_for_timeout(1000)

    # Open University Exam/Result
    erp_page.get_by_text("University Exam/Result").click()

    print("University Exam/Result opened.")

    erp_page.wait_for_timeout(1000)

    # Open Autonomous Student Result
    erp_page.get_by_text("Autonomous Student Result").click()

    print("Autonomous Student Result clicked.")

    erp_page.wait_for_timeout(10000)

    input("\nObserve result page, then press Enter to close browser...")

    browser.close()
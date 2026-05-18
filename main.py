from playwright.sync_api import sync_playwright

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

    # Fill dummy values
    erp_page.fill("#j_username", "test_user")
    erp_page.fill("#password-1", "test_password")

    print("\nDummy credentials filled successfully.")

    input("\nVerify fields visually, then press Enter to close browser...")

    browser.close()
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context()

    page = context.new_page()

    page.goto("https://www.bitmesra.ac.in/")

    print("BIT Mesra website opened.")
    print("Click ERP manually...")

    # Wait for new ERP tab
    erp_page = context.wait_for_event("page")

    print("\nERP tab detected.")

    erp_page.wait_for_load_state()

    print("\nERP URL:")
    print(erp_page.url)

    input("\nPress Enter to close browser...")

    browser.close()
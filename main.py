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

    inputs = erp_page.locator("input")

    count = inputs.count()

    print(f"\nFound {count} input fields:\n")

    for i in range(count):
        field = inputs.nth(i)

        print(f"Field {i+1}:")
        print("Type:", field.get_attribute("type"))
        print("Name:", field.get_attribute("name"))
        print("ID:", field.get_attribute("id"))
        print("------------------------")

    input("\nPress Enter to close browser...")

    browser.close()
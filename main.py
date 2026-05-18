import os
import time

from dotenv import load_dotenv
from playsound import playsound
from playwright.sync_api import sync_playwright

# Load environment variables
load_dotenv()

USERNAME = os.getenv("ERP_USERNAME")
PASSWORD = os.getenv("ERP_PASSWORD")

TARGET_RESULT = "SP2026"

CHECK_INTERVAL = 300  # 5 minutes

SOUND_FILE = "assets/alert.mp3"


def check_result():
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        try:
            print("\nOpening ERP portal...")

            page.goto("https://erpportal.bitmesra.ac.in", timeout=60000)

            # Login
            page.fill("#j_username", USERNAME)
            page.fill("#password-1", PASSWORD)

            page.get_by_role("button", name="Login").click()

            print("Login successful.")

            page.wait_for_timeout(3000)

            # Navigate menus
            page.get_by_text("Academic Functions").click()

            page.wait_for_timeout(1000)

            page.get_by_text("University Exam/Result").click()

            page.wait_for_timeout(1000)

            page.get_by_text("Autonomous Student Result").click()

            print("Reached result page.")

            page.wait_for_timeout(3000)

            # Read page content
            page_text = page.inner_text("body")

            if TARGET_RESULT in page_text:

                print(f"\n{TARGET_RESULT} RESULT FOUND!")

                # Play alert sound
                playsound(SOUND_FILE)

                browser.close()

                return True

            else:
                print(f"\n{TARGET_RESULT} not available yet.")

        except Exception as e:

            print("\nError occurred:")
            print(e)

            print("\nWill retry after 5 minutes...")

        browser.close()

        return False


# Monitoring loop
while True:

    found = check_result()

    if found:
        print("\nMonitoring stopped.")
        break

    print(f"\nWaiting {CHECK_INTERVAL // 60} minutes before next check...\n")

    time.sleep(CHECK_INTERVAL)
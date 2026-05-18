import os
import time
import requests

from datetime import datetime

from dotenv import load_dotenv
from playsound import playsound
from playwright.sync_api import sync_playwright


# =========================
# Logging Helper
# =========================

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


# =========================
# Load Environment Variables
# =========================

load_dotenv()

USERNAME = os.getenv("ERP_USERNAME")
PASSWORD = os.getenv("ERP_PASSWORD")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TARGET_RESULT = os.getenv("TARGET_RESULT", "SP2026")

CHECK_INTERVAL = 300  # 5 minutes

SOUND_FILE = "assets/alert.mp3"


# =========================
# Telegram Notification
# =========================

def send_telegram_message(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, data=data)

        result = response.json()

        log(f"Telegram response: {result}")

        return result.get("ok", False)

    except Exception as e:
        log(f"Telegram error: {e}")
        return False


# =========================
# Result Checking Logic
# =========================

def check_result():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        try:

            log("Opening ERP portal...")

            page.goto(
                "https://erpportal.bitmesra.ac.in",
                timeout=60000
            )

            # Login
            page.fill("#j_username", USERNAME)
            page.fill("#password-1", PASSWORD)

            page.get_by_role("button", name="Login").click()

            log("Login successful.")

            page.wait_for_timeout(3000)

            # Navigate menus
            page.get_by_text("Academic Functions").click()

            page.wait_for_timeout(1000)

            page.get_by_text("University Exam/Result").click()

            page.wait_for_timeout(1000)

            page.get_by_text("Autonomous Student Result").click()

            log("Reached result page.")

            page.wait_for_timeout(3000)

            # Read page content
            page_text = page.inner_text("body")

            # Result Found
            if TARGET_RESULT in page_text:

                log(f"{TARGET_RESULT} RESULT FOUND!")

                # Screenshot capture
                page.screenshot(path="result_found.png")

                telegram_sent = send_telegram_message(
                    f"{TARGET_RESULT} result is now available on BIT Mesra ERP!"
                )

                if telegram_sent:
                    log("Telegram notification sent successfully.")
                else:
                    log("Telegram notification failed.")

                browser.close()

                return True

            else:
                log(f"{TARGET_RESULT} not available yet.")

        except Exception as e:

            log(f"Error occurred: {e}")

            log("Will retry after 5 minutes...")

        finally:
            browser.close()

        return False


# =========================
# Monitoring Loop
# =========================

log("BIT Mesra ERP Result Monitor Started.")

while True:

    found = check_result()

    if found:

        log("Monitoring stopped.")

        # Infinite alert loop
        for _ in range(5):
            playsound(SOUND_FILE)
            time.sleep(1)

        log("Program terminated after successful detection.")
        break

    log(f"Waiting {CHECK_INTERVAL // 60} minutes before next check...")

    time.sleep(CHECK_INTERVAL)
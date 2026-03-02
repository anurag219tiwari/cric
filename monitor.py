import asyncio
import requests
import os
import time
from playwright.async_api import async_playwright

URL = "https://in.bookmyshow.com/sports/icc-men-s-t20-world-cup-2026-semi-final-2/ET00474271"
NTFY_TOPIC = os.environ.get("NTFY_TOPIC")

async def check_booking_open():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36")
        await page.goto(URL, wait_until="networkidle", timeout=30000)
        try:
            await page.wait_for_selector("text=Book Now", timeout=8000)
            await browser.close()
            return True
        except:
            await browser.close()
            return False

def send_notification():
    requests.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data="🏏 ICC T20 WC Semi-Final 2 tickets OPEN! Book now!",
        headers={"Title": "Book Now!", "Priority": "urgent", "Tags": "cricket"}
    )
    print("Notification sent!")

async def main():
    print("Starting monitor...")
    start = time.time()
    i = 0

    while time.time() - start < 540:  # run for exactly 9 minutes
        i += 1
        print(f"Check #{i}...")
        try:
            is_open = await check_booking_open()
            if is_open:
                send_notification()
                return
            else:
                print("Still Coming Soon.")
        except Exception as e:
            print(f"Error: {e}")

    print("9 minutes done. GitHub will re-trigger.")

asyncio.run(main())

# -*- coding: utf-8 -*-
"""
測試 Selenium 自動化瀏覽器
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def test_browser():
    """Test browser automation"""
    print("Testing Selenium browser automation...")

    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        # Start Chrome
        driver = webdriver.Chrome(options=chrome_options)
        print("Chrome browser started successfully")

        # Test visiting website
        driver.get("https://app.koyeb.com")
        print(f"Successfully visited Koyeb, title: {driver.title}")

        # Wait a bit
        time.sleep(2)

        # Close browser
        driver.quit()
        print("Test completed")

        return True
    except Exception as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    test_browser()

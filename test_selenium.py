# -*- coding: utf-8 -*-
"""
測試 Selenium 自動化瀏覽器
使用 undetected-chromedriver 避免被 Google 檢測
"""

import undetected_chromedriver as uc
import time

def test_browser():
    """Test browser automation"""
    print("Testing Selenium browser automation with undetected-chromedriver...")

    try:
        # 使用 undetected-chromedriver
        options = uc.ChromeOptions()
        options.add_argument("--headless")  # 如需看到瀏覽器，移除此行
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # 創建 driver
        driver = uc.Chrome(options=options, version_main=None)  # 自動檢測 Chrome 版本

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

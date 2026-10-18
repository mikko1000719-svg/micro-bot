# -*- coding: utf-8 -*-
"""
自動化部署到 Koyeb
使用 Selenium 自動化網頁操作
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def load_env_file():
    """Load environment variables from .env file"""
    env_vars = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    except FileNotFoundError:
        print("Warning: .env file not found")
    return env_vars

def deploy_to_koyeb():
    """Automate deployment to Koyeb using Selenium"""
    print("Starting automated deployment to Koyeb...")

    # Chrome options - NOT headless so you can see the browser
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--headless")  # Commented out to see browser

    try:
        # Start Chrome
        driver = webdriver.Chrome(options=chrome_options)
        print("Chrome browser started - you should see a browser window")

        # Go to Koyeb
        driver.get("https://app.koyeb.com")
        print("Navigated to Koyeb")
        time.sleep(5)

        # Check if logged in
        page_title = driver.title
        print(f"Page title: {page_title}")

        # Load environment variables
        env_vars = load_env_file()
        print(f"Loaded {len(env_vars)} environment variables:")
        for key, value in env_vars.items():
            print(f"  {key}: {value[:20]}...")

        # Keep browser open for manual interaction
        print("\n=== Browser is now open for manual interaction ===")
        print("Please:")
        print("1. Login to Koyeb if not logged in")
        print("2. Configure environment variables")
        print("3. Deploy the service")
        print("4. Press Enter in this terminal to close the browser")
        
        input("\nPress Enter to close browser...")
        driver.quit()
        print("Browser closed")

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    deploy_to_koyeb()

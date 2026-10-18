# -*- coding: utf-8 -*-
"""
自動點擊腳本 - 自動點擊屏幕上的按鈕
使用 pyautogui 自動點擊指定位置
"""

import pyautogui
import time
import keyboard

def auto_click_button(x, y, clicks=1, interval=0.5):
    """
    自動點擊指定位置
    
    Args:
        x: X 坐標
        y: Y 坐標
        clicks: 點擊次數
        interval: 點擊間隔（秒）
    """
    print(f"🎯 準備點擊位置: ({x}, {y})")
    print(f"⏱️  3秒後開始點擊... 按 ESC 取消")
    
    # 倒數 3 秒
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    # 檢查是否按下 ESC 取消
    if keyboard.is_pressed('esc'):
        print("❌ 已取消")
        return
    
    # 執行點擊
    print("✅ 開始點擊...")
    for i in range(clicks):
        pyautogui.click(x, y)
        print(f"   點擊 {i+1}/{clicks}")
        if i < clicks - 1:
            time.sleep(interval)
    
    print("✅ 完成！")

def get_mouse_position():
    """獲取當前滑鼠位置"""
    print("🖱️  移動滑鼠到要點擊的位置，按空格鍵獲取坐標")
    print("   按 ESC 退出")
    
    while True:
        if keyboard.is_pressed('space'):
            x, y = pyautogui.position()
            print(f"📍 當前位置: X={x}, Y={y}")
            return x, y
        elif keyboard.is_pressed('esc'):
            print("❌ 已退出")
            return None, None
        time.sleep(0.1)

def continuous_click(x, y, interval=1):
    """
    持續點擊（用於需要重複點擊的情況）
    
    Args:
        x: X 坐標
        y: Y 坐標
        interval: 點擊間隔（秒）
    """
    print(f"🔄 持續點擊模式: ({x}, {y})")
    print(f"⏱️  每 {interval} 秒點擊一次")
    print("   按 ESC 停止")
    
    try:
        while True:
            pyautogui.click(x, y)
            print(f"✅ 點擊於 {time.strftime('%H:%M:%S')}")
            time.sleep(interval)
            
            if keyboard.is_pressed('esc'):
                print("❌ 已停止")
                break
    except KeyboardInterrupt:
        print("❌ 已停止")

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 自動點擊腳本")
    print("=" * 50)
    print()
    print("選擇模式:")
    print("1. 獲取滑鼠位置")
    print("2. 單次點擊")
    print("3. 多次點擊")
    print("4. 持續點擊")
    print()
    
    choice = input("請選擇 (1-4): ").strip()
    
    if choice == "1":
        x, y = get_mouse_position()
        if x is not None:
            print(f"\n使用坐標: ({x}, {y})")
    
    elif choice == "2":
        try:
            x = int(input("X 坐標: "))
            y = int(input("Y 坐標: "))
            auto_click_button(x, y, clicks=1)
        except ValueError:
            print("❌ 請輸入有效的數字")
    
    elif choice == "3":
        try:
            x = int(input("X 坐標: "))
            y = int(input("Y 坐標: "))
            clicks = int(input("點擊次數: "))
            interval = float(input("間隔(秒): "))
            auto_click_button(x, y, clicks=clicks, interval=interval)
        except ValueError:
            print("❌ 請輸入有效的數字")
    
    elif choice == "4":
        try:
            x = int(input("X 坐標: "))
            y = int(input("Y 坐標: "))
            interval = float(input("間隔(秒): "))
            continuous_click(x, y, interval=interval)
        except ValueError:
            print("❌ 請輸入有效的數字")
    
    else:
        print("❌ 無效選擇")

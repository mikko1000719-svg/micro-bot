# -*- coding: utf-8 -*-
"""
屏幕錄影腳本 - 使用 mss 庫錄製屏幕
"""

import mss
import time
import numpy as np
import cv2
import threading
import keyboard

class ScreenRecorder:
    def __init__(self, output_file="recording.mp4", fps=30):
        self.output_file = output_file
        self.fps = fps
        self.recording = False
        self.thread = None

    def start_recording(self, monitor=1):
        """開始錄影"""
        if self.recording:
            print("⚠️  已經在錄影中")
            return

        self.recording = True
        self.thread = threading.Thread(target=self._record, args=(monitor,))
        self.thread.start()
        print(f"🎥 開始錄影到 {self.output_file}")
        print("   按 ESC 停止錄影")

    def _record(self, monitor):
        """錄影線程"""
        with mss.mss() as sct:
            # 獲取屏幕尺寸
            monitor_info = sct.monitors[monitor]
            width = monitor_info["width"]
            height = monitor_info["height"]

            # 設置視頻編碼器
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(self.output_file, fourcc, self.fps, (width, height))

            print(f"📺 錄影區域: {width}x{height}")

            while self.recording:
                # 截圖
                screenshot = sct.grab(monitor_info)
                # 轉換為 numpy array
                img = np.array(screenshot)
                # 轉換顏色格式 (BGRA to BGR)
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                # 寫入視頻
                out.write(img)

                # 檢查是否按下 ESC
                if keyboard.is_pressed('esc'):
                    print("⏹️  檢測到 ESC，停止錄影")
                    break

                # 控制幀率
                time.sleep(1 / self.fps)

            out.release()
            print(f"✅ 錄影已保存到 {self.output_file}")

    def stop_recording(self):
        """停止錄影"""
        if not self.recording:
            print("⚠️  沒有在錄影")
            return

        self.recording = False
        if self.thread:
            self.thread.join()
        print("⏹️  錄影已停止")

if __name__ == "__main__":
    print("=" * 50)
    print("🎥 屏幕錄影工具")
    print("=" * 50)
    print()

    recorder = ScreenRecorder(output_file="screen_recording.mp4", fps=30)

    print("選擇操作:")
    print("1. 開始錄影")
    print("2. 開始錄影（指定監視器）")
    print()

    choice = input("請選擇 (1-2): ").strip()

    if choice == "1":
        recorder.start_recording(monitor=1)
        input("按 Enter 停止錄影...")
        recorder.stop_recording()

    elif choice == "2":
        monitor = int(input("監視器編號 (默認 1): ") or "1")
        recorder.start_recording(monitor=monitor)
        input("按 Enter 停止錄影...")
        recorder.stop_recording()

    else:
        print("❌ 無效選擇")

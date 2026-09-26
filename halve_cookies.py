def halve_cookies_file(input_filename='cookies.txt', output_filename='cookies_halved.txt'):
    comments = []
    cookie_lines = []
    
    try:
        # 1. 讀取原始檔案並將註解與 Cookie 資料分離
        with open(input_filename, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('#'):
                    comments.append(line)
                elif line.strip():  # 排除空行
                    cookie_lines.append(line)
        
        # 2. 計算並保留前一半的 Cookie 項目
        half_count = len(cookie_lines) // 2
        halved_cookies = cookie_lines[:half_count]
        
        # 3. 寫入新的減半後檔案
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.writelines(comments)
            f.writelines(halved_cookies)
            
        print(f"【處理成功】")
        print(f"原始 Cookie 總數：{len(cookie_lines)} 行")
        print(f"減半後 Cookie 數：{len(halved_cookies)} 行")
        print(f"新檔案已儲存至：{output_filename}")
        
    except FileNotFoundError:
        print(f"【錯誤】找不到檔案 {input_filename}，請確認檔案是否與此程式放在同一資料夾中。")

if __name__ == '__main__':
    # 執行函數（可依需求修改檔名）
    halve_cookies_file('cookies.txt', 'cookies_halved.txt')

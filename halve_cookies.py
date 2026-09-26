# -*- coding: utf-8 -*-
def halve_cookies_file(input_filename='cookies.txt', output_filename='cookies_halved.txt'):
    comments = []
    cookie_lines = []

    try:
        # 1. Read original file and separate comments from cookie data
        with open(input_filename, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('#'):
                    comments.append(line)
                elif line.strip():  # Exclude empty lines
                    cookie_lines.append(line)

        # 2. Calculate and keep first half of cookie items
        half_count = len(cookie_lines) // 2
        halved_cookies = cookie_lines[:half_count]

        # 3. Write new halved file
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.writelines(comments)
            f.writelines(halved_cookies)

        print(f"[SUCCESS] Processing complete")
        print(f"Original cookie total: {len(cookie_lines)} lines")
        print(f"Halved cookie count: {len(halved_cookies)} lines")
        print(f"New file saved to: {output_filename}")

    except FileNotFoundError:
        print(f"[ERROR] File {input_filename} not found, please confirm file is in the same folder as this program.")

if __name__ == '__main__':
    # Execute function (can modify filename as needed)
    halve_cookies_file('cookies.txt', 'cookies_halved.txt')

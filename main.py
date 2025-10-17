import os
import re

class FileStructure:
    def __init__(self):
        self.root_folder = "./"
        self.path_stack = []  # 儲存目前層級的資料夾名稱

    def parse_line(self, line: str):
        """
        解析一行結構字串，回傳 (層級, 名稱, 是否為資料夾)
        """
        # 移除註解部分 (# 後面的都忽略)
        line = line.split('#')[0].rstrip()

        if not line.strip():
            return None  # 跳過空行或純註解

        # 統一符號：把 '──' 或 '-' 全部簡化，方便正則處理
        line = line.replace('──', '─')

        # 計算層級（根據 │、├、└、| 出現次數）
        level = len(re.findall(r'[│├└|]', line))

        # 移除開頭的結構符號與多餘空白
        name = re.sub(r'^[\s│├└─|]+', '', line).strip()

        # 移除尾端的斜線（代表資料夾）
        name = name.rstrip('/\\')

        # 判斷是否為資料夾（如果沒有副檔名，視為資料夾）
        is_folder = '.' not in name

        return level, name, is_folder

    def create_from_lines(self, lines):
        # root_flag = True
        for raw_line in lines:
        #     if root_flag:
        #         root_flag = False
        #         self.root_folder += raw_line

            parsed = self.parse_line(raw_line)
            if not parsed:
                continue

            level, name, is_folder = parsed

            # 修正層級堆疊
            if level < len(self.path_stack):
                self.path_stack = self.path_stack[:level]
            elif level > len(self.path_stack):
                while len(self.path_stack) < level:
                    self.path_stack.append("")

            self.path_stack = self.path_stack[:level] + [name]
            path = os.path.join(self.root_folder, *self.path_stack)

            # 建立資料夾或檔案
            if is_folder:
                os.makedirs(path, exist_ok=True)
                print(f"[Created] Folder: {path}")
            else:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                open(path, 'w', encoding='utf-8').close()
                print(f"[Created] File: {path}")

    def input_structure(self):
        print("📁 Paste your folder structure (empty line to finish):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        return lines


if __name__ == '__main__':
    fs = FileStructure()
    lines = fs.input_structure()
    fs.create_from_lines(lines)
    print("\n✅ Folder structure created successfully!")

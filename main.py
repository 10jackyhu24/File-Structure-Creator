import os
import re

class FileStructure:
    def __init__(self):
        self.root_folder = "./"
        self.path_stack = []  # 儲存當前層級的資料夾名稱

    def parse_line(self, line: str):
        """
        分析一行樹狀結構文字，回傳 (層級, 名稱, 是否為資料夾)
        """
        line = line.rstrip()

        # 統計層級：數 '│' 或 前導空白群組
        level = line.count('│')

        # 清除開頭的樹狀符號 (│ ├ └ ─ 和空白)
        name = re.sub(r'^[\s│├└─]+', '', line).strip()

        # 判斷是否為資料夾
        is_folder = '.' not in name
        return level, name, is_folder

    def create_from_lines(self, lines):
        root_flag = True
        for line in lines:
            if root_flag:
                self.root_folder = line
                root_flag = False
                continue

            if not line.strip():
                continue

            level, name, is_folder = self.parse_line(line)

            # 若層級比堆疊小 → 回到上層
            if level < len(self.path_stack):
                self.path_stack = self.path_stack[:level]
            elif level > len(self.path_stack):
                # 若層級比當前堆疊多 → 自動補齊
                while len(self.path_stack) < level:
                    self.path_stack.append("")

            # 建立目前層級名稱
            self.path_stack = self.path_stack[:level] + [name]

            # 組合實際路徑
            path = os.path.join(self.root_folder, *self.path_stack)

            if is_folder:
                os.makedirs(path, exist_ok=True)
                print(f"[Created] Folder: {path}")
            else:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                open(path, 'w', encoding='utf-8').close()
                print(f"[Created] File: {path}")

    def input_structure(self):
        print("Please paste the folder structure (end with blank line):")
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
    print("\nFinished !")

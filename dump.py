import os
from pathlib import Path

# ========= CONFIG =========
ROOT_DIR = Path(".")  # текущая папка проекта
OUTPUT_FILE = "project_dump.txt"

# что игнорируем
IGNORE_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    "__pycache__",
    "node_modules",
    ".venv",
    "dist",
    "build",
    ".next",
    ".cache",
    "coverage",
}

IGNORE_FILES = {
    ".DS_Store",
    "project_dump.txt",
}

# расширения, которые НЕ трогаем (бинарь)
IGNORE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg",
    ".ico", ".pdf", ".zip", ".tar", ".gz",
    ".mp4", ".mp3", ".wav",
    ".woff", ".woff2", ".ttf", ".eot",
}

# ========= LOGIC =========

def is_ignored(path: Path) -> bool:
    if any(part in IGNORE_DIRS for part in path.parts):
        return True
    if path.name in IGNORE_FILES:
        return True
    if path.suffix.lower() in IGNORE_EXTENSIONS:
        return True
    return False


def dump_project():
    files = []

    for path in ROOT_DIR.rglob("*"):
        if path.is_file() and not is_ignored(path):
            files.append(path)

    files.sort()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for file_path in files:
            relative_path = file_path.relative_to(ROOT_DIR)

            try:
                content = file_path.read_text(encoding="utf-8")
            except Exception:
                # бинарники или кривые файлы
                content = "[[BINARY OR UNREADABLE FILE]]"

            out.write(f"\n\n{'='*80}\n")
            out.write(f"FILE: {relative_path}\n")
            out.write(f"{'='*80}\n\n")
            out.write(content)

    print(f"\n✅ Dump saved to: {OUTPUT_FILE}")
    print(f"📦 Files processed: {len(files)}")


if __name__ == "__main__":
    dump_project()
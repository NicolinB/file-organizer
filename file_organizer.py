#!/usr/bin/env python3
"""
file_organizer.py
Organizes files in a folder into subdirectories by extension.
Author: Barbaros Nicolin
"""

import os
import shutil
from datetime import datetime

CATEGORIES = {
    "Images":        [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".ico", ".webp"],
    "Documents":     [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".md"],
    "Spreadsheets":  [".xls", ".xlsx", ".csv", ".ods"],
    "Presentations": [".ppt", ".pptx", ".odp"],
    "Videos":        [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
    "Audio":         [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Archives":      [".zip", ".rar", ".tar", ".gz", ".7z", ".bz2"],
    "Code":          [".py", ".c", ".cpp", ".h", ".js", ".html", ".css", ".java"],
}


def get_category(ext):
    ext = ext.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Other"


def organize(folder_path, dry_run=False):
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory.")
        return

    files = [f for f in os.listdir(folder_path)
             if os.path.isfile(os.path.join(folder_path, f))]

    if not files:
        print("No files found.")
        return

    moved = 0
    skipped = 0
    mode = "[DRY RUN] " if dry_run else ""

    print(f"\n{mode}Organizing: {folder_path}")
    print("-" * 55)

    for filename in sorted(files):
        _, ext = os.path.splitext(filename)
        if not ext:
            skipped += 1
            continue

        category  = get_category(ext)
        src       = os.path.join(folder_path, filename)
        dest_dir  = os.path.join(folder_path, category)
        dest      = os.path.join(dest_dir, filename)

        # Avoid overwriting files with the same name
        if os.path.exists(dest):
            name, extension = os.path.splitext(filename)
            ts   = datetime.now().strftime("%H%M%S")
            dest = os.path.join(dest_dir, f"{name}_{ts}{extension}")

        print(f"  {filename:<40} ->  {category}/")

        if not dry_run:
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(src, dest)

        moved += 1

    print("-" * 55)
    action = "Would move" if dry_run else "Moved"
    print(f"{action}: {moved} file(s), skipped (no extension): {skipped}")


def main():
    print("=== File Organizer ===")
    folder = input("Folder path (or '.' for current directory): ").strip()
    if folder == ".":
        folder = os.getcwd()

    print("\n  1. Organize (move files)")
    print("  2. Preview only (no changes)")
    choice = input("Choice [1/2]: ").strip()

    organize(folder, dry_run=(choice == "2"))


if __name__ == "__main__":
    main()

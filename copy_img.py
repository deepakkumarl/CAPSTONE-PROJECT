import shutil
from pathlib import Path

src = Path(r"C:\Users\Administrator\.gemini\antigravity\brain\30d8dd06-6d7b-4f69-b92a-295bad37e68b\architecture_diagram_1789708175209.jpg")
dst = Path(r"d:\documents\PRO-1\bmw-capstone-usecase\docs\architecture.png")

if src.exists():
    shutil.copy(src, dst)
    print("Copied image to docs/architecture.png")
else:
    print("Source image not found.")

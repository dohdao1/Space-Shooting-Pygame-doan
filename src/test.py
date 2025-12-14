# test_item.py
import pygame
import os
import sys

# Khởi tạo pygame
pygame.init()

# Test resource_path
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Test các file
files = [
    "assets/images/items/double.png",
    "assets/images/items/triple.png",
    "assets/images/items/quad.png",
    "assets/images/items/six.png",
    "assets/images/items/shield.png",
    "assets/images/items/life.png",
    "assets/images/items/bomb.png",
]

print("Testing asset files:")
for f in files:
    path = resource_path(f)
    exists = os.path.exists(path)
    print(f"{'✅' if exists else '❌'} {f}: {exists}")
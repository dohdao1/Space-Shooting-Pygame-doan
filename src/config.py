import os, sys

#cấu hình của game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Màu sắc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game settings
PLAYER_START_LIVES = 3
PLAYER_MAX_HEALTH = 100

BASE_DROP_RATE = 0.3  # tỉ lệ rơi item cơ bản
DIFFICULTY_BONUS = 0.01  # Mỗi độ khó +1%
MAX_DROP_RATE = 0.6  # Tối đa 60%

# dùng cho khi chuyển file
def resource_path(relative_path):
    try:
        # PyInstaller tạo thư mục tạm và lưu đường dẫn trong _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    if os.name == 'nt':  # Windows
        relative_path = relative_path.replace('/', '\\')
    
    return os.path.join(base_path, relative_path)
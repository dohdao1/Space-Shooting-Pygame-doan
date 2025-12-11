import pygame
from .bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=6):
        super().__init__()
        self.image = pygame.image.load("../assets/images/player/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60)) 
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = speed

        # bullet system
        self.last_shot = 0
        
        # --- GÓI ĐẠN HIỆN TẠI ---
        # bạn có thể thay đổi gói này khi chơi, khi ăn item,...
        self.bullet_package = {
            "bullet_class": Bullet,   # loại bullet
            "fire_rate": 200,         # thời gian giữa mỗi lần bắn (ms)
            "burst": 1,               # số đạn mỗi lần
            "spread": 0               # độ lệch trái/phải (0 = bắn thẳng)
        }

    # ========= DI CHUYỂN THEO CHUỘT =========
    def move_mouse(self, screen_width, screen_height=720):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.rect.center = (mouse_x, mouse_y)

        # giới hạn biên
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    # ========== TỰ ĐỘNG BẮN THEO GÓI ==========   
    def auto_shoot(self, bullets_group):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_shot >= self.bullet_package["fire_rate"]:
            bullet_class = self.bullet_package["bullet_class"]
            burst = self.bullet_package["burst"]
            spread = self.bullet_package["spread"]

            # Nếu chỉ bắn 1 viên
            if burst == 1:
                bullets_group.add(bullet_class(self.rect.centerx, self.rect.top))

            else:
                # bắn N viên lan sang 2 bên
                offset_start = -(burst // 2) * spread
                for i in range(burst):
                    offset = offset_start + i * spread
                    b = bullet_class(self.rect.centerx + offset, self.rect.top)
                    bullets_group.add(b)

            self.last_shot = current_time

    # ========= UPDATE =========
    def update(self, keys, bullets_group, screen_width, screen_height=720):
        self.move_mouse(screen_width, screen_height)
        self.auto_shoot(bullets_group)

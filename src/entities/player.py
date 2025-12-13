import pygame, math
from .bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=6, skin_manager=None):
        super().__init__()
        # Nhận skin_manager từ bên ngoài
        self.skin_manager = skin_manager
        
        # Lấy skin đang được chọn
        if self.skin_manager:
            skin_name = self.skin_manager.selected_skin
            skin_path = self.skin_manager.get_skin_path()  # Dùng method mới
        else:
            skin_name = "default"
            skin_path = "assets/images/player/player.png"

        self.image = pygame.image.load(skin_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (72, 72))
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = speed
        self.has_shield = False
        self.shield_end_time = 0
        self.shield_image = pygame.image.load("assets/images/effects/shield.png").convert_alpha()
        self.shield_image = pygame.transform.scale(self.shield_image, (90, 90))
        self.activate_shield(6000)   # 6 giây khi vào trận
        self.shield_broken_at = None


        # bullet system
        self.last_shot = 0
        
        # --- GÓI ĐẠN HIỆN TẠI ---
        # bạn có thể thay đổi gói này khi chơi, khi ăn item,...
        self.bullet_package = {
            "bullet_class": Bullet,   # loại bullet
            "fire_rate": 300,         # thời gian giữa mỗi lần bắn (ms)
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

            base_angle = 270 

            # Nếu chỉ bắn 1 viên
            if burst == 1:
                bullets_group.add(bullet_class(self.rect.centerx, self.rect.top, base_angle))

            else:
                if burst == 2 and spread == 0:
                    offset = 14
                    bullets_group.add(
                        bullet_class(self.rect.centerx - offset, self.rect.top, base_angle)
                    )
                    bullets_group.add(  
                        bullet_class(self.rect.centerx + offset, self.rect.top, base_angle)
                    )
                else:
                    angles = [
                        base_angle - spread + i * (2 * spread / (burst - 1))
                        for i in range(burst)   
                    ]
                    for angle in angles:
                        bullets_group.add(
                            bullet_class(self.rect.centerx, self.rect.top, angle)
                        )

            if hasattr(self, 'game_ref') and hasattr(self.game_ref.game, 'audio_manager'):
            # Tính volume scale dựa trên loại đạn
                volume_scale = 0.3

                if burst == 1:
                    volume_scale = 0.25

                else:
                    volume_scale = min(0.5, 0.3 + (burst * 0.05))  # đạn nhiều thì to hơn
            
                self.game_ref.game.audio_manager.play_sound("bullet", volume_scale=volume_scale)

            self.last_shot = current_time

    # ========= UPDATE =========
    def update(self, keys, bullets_group, screen_width, screen_height=720):
        self.move_mouse(screen_width, screen_height)
        self.auto_shoot(bullets_group)
        # --- Shield timer ---
        if self.has_shield and pygame.time.get_ticks() > self.shield_end_time:
                self.break_shield()

    def draw_shield(self, screen):
        if self.has_shield:
            shield_rect = self.shield_image.get_rect(center=self.rect.center)
            screen.blit(self.shield_image, shield_rect)

    # ===== KÍCH HOẠT KHIÊN =====
    def activate_shield(self, duration=6000):
        self.has_shield = True
        self.shield_active = True
        self.shield_end_time = pygame.time.get_ticks() + duration
    def break_shield(self):
        self.has_shield = False
        self.shield_active = False
        self.shield_end_time = 0
        self.shield_broken_at = pygame.time.get_ticks()

    def take_damage(self, amount):
    
        # nếu có khiên thì không trừ máu
        if getattr(self, "shield_active", False):
            self.break_shield()
            return

        # không có khiên → trừ mạng
        if hasattr(self, "game_ref"):
            self.game_ref.lives -= 1
import pygame
from .bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, shoot_cooldown=200):
        super().__init__()

        from managers.skinManager import SkinManager
        skin = SkinManager()

        # load skin người chơi đã chọn
        selected_path = skin.skins[skin.selected_skin]["path"]
        # Load ảnh
        self.original_image = pygame.image.load(selected_path).convert_alpha()

        # --- SCALE PLAYER: chỉnh kích thước theo chiều rộng cố định ---
        TARGET_HEIGHT = 100  # đặt kích thước chuẩn (tùy bạn: 70–120 rất hợp lý)

        original_w = self.original_image.get_width()
        original_h = self.original_image.get_height()

        scale_factor = TARGET_HEIGHT / original_h
        new_h = TARGET_HEIGHT
        new_w = int(original_w * scale_factor)
        self.image = pygame.transform.scale(self.original_image, (new_w, new_h))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

        # --- SHOOT ---
        self.shoot_cooldown = shoot_cooldown
        self.last_shot = 0

        # --- ANIMATION SYSTEM (để khỏi bị lỗi animate) ---
        self.anim_frames = [self.image]   # hiện tại chưa có animation -> dùng 1 frame
        self.anim_index = 0
        self.anim_speed = 0.25

    # animate cơ bản
    def animate(self):
        self.anim_index += self.anim_speed
        if self.anim_index >= len(self.anim_frames):
            self.anim_index = 0
        self.image = self.anim_frames[int(self.anim_index)]

    # di chuyển + giới hạn màn hình
    def move(self, keys, screen_width, screen_height=720):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        # giới hạn cạnh trái/phải
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

        # giới hạn cạnh trên/dưới
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    # bắn
    def shoot(self, bullets_group):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.shoot_cooldown:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullets_group.add(bullet)
            self.last_shot = current_time

    # update tổng
    def update(self, keys, bullets_group, screen_width):
        self.move(keys, screen_width)
        self.animate()

        # bắn bằng SPACE
        if keys[pygame.K_SPACE]:
            self.shoot(bullets_group)

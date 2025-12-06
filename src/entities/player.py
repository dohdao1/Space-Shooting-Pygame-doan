#tổng quan người chơi, di chuyển bắn đạn(việc di chuyển của viên đạn bắn ra là do bullet xử lý)
import pygame
from .bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=5, shoot_cooldown=300):
        super().__init__()
        self.image = pygame.image.load("assets/images/player/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60)) 
        self.rect = self.image.get_rect(center=(x, y))

        # animation
        self.anim_frames = [self.image]  # bạn có thể thêm nhiều frame
        self.anim_index = 0
        self.anim_speed = 0.15

        # movement
        self.speed = speed

        # shooting
        self.can_shoot = True
        self.shoot_cooldown = shoot_cooldown
        self.last_shot = 0

        # health
        self.max_health = 100
        self.health = 100

    def animate(self):
        self.anim_index += self.anim_speed
        if self.anim_index >= len(self.anim_frames):
            self.anim_index = 0
        self.image = self.anim_frames[int(self.anim_index)]

    def move(self, keys, screen_width):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        # giới hạn
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    def shoot(self, bullets_group):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.shoot_cooldown:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullets_group.add(bullet)
            self.last_shot = current_time

    def update(self, keys, bullets_group, screen_width):
        self.move(keys, screen_width)
        self.animate()

        # bắn bằng phím SPACE
        if keys[pygame.K_SPACE]:
            self.shoot(bullets_group)

# đạn do người chơi bắn ra
import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=270, speed=12):   # 270° = bắn lên trên
        super().__init__()
        self.image = pygame.Surface((4, 12))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = speed
        self.damage = 1

        # Convert độ sang radian
        rad = math.radians(angle)

        # Tính vector bay
        self.vx = math.cos(rad) * speed
        self.vy = math.sin(rad) * speed

    def update(self, dt):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.bottom < 0 or self.rect.top > 800:
            self.kill()

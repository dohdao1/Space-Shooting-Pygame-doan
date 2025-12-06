# đạn do người chơi bắn ra
import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=10):
        super().__init__()
        self.image = pygame.Surface((4, 12))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


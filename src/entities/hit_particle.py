import pygame
import random

class HitParticle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        size = random.randint(3, 6)
        self.image = pygame.Surface((size, size))
        self.image.fill((255, 200, 50))
        self.rect = self.image.get_rect(center=(x, y))

        self.vel_x = random.uniform(-2, 2)
        self.vel_y = random.uniform(-2, 2)
        self.life = random.randint(10, 20)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.life -= 1

        if self.life <= 0:
            self.kill()

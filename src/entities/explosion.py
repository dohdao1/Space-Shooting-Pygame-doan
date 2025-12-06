import pygame
import random

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # nếu có sprite sheet — bạn thay bằng load ảnh thật
        self.frames = []
        for size in [20, 30, 40, 60]:
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, random.randint(100,180), 0), (size//2, size//2), size//2)
            self.frames.append(surf)

        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.frame_timer = 0

    def update(self):
        self.frame_timer += 1
        if self.frame_timer % 3 == 0:  # tốc độ animation
            self.index += 1
            if self.index >= len(self.frames):
                self.kill()
            else:
                old_center = self.rect.center
                self.image = self.frames[self.index]
                self.rect = self.image.get_rect(center=old_center)

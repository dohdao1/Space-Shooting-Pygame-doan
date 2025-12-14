import pygame
import os
from config import resource_path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_DIR = os.path.join(BASE_DIR, "assets", "images", "asteroid")

class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, speed=150):
        super().__init__()
        # try load image
        bullet_img_path = os.path.join("assets", "images", "asteroid", "bullet-boss.png")
        # chuẩn hóa
        bullet_img_path = os.path.normpath(bullet_img_path)
        try:
            self.image = pygame.image.load(resource_path(bullet_img_path)).convert_alpha()
            print("load dc rồi nha")
        except Exception:
            self.image = pygame.Surface((8,16), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255,80,80), (0,0,8,16))
        self.rect = self.image.get_rect(center=(x,y))

       
        self.vx = dx
        self.vy = dy
        self.speed = speed

        
        self.damage = 20

        
        try:
            self.mask = pygame.mask.from_surface(self.image)
        except Exception:
            self.mask = None

    def update(self, dt):
       
        self.rect.x += self.vx
        self.rect.y += self.vy
        

        if self.rect.top > 700 or self.rect.bottom < -50 or self.rect.left < -100 or self.rect.right > 900:
            self.kill()

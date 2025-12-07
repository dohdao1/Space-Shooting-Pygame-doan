import pygame
import random
from enum import Enum
import os

# --- ENUM loại thiên thạch ---
class AsteroidType(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

ASTEROID_STATS = {
    AsteroidType.SMALL:  {"hp": 2, "speed": (28), "img": "assets/images/asteroid/small_asteroid.png"},
    AsteroidType.MEDIUM: {"hp": 3, "speed": (25), "img": "assets/images/asteroid/medium_asteroid.png"},
    AsteroidType.LARGE:  {"hp": 4, "speed": (22), "img": "assets/images/asteroid/large_asteroid.png"},
}

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, difficulty=1.0, screen_width=800):
        super().__init__()
        self.type = random.choice(list(AsteroidType))
        self.difficulty = difficulty
        self.screen_width = screen_width

        self.load_image()
        self.reset()

    # -----------------------------------------------------
    def load_image(self):
        stats = ASTEROID_STATS[self.type]
        self.original_img = pygame.image.load(stats["img"]).convert_alpha()

        scale_factor = random.uniform(0.4,0.6)
        w = int(self.original_img.get_width() * scale_factor)
        h = int(self.original_img.get_height() * scale_factor)

        self.original_img = pygame.transform.scale(self.original_img, (w, h))
        self.image = self.original_img.copy()
        self.rect = self.image.get_rect()

    # -----------------------------------------------------
    def reset(self):
        stats = ASTEROID_STATS[self.type]

        # HP
        self.hp = int(stats["hp"] + self.difficulty * 0.1)

        # Speed (px/s)
        speed = stats["speed"]
        self.speed = (speed) + (self.difficulty * 5)

        # Spawn random từ trên trời rơi xuống
        self.rect.x = random.randint(0, self.screen_width - self.rect.width)
        self.rect.y = random.randint(-200, -50)

        # Rotation
        self.rotation = random.randint(0, 360)
        self.rotation_speed = random.uniform(-0.5, 0.5)

        self.active = True

    # -----------------------------------------------------
    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.active = False
            self.kill()
            return "dead"
        return "hit"

    # -----------------------------------------------------
    def update(self, dt):
        # di chuyển theo speed px/s
        self.rect.y += self.speed * dt

        # ra ngoài màn hình → reset
        if self.rect.top > 600:
            self.reset()

        # xoay
        self.rotation += self.rotation_speed
        self.image = pygame.transform.rotate(self.original_img, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)

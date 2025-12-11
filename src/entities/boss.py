import pygame
import math
import os
from entities.boss_bullet import BossBullet

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_DIR = os.path.join(BASE_DIR, "assets", "images")

class Boss(pygame.sprite.Sprite):

    def __init__(self, x, y, image, boss_bullet_group, player, player_bullet_group):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x,y))
    

        # stats
        self.max_hp = 2000
        self.hp = self.max_hp

        # movement
        self.entry_speed = 80
        self.spawning = True
        self.entry_target_y = 120
        self.speed_x = 100
        self.dir = 1

        # references
        self.bullet_group = boss_bullet_group
        self.player = player
        self.player_bullet_group = player_bullet_group

        # shooting
        self.fire_timer = 0.0
        self.phase = 1

        # phase thresholds
        self.phase2_hp = int(self.max_hp * 0.66)
        self.phase3_hp = int(self.max_hp * 0.33)

        # internal params
        self.spiral_angle = 0.0

        # mask for collision
        try:
            self.mask = pygame.mask.from_surface(self.image)
        except Exception:
            self.mask = None

    def update(self, dt):
        if self.spawning:
            self.rect.y += self.entry_speed * dt
            if self.rect.y >= self.entry_target_y:
                self.spawning = False
            return

        #chọn phase
        if self.hp <= self.phase3_hp:
            self.phase = 3
        elif self.hp <= self.phase2_hp:
            self.phase = 2
        else:
            self.phase = 1

        
        self.rect.x += self.dir * self.speed_x * dt
        if self.rect.left < 20:
            self.rect.left = 20
            self.dir *= -1
        if self.rect.right > 780:
            self.rect.right = 780
            self.dir *= -1

        
        self.fire_timer += dt
        if self.phase == 1:
            if self.fire_timer >= 1.2:
                self.fire_timer = 0
                self._spread(5, speed=220)
        elif self.phase == 2:
            if self.fire_timer >= 0.9:
                self.fire_timer = 0
                self._spread(7, speed=240)
                self._aim_player(speed=260)
        else:  
            if self.fire_timer >= 0.35:
                self.fire_timer = 0
                
                self._spiral(count=6, speed=300)
                
                self._aim_player(speed=320)

        
        if self.player_bullet_group:
            hits = pygame.sprite.spritecollide(self, self.player_bullet_group, True, collided=pygame.sprite.collide_mask)
            for _ in hits:
                
                self.hp -= 20

  
    def _spread(self, count=5, speed=200):
        cx, cy = self.rect.centerx, self.rect.bottom
        half = (count-1)/2.0
        for i in range(count):
            offset = (i - half) * 8
            dx = offset
            dy = 6
            b = BossBullet(cx + offset*2, cy, dx, dy, speed)
            self.bullet_group.add(b)

    def _aim_player(self, speed=240):
        if not self.player:
            return
        px, py = self.player.rect.center
        bx, by = self.rect.center
        vx = px - bx
        vy = py - by
        dist = math.hypot(vx, vy)
        if dist == 0:
            return
        vx /= dist
        vy /= dist
        b = BossBullet(bx, by, vx * 5, vy * 5, speed)
        self.bullet_group.add(b)

    def _spiral(self, count=6, speed=280):
        cx, cy = self.rect.center
        angle_step = 360.0 / count
        for i in range(count):
            ang = math.radians(self.spiral_angle + i * angle_step)
            dx = math.cos(ang) * 4
            dy = math.sin(ang) * 4
            b = BossBullet(cx, cy, dx, dy, speed)
            self.bullet_group.add(b)
        self.spiral_angle += 18

    def is_dead(self):
        return self.hp <= 0

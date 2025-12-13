import pygame
import math

class Boss(pygame.sprite.Sprite):

    def __init__(
        self,
        x, y,
        image,
        boss_bullet_group,
        player,
        player_bullet_group
    ):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

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

        self.phase2_hp = int(self.max_hp * 0.66)
        self.phase3_hp = int(self.max_hp * 0.33)

        self.spiral_angle = 0.0

    # -----------------------------------------
    def update(self, dt):
        if self.spawning:
            self.rect.y += self.entry_speed * dt
            if self.rect.y >= self.entry_target_y:
                self.spawning = False
            return

        # phase
        if self.hp <= self.phase3_hp:
            self.phase = 3
        elif self.hp <= self.phase2_hp:
            self.phase = 2
        else:
            self.phase = 1

        # move left/right
        self.rect.x += self.dir * self.speed_x * dt
        if self.rect.left < 20 or self.rect.right > 780:
            self.dir *= -1

        # shoot
        self.fire_timer += dt
        if self.phase == 1 and self.fire_timer >= 1.2:
            self.fire_timer = 0
            self._spread(5, 220)

        elif self.phase == 2 and self.fire_timer >= 0.9:
            self.fire_timer = 0
            self._spread(7, 240)
            self._aim_player(260)

        elif self.phase == 3 and self.fire_timer >= 0.35:
            self.fire_timer = 0
            self._spiral(6, 300)
            self._aim_player(320)

    # -----------------------------------------
    def take_damage(self, dmg):
        self.hp -= dmg

    def is_dead(self):
        return self.hp <= 0

    # -----------------------------------------
    def _spread(self, count, speed):
        cx, cy = self.rect.centerx, self.rect.bottom
        half = (count - 1) / 2
        for i in range(count):
            dx = (i - half) * 8
            dy = 6
            from entities.boss_bullet import BossBullet
            self.bullet_group.add(
                BossBullet(cx, cy, dx, dy, speed)
            )

    def _aim_player(self, speed):
        if not self.player:
            return
        px, py = self.player.rect.center
        bx, by = self.rect.center
        vx, vy = px - bx, py - by
        dist = math.hypot(vx, vy)
        if dist == 0:
            return
        vx, vy = vx / dist, vy / dist

        from entities.boss_bullet import BossBullet
        self.bullet_group.add(
            BossBullet(bx, by, vx * 5, vy * 5, speed)
        )

    def _spiral(self, count, speed):
        cx, cy = self.rect.center
        angle_step = 360 / count
        from entities.boss_bullet import BossBullet

        for i in range(count):
            ang = math.radians(self.spiral_angle + i * angle_step)
            dx = math.cos(ang) * 4
            dy = math.sin(ang) * 4
            self.bullet_group.add(
                BossBullet(cx, cy, dx, dy, speed)
            )

        self.spiral_angle += 18

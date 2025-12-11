import pygame
import random
from entities.asteroid import Asteroid
from entities.hit_particle import HitParticle
from entities.explosion import Explosion

class AsteroidSpawner:
    def __init__(self, asteroid_group, screen_width):
        self.asteroids = asteroid_group
        self.screen_width = screen_width
        self.spawn_timer = 0
        self.spawn_interval = 800  # ms
        self.hit_particles = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.difficulty = 1.0
        self.difficulty_growth = 0.005  # mỗi giây tăng difficulty
        self.stop_spawn = False


    def update(self, dt):
        # tăng difficulty theo thời gian
        self.difficulty += self.difficulty_growth * dt

        # spawn asteroid
        self.spawn_timer += dt*1000  # dt tính giây, spawn_timer ms
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.try_spawn()
            # spawn interval biến thiên ngẫu nhiên
            self.spawn_interval = random.randint(1000, 1200)
        if self.stop_spawn:
            return

            

        # update tất cả asteroid
        self.asteroids.update(dt)
        self.hit_particles.update()
        self.explosions.update()

    # ---------------------------------------------------------
    def try_spawn(self):
        asteroid = Asteroid(difficulty=self.difficulty, screen_width=self.screen_width)
        self.asteroids.add(asteroid)

    # ---------------------------------------------------------
    def handle_bullet_collision(self, bullets, game_screen = None):
        hits = pygame.sprite.groupcollide(self.asteroids, bullets, False, True,collided=pygame.sprite.collide_mask)
        for asteroid, bullet_list in hits.items():
            for bullet in bullet_list:
                status=asteroid.take_damage(getattr(bullet, "dmg", 1))
                for _ in range(5):
                    particle = HitParticle(asteroid.rect.centerx, asteroid.rect.centery)
                    self.hit_particles.add(particle)
                if status == "dead":
                    if game_screen:
                        game_screen.score += 10     # này sau cập nhật cho từng thiên tạch cụ thể nha
                        game_screen.total_kills += 1    # Cập nhật điểm kill để lưu vào save
                    explosion = Explosion(asteroid.rect.centerx, asteroid.rect.centery)
                    self.explosions.add(explosion)

    # ---------------------------------------------------------
    def draw(self, screen):
        self.asteroids.draw(screen)
        self.hit_particles.draw(screen)
        self.explosions.draw(screen)
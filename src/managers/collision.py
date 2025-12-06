import pygame
import random

class CollisionSystem:
    def __init__(self):
        pass

    # -------------------------------------------------------------
    def bullet_vs_asteroid(self, bullets, asteroid_spawner):
        hit_particles = []
        death_particles = []
        dropped_items = []

        for bullet in bullets:
            hits = pygame.sprite.spritecollide(bullet, asteroid_spawner.asteroids, False)

            for asteroid in hits:
                result = asteroid.take_damage(bullet.damage)

                bullet.kill()  # đạn biến mất khi trúng

                if result == "hit":
                    # tạo particle trúng
                    hit_particles.append({
                        "pos": asteroid.rect.center,
                        "count": random.randint(3, 6)
                    })

                elif result == "dead":
                    # particle explosion
                    death_particles.append({
                        "pos": asteroid.rect.center,
                        "size": random.randint(20, 40)
                    })

                    if random.random() < 0.01:
                        dropped_items.append({
                            "type": random.choice(["atk+", "spd+", "regen"]),
                            "pos": asteroid.rect.center
                        })

        return hit_particles, death_particles, dropped_items

    # -------------------------------------------------------------
    def asteroid_vs_player(self, asteroid_spawner, player):
        for asteroid in asteroid_spawner.asteroids:
            if asteroid.rect.colliderect(player.rect):
                player.take_damage(10)  # hoặc damage theo loại asteroid
                asteroid.kill()
                return True

        return False

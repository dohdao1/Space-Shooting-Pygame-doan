import pygame
import random

class CollisionSystem:
    def __init__(self):
        # 
        pass
    def bullet_vs_asteroid(self, bullets, asteroid_spawner):
        hit_particles = []
        death_particles = []
        dropped_items = []

        for bullet in bullets:
            hits = pygame.sprite.spritecollide(bullet, asteroid_spawner.asteroids, False)
            for asteroid in hits:
                result = asteroid.take_damage(bullet.damage)
                bullet.kill()

                if result == "hit":
                    hit_particles.append({
                        "pos": asteroid.rect.center,
                        "count": random.randint(3, 6)
                    })  
                elif result == "dead":
                    # ⭐ Cộng điểm
                    asteroid_spawner.game_ref.score += 10

                    death_particles.append({ "pos": asteroid.rect.center})

                    if random.random() < min(0.5 + asteroid_spawner.difficulty * 0.02, 0.80):
                        drop_type = random.choice([
                            "double_bullet",
                            "triple_bullet",
                            "quad_bullet",
                            "six_bullet",
                            "shield",
                            "life",
                            "bomb"
                        ])

                        dropped_items.append({
                            "type": drop_type,
                            "pos": asteroid.rect.center
                        })

        return hit_particles, death_particles, dropped_items

    def asteroid_vs_player(self, asteroid_spawner, player):
        for asteroid in asteroid_spawner.asteroids:
            if asteroid.rect.colliderect(player.rect):
                #nếu có khiên
                if player.has_shield:
                    player.break_shield()
                    asteroid.kill()
                    return True
                # không có khiên
                
                player.take_damage(10)
                asteroid.kill()
                return True
        return False


   
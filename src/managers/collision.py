import pygame
import random

class CollisionSystem:
    def __init__(self):
        pass

    # ------------------------------------------------
    def bullet_vs_asteroid(self, bullets, asteroid_spawner):
        hit_particles = []
        death_particles = []
        dropped_items = []

        for bullet in bullets:
            hits = pygame.sprite.spritecollide(
                bullet,
                asteroid_spawner.asteroids,
                False,
                pygame.sprite.collide_mask
            )

            for asteroid in hits:
                bullet.kill()
                result = asteroid.take_damage(bullet.damage)

                if result == "hit":
                    hit_particles.append({
                        "pos": asteroid.rect.center,
                        "count": random.randint(3, 6)
                    })

                elif result == "dead":
                    asteroid_spawner.game_ref.score += 10
                    asteroid_spawner.game_ref.total_kills += 1

                    death_particles.append({
                        "pos": asteroid.rect.center
                    })

                    # DROP ITEM
                    if random.random() < 0.35:
                        dropped_items.append({
                            "type": random.choice([
                                "double_bullet",
                                "triple_bullet",
                                "quad_bullet",
                                "six_bullet",
                                "shield",
                                "life",
                                "bomb"
                            ]),
                            "pos": asteroid.rect.center
                        })
                    asteroid.last_hit_pos = asteroid.rect.center
                    asteroid.kill()

        return hit_particles, death_particles, dropped_items

    # ------------------------------------------------
    def asteroid_vs_player(self, asteroid_spawner, player):
        hits = pygame.sprite.spritecollide(
            player,
            asteroid_spawner.asteroids,
            True,
            pygame.sprite.collide_mask
        )

        if hits:
            if player.has_shield:
                player.break_shield()
            else:
                player.take_damage(10)
            return True

        return False

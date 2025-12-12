import pygame
class ItemManager:
    def __init__(self, player):
        self.player = player
        self.active_effects = {}

        self.effect_duration = {
            "double_bullet": 10000,
            "triple_bullet": 10000,
            "quad_bullet": 10000,
            "six_bullet": 10000,
            "shield": 10000
        }

    def apply_item(self, item_type):
        # MẠNG
        if item_type == "life":
            self.player.game_ref.lives += 1
            return

        # BOMB
        if item_type == "bomb":
            self.player.trigger_bomb = True
            return

        # SHIELD
        if item_type == "shield":
            self.player.activate_shield(6000)
            self.active_effects["shield"] = pygame.time.get_ticks()
            return

        # ⭐ ĐẠN
        bullet = self.player.bullet_package["bullet_class"]

        if item_type == "double_bullet":
            self.player.bullet_package = {
                "bullet_class": bullet,
                "fire_rate": 250,
                "burst": 2,
                "spread": 0
            }
        elif item_type == "triple_bullet":
            self.player.bullet_package = {
                "bullet_class": bullet,
                "fire_rate": 200,
                "burst": 3,
                "spread": 20
            }
        elif item_type == "quad_bullet":
            self.player.bullet_package = {
                "bullet_class": bullet,
                "fire_rate": 170,
                "burst": 4,
                "spread": 30
            }
        elif item_type == "six_bullet":
            self.player.bullet_package = {
                "bullet_class": bullet,
                "fire_rate": 150,
                "burst": 6,
                "spread": 45
            }

        # ⭐ LƯU THỜI GIAN
        self.active_effects[item_type] = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        expired = []

        for eff, start in self.active_effects.items():
            if now - start >= self.effect_duration.get(eff, 0):
                expired.append(eff)

        for eff in expired:
            if eff == "shield":
                self.player.has_shield = False
            else:
                # ⭐ RESET LẠI ĐẠN VỀ MẶC ĐỊNH
                bullet = self.player.bullet_package["bullet_class"]
                self.player.bullet_package = {
                    "bullet_class": bullet,
                    "fire_rate": 300,
                    "burst": 1,
                    "spread": 0
                }

            del self.active_effects[eff]

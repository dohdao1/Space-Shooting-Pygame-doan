import pygame
class ItemManager:
    def __init__(self, player):
        self.player = player
        self.active_effects = {}  # tất cả buff đang chạy
        self.effect_duration = {
            "double_bullet": 15000,
            "triple_bullet": 15000,
            "quad_bullet": 15000,
            "six_bullet": 15000,
            "shield": 15000
        }
        self.active_bullet = None  # buff đạn đang chạy
        self.bullet_end_time = 0
        self.active_shield = None  # buff shield đang chạy
        self.shield_end_time = 0

    def apply_item(self, item_type):
        now = pygame.time.get_ticks()

        if item_type == "life":
            self.player.game_ref.lives += 1
            return

        if item_type == "bomb":
            self.player.trigger_bomb = True
            return

        # --- SHIELD ---
        if item_type == "shield":
            self.player.activate_shield(6000)
            self.active_effects["shield"] = now
            self.active_shield = "shield"
            self.shield_end_time = now + self.effect_duration["shield"]
            return

        # --- BULLET ---
        if item_type in ["double_bullet", "triple_bullet", "quad_bullet", "six_bullet"]:
            # xóa bullet cũ nếu có
            if self.active_bullet:
                del self.active_effects[self.active_bullet]
            self.active_bullet = item_type
            self.bullet_end_time = now + self.effect_duration[item_type]
            self.active_effects[item_type] = now

            bullet = self.player.bullet_package["bullet_class"]

            if item_type == "double_bullet":
                self.player.bullet_package = {"bullet_class": bullet, "fire_rate": 250, "burst": 2, "spread": 0}
            elif item_type == "triple_bullet":
                self.player.bullet_package = {"bullet_class": bullet, "fire_rate": 200, "burst": 3, "spread": 20}
            elif item_type == "quad_bullet":
                self.player.bullet_package = {"bullet_class": bullet, "fire_rate": 170, "burst": 4, "spread": 30}
            elif item_type == "six_bullet":
                self.player.bullet_package = {"bullet_class": bullet, "fire_rate": 150, "burst": 6, "spread": 45}

    def update(self):
        now = pygame.time.get_ticks()
        expired = []

        for eff, start in list(self.active_effects.items()):
            if eff == "shield" and not self.player.has_shield:
                # khi khiên bị phá → xóa timeline luôn
                expired.append(eff)
                continue

            if now - start >= self.effect_duration.get(eff, 0):
                expired.append(eff)

        for eff in expired:
            if eff == "shield":
                self.active_shield = None
                self.shield_end_time = 0
                if "shield" in self.active_effects:
                    del self.active_effects["shield"]
            else:  # buff đạn
                bullet = self.player.bullet_package["bullet_class"]
                self.player.bullet_package = {"bullet_class": bullet, "fire_rate": 300, "burst": 1, "spread": 0}

                if self.active_bullet == eff:
                    self.active_bullet = None
                    self.bullet_end_time = 0
                if eff in self.active_effects:
                    del self.active_effects[eff]

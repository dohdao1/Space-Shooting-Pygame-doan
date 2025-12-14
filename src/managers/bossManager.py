import pygame
import random
from entities.boss import Boss
from entities.item import Item
from config import resource_path
from entities.explosion import Explosion

class BossManager:

    def __init__(
        self,
        spawner,
        boss_bullet_group,
        player_bullet_group,
        player,
        asteroid_group,
        hit_particles,
        player_bullets,
        item_group,
        game_ref
    ):
        self.boss = None
        self.spawner = spawner
        self.boss_bullets = boss_bullet_group
        self.player_bullet_group = player_bullet_group
        self.player = player
        self.asteroid_group = asteroid_group
        self.hit_particles = hit_particles
        self.player_bullets = player_bullets
        self.item_group = item_group
        self.game_ref = game_ref

        self.current_boss_score_milestone = None

        # ITEM RƠI KHI BOSS CHẾT (CỐ ĐỊNH)
        # ITEM DROP KHI BOSS CHẾT
        self.boss_drop_items = [
            "shield",
            "life",
            "quad_bullet",
            "six_bullet",
        ]

        # load boss image
        try:
            boss_image_0 = pygame.image.load(resource_path("assets/images/asteroid/boss.png")).convert_alpha()
            scale_factor = 0.6 # tỉ lệ
            new_width = int(boss_image_0.get_width() * scale_factor)
            new_height = int(boss_image_0.get_height() * scale_factor)
            self.boss_image = pygame.transform.scale(boss_image_0, (new_width, new_height))
            
        except Exception:
            surf = pygame.Surface((180,140), pygame.SRCALPHA)
            pygame.draw.ellipse(surf, (180,40,40), surf.get_rect())
            self.boss_image = surf

        # spawn effect
        self.spawning = False
        self.spawn_effect_start = 0
        self.spawn_effect_duration_ms = 1600

        self.spawned_milestones = set()
        self.entry_target_y = 40

        # shake
        self.shake_timer = 0
        self.shake_intensity = 4

    # ----------------------------------------------------
    def spawn_boss(self):
        if self.boss:
            return
    
        setattr(self.spawner, "stop_spawn", True)

        # Xác đinh milestone để spawn
        current_score = self.game_ref.score
        milestone_to_use = None
        
        for milestone in self.game_ref.boss_score_milestones:
            if current_score >= milestone and milestone not in self.spawned_milestones:
                milestone_to_use = milestone
                break
        
        if milestone_to_use is None:
            return  # Không có milestone nào phù hợp
        
        self.current_boss_score_milestone = milestone_to_use  # Lưu lại milestone này
        self.spawned_milestones.add(milestone_to_use)
        
        try:
            # iterate over a copy to be safe
            for a in list(self.asteroid_group):
                a.kill()
        except Exception:
            pass

        # CLEAR spawner effects / explosions if they exist on spawner
        try:
            if hasattr(self.spawner, "hit_particles"):
                self.spawner.hit_particles.empty()
            if hasattr(self.spawner, "explosions"):
                self.spawner.explosions.empty()
        except Exception:
            pass

        try:
            self.hit_particles.empty()
        except Exception:
            pass

        try:
            self.player_bullets.empty()
        except Exception:
            pass
        try:
            self.boss_bullets.empty()
        except Exception:
            pass

        setattr(self.spawner, "stop_spawn", True)

        # clear screen
        for a in list(self.asteroid_group):
            a.kill()

        self.player_bullets.empty()
        self.boss_bullets.empty()
        self.hit_particles.empty()

        self.boss = Boss(
            400,
            -300,
            self.boss_image,
            self.boss_bullets,
            self.player,
            self.player_bullet_group
        )

        self.boss.entry_target_y = self.entry_target_y

        self.spawning = True
        self.spawn_effect_start = pygame.time.get_ticks()

    # ----------------------------------------------------
    def spawning_effect_active(self):
        return self.spawning and (
            pygame.time.get_ticks() - self.spawn_effect_start
        ) < self.spawn_effect_duration_ms

    # ----------------------------------------------------
    def update(self, dt):
        if not self.boss:
            return

        # boss movement
        self.boss.update(dt)

        # boss entry done
        if self.spawning_effect_active():
            return
       
        self.boss.update(dt)

        try:
            player_top = self.player.rect.top
            
            min_gap = 200
            if self.boss.rect.bottom >= player_top - (min_gap // 2):
                
                target_y = max(self.boss.entry_target_y, player_top - min_gap)
                
                if self.boss.rect.y > target_y:
                    self.boss.rect.y = target_y
        except Exception:
            pass
        self.spawning = False

        # PLAYER BULLET → BOSS
        hits = pygame.sprite.spritecollide(
            self.boss,
            self.player_bullet_group,
            True,
            pygame.sprite.collide_mask
        )

        for bullet in hits:
            self.boss.take_damage(bullet.damage)

            # HIT PARTICLE
            self.hit_particles.add(
                Explosion(bullet.rect.centerx, bullet.rect.centery)
            )

            # SHAKE boss
            self.shake_timer = 6

        # shake effect
        if self.shake_timer > 0:
            offset = random.randint(-self.shake_intensity, self.shake_intensity)
            self.boss.rect.x += offset
            self.shake_timer -= 1

        # boss chết
        if self.boss.is_dead():
            # cộng điểm và kill
            if hasattr(self.game_ref, 'score'):
                self.game_ref.score += 100  # Boss = 100 điểm
                self.game_ref.total_kills += 1  # Boss = 1 kill

            # Thêm mile stone nếu cha nội nào rảnh quá chơi quá 180p 1 ngày
            if (hasattr(self.game_ref, 'boss_score_milestones') and self.current_boss_score_milestone is not None):
                milestones = self.game_ref.boss_score_milestones
                
                # Chỉ thêm milestone mới nếu đã đánh bại boss cuối cùng trong danh sách
                if len(milestones) > 0 and self.current_boss_score_milestone == milestones[-1]:
                    new_milestone = milestones[-1] + 1000  # Tăng 1000 điểm mỗi boss
                    milestones.append(new_milestone)
            self._on_boss_dead()

    # ----------------------------------------------------
    def _on_boss_dead(self):
        cx, cy = self.boss.rect.center
        self.game_ref.score += 100

        drop_count = random.randint(3, 5)
        drop_types = self.boss_drop_items.copy()

        for _ in range(drop_count):
            item_type = random.choice(drop_types)
            offset_x = random.randint(-60, 60)
            offset_y = random.randint(-30, 30)

            item = Item(cx + offset_x, cy + offset_y, item_type)
            self.item_group.add(item)

            self.boss.kill()
            self.boss = None
            setattr(self.spawner, "stop_spawn", False)
            self.spawning = False
            # trả về 
            self.current_boss_score_milestone = None
            
        self.boss.kill()
        self.boss = None
        setattr(self.spawner, "stop_spawn", False)

    # ----------------------------------------------------
    def draw(self, screen):
        if not self.boss:
            return

        # WARNING TEXT (KHÔNG FLASH)
        if self.spawning_effect_active():
            font = pygame.font.SysFont("arial", 52, bold=True)
            text = font.render("WARNING — BOSS INCOMING", True, (255,200,60))
            rect = text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
            screen.blit(text, rect)

        screen.blit(self.boss.image, self.boss.rect)
        self.draw_hp_bar(screen)

    # ----------------------------------------------------
    def draw_hp_bar(self, screen):
        bar_w, bar_h = 520, 16
        x = (screen.get_width()-bar_w)//2
        y = 22
        ratio = self.boss.hp / self.boss.max_hp

        pygame.draw.rect(screen, (30,30,30), (x,y,bar_w,bar_h))
        pygame.draw.rect(screen, (220,50,50), (x,y,int(bar_w*ratio),bar_h))
        pygame.draw.rect(screen, (255,255,255), (x,y,bar_w,bar_h), 2)

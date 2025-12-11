import pygame
import random
from entities.boss import Boss

class BossManager:

    def __init__(self, spawner, boss_bullet_group, player_bullet_group, player, asteroid_group, hit_particles, player_bullets):
        self.boss = None
        self.spawner = spawner
        self.boss_bullets = boss_bullet_group
        self.player_bullet_group = player_bullet_group
        self.player = player
        self.asteroid_group = asteroid_group
        self.hit_particles = hit_particles           
        self.player_bullets = player_bullets 

        # self.sfx_boss_hit = pygame.mixer.Sound("../assets/sounds/boss_hit.wav")
        # self.sfx_boss_hit.set_volume(0.55)        

       
        try:
            self.boss_image = pygame.image.load("../assets/images/asteroid/boss.png").convert_alpha()
        except Exception:
            surf = pygame.Surface((180, 140), pygame.SRCALPHA)
            pygame.draw.ellipse(surf, (180,40,40), surf.get_rect())
            self.boss_image = surf

        
        self.spawning = False
        self.spawn_effect_start = 0
        self.spawn_effect_duration_ms = 1800  # ms

       
        self.spawned_milestones = set()

        
        self.entry_target_y = 30

    def spawn_boss(self):

        if self.boss:
            return

        print("Boss xuất hiện — clearing screen")

        
        setattr(self.spawner, "stop_spawn", True)

        
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

        start_y = -350
        self.boss = Boss(
            400,
            start_y,
            self.boss_image,
            self.boss_bullets,
            self.player,
            self.player_bullet_group
        )

        
        self.boss.entry_target_y = self.entry_target_y

        
        self.spawning = True
        self.spawn_effect_start = pygame.time.get_ticks()

    def spawning_effect_active(self):
        if not self.spawning:
            return False
        return (pygame.time.get_ticks() - self.spawn_effect_start) < self.spawn_effect_duration_ms

    def update(self, dt):
       
        if not self.boss:
            return


        if self.spawning_effect_active():
        
            self.boss.update(dt)
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

        if self.boss.is_dead():
            print("Boss defeated")
          
            try:
                self.boss.kill()
            except Exception:
                pass
            self.boss = None


            setattr(self.spawner, "stop_spawn", False)

            
            self.spawning = False

    def draw(self, screen):
        if not self.boss:
            return


        if self.spawning_effect_active():
            # nháy
            elapsed = pygame.time.get_ticks() - self.spawn_effect_start
            alpha = int(255 * (1 - min(1.0, elapsed / self.spawn_effect_duration_ms)))
            
            flash = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            flash.fill((255, 80, 80, min(90, alpha//3)))
            screen.blit(flash, (0,0))

            # vẽ warning
            font = pygame.font.SysFont("arial", 56, bold=True)
            text = font.render("WARNING — BOSS INCOMING", True, (255, 220, 60))
            rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 20))
            screen.blit(text, rect)

        
        try:
            screen.blit(self.boss.image, self.boss.rect)
        except Exception:
            pass

        # draw hp bar
        self.draw_hp_bar(screen)

    def draw_hp_bar(self, screen):
        if not self.boss:
            return
        bar_width = 520
        bar_height = 16
        x = (screen.get_width() - bar_width) // 2
        y = 22
        ratio = max(0.0, min(1.0, self.boss.hp / (self.boss.max_hp if self.boss.max_hp else 1)))
        pygame.draw.rect(screen, (20,20,20), (x, y, bar_width, bar_height))
        pygame.draw.rect(screen, (200,40,40), (x, y, int(bar_width * ratio), bar_height))
        pygame.draw.rect(screen, (255,255,255), (x, y, bar_width, bar_height), 2)

import pygame, random, math
import sys, os

from managers.collision import CollisionSystem
from entities.player import Player
from entities.asteroid import Asteroid
from managers.itemManager import ItemManager
from managers.spawnAsteroid import AsteroidSpawner
from managers.bossManager import BossManager
from managers.collision import CollisionSystem
from entities.item import Item
from managers.skinManager import SkinManager
from managers.effects import ShieldBreakParticle, Shockwave

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import *
from .baseScreen import baseScreen


class gameScreen(baseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont('arial', 32)
        self.font_suggest = pygame.font.SysFont('arial', 20)

        self.heart_img = pygame.image.load("assets/images/ui/heart.png").convert_alpha()
        self.heart_img = pygame.transform.smoothscale(self.heart_img, (32, 32))

        self.item_icons = {}
        for name, path in Item.ICONS.items():
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.smoothscale(img, (35, 35))
            self.item_icons[name] = img



        # mốc điểm spawn boss
        self.boss_score_milestones = [1000, 2000, 4000]
        

        self.reset_game_state()

    def reset_game_state(self):
        self.game_start_time = pygame.time.get_ticks()
        self.play_time = 0
        self.total_kills = 0
        self.score = 0
        self.lives = 3
        self.is_paused = False
        self.screen_shake_time = 0 
        self.screen_shake_intensity = 5
        self.hit_particles = pygame.sprite.Group()
        self.shield_break_effects = pygame.sprite.Group() 
        self.shockwave_group = pygame.sprite.Group()

        self.skin_manager = SkinManager()
        # Player
        self.player = Player(
            x=self.screen.get_width() // 2,
            y=self.screen.get_height() - 80,
            speed=5
        )

        self.item_group = pygame.sprite.Group()
        self.item_manager = ItemManager(self.player)


        # Groups
        self.player_group = pygame.sprite.Group(self.player)
        self.bullet_group = pygame.sprite.Group()

        # Asteroids
        self.asteroid_group = pygame.sprite.Group()
       
        self.spawner = AsteroidSpawner(self.asteroid_group, screen_width=self.screen.get_width(), game_ref=self)

        # Collision system
        self.collision = CollisionSystem()

        # effects
        self.hit_particles = pygame.sprite.Group()

        # shields broken 
        self.shield_break_effects = pygame.sprite.Group()

        self.shockwave_group = pygame.sprite.Group()

        # Boss groups & manager
        self.boss_bullets = pygame.sprite.Group()
        # Pass asteroid_group and spawner so BossManager can clear them
        self.boss_manager = BossManager(
            spawner=self.spawner,
            boss_bullet_group=self.boss_bullets,
            player_bullet_group=self.bullet_group,
            player=self.player,
            asteroid_group=self.asteroid_group,
            hit_particles=self.hit_particles,
            player_bullets=self.bullet_group
        )

        # UI test
        self.score_button = pygame.Rect(10, 170, 100, 50)
        self.button_hover = False

        # local cooldown for player-boss collision
        self._last_boss_hit_ms = 0
        self._boss_hit_cooldown_ms = 500

            # cho phép item manager truy cập gameScreen (để + mạng)
        self.player.game_ref = self
    def handle_events(self, events):
        if self.is_paused:
            return

        for event in events:
            if event.type == pygame.QUIT:
                self.save_current_stats()   # Lưu trước khi thoát
                self.game.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                    # Lưu thống kê khi pause
                    self.save_current_stats()
                    # dừng nhạc nền
                    self.game.audio_manager.pause_music()
                    pygame.mouse.set_visible(True)
                    self.switch_to("pause")
                elif event.key == pygame.K_l:
                    self.lives = 0
                elif event.key == pygame.K_t:
                    self.score += 10
                elif event.key == pygame.K_y:
                    self.lives -= 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
 
    def update(self):
        if self.is_paused:
            return

        dt = self.game.clock.get_time() / 1000.0
        now_ms = pygame.time.get_ticks()
        last_update_time = now_ms

        if self.screen_shake_time > 0:
            self.screen_shake_time -= now_ms - last_update_time

        # ⭐ CẬP NHẬT NHÓM SHOCKWAVE
        try:
            self.shockwave_group.update(dt) 
        except TypeError:
            self.shockwave_group.update()

        # bomb effect
        if getattr(self.player, "trigger_bomb", False):
            # ⭐ KÍCH HOẠT RUNG KHI DÙNG BOMB
            self.screen_shake_time = 1000 # Rung 1 giây (1000ms)
            shockwave = Shockwave(self.player.rect.center)
            self.shockwave_group.add(shockwave)
            self.game.audio_manager.play_sound("bomb_explosion")
            self.player.trigger_bomb = False
        
        # ⭐ COLLISION: SHOCKWAVE VS ASTEROID
        shockwave_active = len(self.shockwave_group) > 0
        if shockwave_active:
            for shockwave in self.shockwave_group:
                # Tìm thiên thạch bị sóng xung kích chạm vào
                asteroids_hit = []
                for asteroid in self.asteroid_group:
                    # Kiểm tra khoảng cách: nếu khoảng cách <= bán kính sóng, thiên thạch bị va chạm
                    dist_sq = (asteroid.rect.centerx - shockwave.center_x)**2 + (asteroid.rect.centery - shockwave.center_y)**2
                    # Lấy bán kính thiên thạch lớn nhất (giả sử 30)
                    if dist_sq <= (shockwave.radius + 30)**2: 
                        asteroids_hit.append(asteroid)

                for asteroid in asteroids_hit:
                    # Tiêu diệt thiên thạch
                    self.score += 10
                    # Tạo hiệu ứng nổ nhỏ cho thiên thạch bị Bomb tiêu diệt
                    self.create_shield_break_particles(asteroid.rect.center) # Dùng lại hàm particle
                    asteroid.kill()

        # spawn boss when milestone reached (only once per milestone)
        if self.boss_manager.boss is None:
            for milestone in self.boss_score_milestones:
                if self.score >= milestone and milestone not in self.boss_manager.spawned_milestones:
                    # spawn boss and record milestone
                    self.boss_manager.spawn_boss()
                    self.boss_manager.spawned_milestones.add(milestone)
                    break

        # player input & update
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.bullet_group, self.screen.get_width())

        if self.player.shield_broken_at is not None:
            self.create_shield_break_particles(self.player.rect.center)
            self.player.shield_broken_at = None
            self.game.audio_manager.play_sound("shield_break")

        self.shield_break_effects.update(dt)
        

        # update player's bullets (some bullets may use dt, some not - update supports both)
        try:
            self.bullet_group.update(dt)
        except TypeError:
            self.bullet_group.update()

        # If boss present => stop asteroid spawn & don't update asteroid group
        if (self.boss_manager.boss is None) and (not self.boss_manager.spawning_effect_active()):
            # normal asteroid flow
            try:
                self.spawner.stop_spawn = False
            except Exception:
                pass

            self.spawner.update(dt)
            # the spawner updates asteroid_group internally, but call group update as well
            try:
                self.asteroid_group.update(dt)
            except TypeError:
                self.asteroid_group.update()

            # ⭐ COLLISION: BULLET VS ASTEROID → nhận dropped_items
            hit_particles, death_particles, dropped_items = self.collision.bullet_vs_asteroid(
                self.bullet_group,
                self.spawner
            )
            # ⭐ Spawn Item rơi ra từ asteroid
            for drop in dropped_items:
                item = Item(drop["pos"][0], drop["pos"][1], drop["type"])
                self.item_group.add(item)

            # asteroid vs player
            self.collision.asteroid_vs_player(self.spawner, self.player)

        else:
            # boss active or boss spawning effect: ensure spawner paused
            try:
                self.spawner.stop_spawn = True
            except Exception:
                pass

        # boss update + boss bullets
        try:
            self.boss_bullets.update(dt)
        except TypeError:
            self.boss_bullets.update()

        self.boss_manager.update(dt)

        # collisions: player hit by boss bullets
        hits_boss_bullet = pygame.sprite.spritecollide(self.player, self.boss_bullets, True, collided=pygame.sprite.collide_mask)
        if hits_boss_bullet:
            self.lives -= 1

        # collision: player <-> boss with cooldown
        if self.boss_manager.boss:
            if pygame.sprite.collide_mask(self.player, self.boss_manager.boss):
                if now_ms - self._last_boss_hit_ms > self._boss_hit_cooldown_ms:
                    self.lives -= 1
                    self._last_boss_hit_ms = now_ms
        # update items
        try:
            self.item_group.update(dt)
        except:
            self.item_group.update()
        
        # ⭐ PLAYER ĂN ITEM
        picked = pygame.sprite.spritecollide(
            self.player, 
            self.item_group, 
            True, 
            pygame.sprite.collide_mask
        )
        for item in picked:
            self.item_manager.apply_item(item.type)

        # ⭐ UPDATE ITEM MANAGER
        self.item_manager.update()

        # UI hover
        mouse_pos = pygame.mouse.get_pos()
        self.button_hover = self.score_button.collidepoint(mouse_pos)

        # check lose
        if self.lives <= 0:
            # Gọi hàm lưu vào save
            self.game_over()
            # Chạy âm thanh thua
            self.game.audio_manager.stop_music()
            self.game.audio_manager.play_sound("lose")

            self.game.game_over_data = {"score": self.score}
            pygame.mouse.set_visible(True)
            self.switch_to("game_over", self.score)


    def draw(self):

        # background
        self.screen.fill((10, 10, 30))

        # draw sprites
        self.player_group.draw(self.screen)
        self.bullet_group.draw(self.screen)

        # vẽ khiên nếu có
        self.player.draw_shield(self.screen)

        # ⭐ VẼ HIỆU ỨNG VỠ KHIÊN
        self.shield_break_effects.draw(self.screen)

        # draw asteroids (spawner may pause drawing but group remains)
        self.asteroid_group.draw(self.screen)

        # draw items
        self.item_group.draw(self.screen)

        # draw shockwaves
        self.shockwave_group.draw(self.screen)

        # draw boss (bossManager will render boss + effects)
        self.boss_bullets.draw(self.screen)
        self.boss_manager.draw(self.screen)

        # hit particles (from spawner)
        try:
            self.spawner.hit_particles.draw(self.screen)
            self.spawner.explosions.draw(self.screen)
        except Exception:
            pass

        # UI
        score_text = self.font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 20))

        # ❤️ Draw lives as hearts (max 5)
        for i in range(min(self.lives, 5)):
            self.screen.blit(self.heart_img, (20 + i * 40, 60))

        # ----- ITEM TIMELINE -----
        self.draw_item_timelines()


        # # score button
        # button_color = (100, 200, 100) if self.button_hover else (70, 170, 70)
        # pygame.draw.rect(self.screen, button_color, self.score_button, border_radius=8)
        # pygame.draw.rect(self.screen, (255, 255, 255), self.score_button, 2, border_radius=8)
        # button_text = self.font_suggest.render("+1 ĐIỂM", True, (255, 255, 255))
        # self.screen.blit(button_text, button_text.get_rect(center=self.score_button.center))

        # # life button
        # life_button = pygame.Rect(10, 240, 100, 50)
        # life_hover = life_button.collidepoint(pygame.mouse.get_pos())
        # life_color = (200, 100, 100) if life_hover else (170, 70, 70)
        # pygame.draw.rect(self.screen, life_color, life_button, border_radius=8)
        # pygame.draw.rect(self.screen, (255, 255, 255), life_button, 2, border_radius=8)
        # life_text = self.font_suggest.render("-1 MẠNG", True, (255, 255, 255))
        # self.screen.blit(life_text, life_text.get_rect(center=life_button.center))

        # help
        help_text = self.font_suggest.render("ESC/P: Pause Menu | L: Lose(thua ngay)", True, (200, 200, 200))
        self.screen.blit(help_text, (3*self.screen.get_width()/5, 20))

    # Xử lý khi game thua
    def game_over(self):
        # Tính coin thưởng dựa trên điểm số
        coin_reward = self.score // 10  # 1 coin cho mỗi 10 điểm
        
        # Cập nhật điểm cao
        self.game.save_manager.update_high_score(self.score)
        
        # Thêm coin vào tài khoản
        self.game.save_manager.add_coin(coin_reward)
        
        # Thêm vào lịch sử game
        self.game.save_manager.add_game_history(
            score=self.score,
            play_time=self.play_time,
            kills=self.total_kills,
            deaths=1  # mỗi lần thua tính 1 death
        )

        self.game.audio_manager.stop_music()
    # ⭐ HÀM TẠO HIỆU ỨNG VỠ KHIÊN
    def create_shield_break_particles(self, center_pos):
        for _ in range(15): # Tạo 15 mảnh vỡ
            particle = ShieldBreakParticle(center_pos[0], center_pos[1])
            self.shield_break_effects.add(particle)


    # Lưu tạm thời khi pause hoặc thoát game
    def save_current_stats(self):
        stats = self.game.save_manager.load_stats()
        
        # Cập nhật điểm cao nếu cần
        if self.score > stats['high_score']:
            stats['high_score'] = self.score
            self.game.save_manager.save_stats(stats)
    

    def draw_item_timelines(self):
        now = pygame.time.get_ticks()
        start_x = 20

        # Danh sách item hiển thị
        timelines = []

        if self.item_manager.active_bullet:
            item = self.item_manager.active_bullet
            remaining = max(0, self.item_manager.bullet_end_time - now)
            duration = self.item_manager.effect_duration.get(item, 0)
            if remaining > 0:
                timelines.append((item, remaining, duration, 110))

        if self.item_manager.active_shield:
            item = self.item_manager.active_shield
            remaining = max(0, self.item_manager.shield_end_time - now)
            duration = self.item_manager.effect_duration.get(item, 0)
            if remaining > 0:
                timelines.append((item, remaining, duration, 140))

        # Vẽ tất cả timeline
        for item, remaining, duration, start_y in timelines:
            icon = self.item_icons[item]
            self.screen.blit(icon, (start_x, start_y))

            # Timeline bar
            bar_x, bar_y = start_x + 45, start_y + 12
            bar_width, bar_height = 150, 12

            # Background
            pygame.draw.rect(self.screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height), border_radius=6)

            # Fill theo phần trăm còn lại
            percent = remaining / duration
            fill_width = int(bar_width * percent)
            pygame.draw.rect(self.screen, (50, 200, 255), (bar_x, bar_y, fill_width, bar_height), border_radius=6)

            # Border
            pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2, border_radius=6)

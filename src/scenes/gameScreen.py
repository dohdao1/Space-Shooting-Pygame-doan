import pygame
import sys, os

from entities.player import Player
from entities.asteroid import Asteroid
from managers.spawnAsteroid import AsteroidSpawner

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import *
from .baseScreen import baseScreen

class gameScreen(baseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont('arial', 32)
        self.font_suggest = pygame.font.SysFont('arial', 20)

        # Thoonh tin cần lưu
        self.game_start_time = pygame.time.get_ticks()
        self.play_time = 0  # thời gian chơi tính bằng giây
        self.total_kills = 0  # số asteroid đã tiêu diệt

        # reset game state khi khởi tạo màn hình
        self.reset_game_state()

    def reset_game_state(self):
        self.game_start_time = pygame.time.get_ticks()
        self.play_time = 0
        self.total_kills = 0
        self.score = 0
        self.lives = 3
        self.is_paused = False

        # tạo Player thật
        self.player = Player(
            x=self.screen.get_width() // 2,
            y=self.screen.get_height() - 80,
            speed=5
        )

        # nhóm sprite
        self.player_group = pygame.sprite.Group(self.player)
        self.bullet_group = pygame.sprite.Group()

        # nhóm Asteroid
        self.asteroid_group = pygame.sprite.Group()
        self.spawner = AsteroidSpawner(self.asteroid_group, screen_width=self.screen.get_width())

        #hiệu dứng bắn trúng
        self.hit_particles =pygame.sprite.Group()

        # test UI
        self.score_button = pygame.Rect(10, 170, 100, 50)
        self.button_hover = False

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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
 
    def update(self):
        if self.is_paused:
            return

        dt = self.game.clock.get_time()/1000.0

        # Cập nhật thời gian chơi
        self.play_time = (pygame.time.get_ticks() - self.game_start_time) / 1000.0

        # lấy phím nhấn hiện tại
        keys = pygame.key.get_pressed()

        # update Player: di chuyển + bắn đạn
        self.player.update(keys, self.bullet_group, self.screen.get_width())

        # update đạn
        self.bullet_group.update()

        # update asteroid
        # self.asteroid_group.update(dt)
        self.spawner.update(dt)

        self.spawner.handle_bullet_collision(self.bullet_group, game_screen=self)
        hits_player = pygame.sprite.spritecollide(self.player, self.asteroid_group, False, collided=pygame.sprite.collide_mask)
        for asteroid in hits_player:
            self.lives -= 1
            asteroid.reset()

        # hover nút cộng điểm
        mouse_pos = pygame.mouse.get_pos()
        self.button_hover = self.score_button.collidepoint(mouse_pos)

        # kiểm tra thua
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
        # nền
        self.screen.fill((10, 10, 30))

        # vẽ Player & Bullet
        self.player_group.draw(self.screen)
        self.bullet_group.draw(self.screen)

        #vẽ asteroid
        self.asteroid_group.draw(self.screen)

        #hiệu ứng đạn
        self.spawner.hit_particles.draw(self.screen)
        self.spawner.explosions.draw(self.screen)

        # vẽ UI điểm & mạng
        score_text = self.font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 20))

        lives_text = self.font.render(f"LIVES: {self.lives}", True, (255, 50, 50))
        self.screen.blit(lives_text, (20, 60))

        # hướng dẫn
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


    # Lưu tạm thời khi pause hoặc thoát game
    def save_current_stats(self):
        stats = self.game.save_manager.load_stats()
        
        # Cập nhật điểm cao nếu cần
        if self.score > stats['high_score']:
            stats['high_score'] = self.score
            self.game.save_manager.save_stats(stats)
        
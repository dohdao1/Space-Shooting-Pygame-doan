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

        # reset game state khi khởi tạo màn hình
        self.reset_game_state()

    def reset_game_state(self):
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
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_p]:
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
                    if self.score_button.collidepoint(mouse_pos):
                        self.score += 1
                    life_button = pygame.Rect(10, 240, 100, 50)
                    if life_button.collidepoint(mouse_pos) and self.lives > 0:
                        self.lives -= 1

    def update(self):
        if self.is_paused:
            return

        dt = self.game.clock.get_time()/1000.0

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
            self.game.game_over_data = {"score": self.score}
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

        # nút cộng điểm
        button_color = (100, 200, 100) if self.button_hover else (70, 170, 70)
        pygame.draw.rect(self.screen, button_color, self.score_button, border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 255), self.score_button, 2, border_radius=8)
        button_text = self.font_suggest.render("+1 ĐIỂM", True, (255, 255, 255))
        self.screen.blit(button_text, button_text.get_rect(center=self.score_button.center))

        # nút trừ mạng
        life_button = pygame.Rect(10, 240, 100, 50)
        life_hover = life_button.collidepoint(pygame.mouse.get_pos())
        life_color = (200, 100, 100) if life_hover else (170, 70, 70)
        pygame.draw.rect(self.screen, life_color, life_button, border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 255), life_button, 2, border_radius=8)
        life_text = self.font_suggest.render("-1 MẠNG", True, (255, 255, 255))
        self.screen.blit(life_text, life_text.get_rect(center=life_button.center))

        # hướng dẫn
        help_text = self.font_suggest.render("ESC/P: Pause Menu | L: Lose(thua ngay)", True, (200, 200, 200))
        self.screen.blit(help_text, (3*self.screen.get_width()/5, 20))

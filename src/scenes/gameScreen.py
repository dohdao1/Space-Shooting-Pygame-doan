# đây sẽ là màn hình hoạt động chính của game nha
import pygame
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import *
from .baseScreen import baseScreen

class gameScreen(baseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont('arial', 32)
        self.font_suggest = pygame.font.SysFont('arial',20)
        
        # reset các game state khi khởi tạo màn hình
        self.reset_game_state()

         # Tạo nút cộng điểm, để test thui
        self.score_button = pygame.Rect(10, 170, 100, 50)
        self.button_hover = False

    # reset khi chơi lại
    def reset_game_state(self):
        self.score = 0
        self.lives = 3
        self.is_paused = False
        
        # Player(cái này tui test di chuyển người chơi trong hàm update thôi á, nào làm xóa đi nha)
        self.player_rect = pygame.Rect(0, 0, 50, 50)
        self.player_rect.centerx = self.screen.get_width() // 2
        self.player_rect.bottom = self.screen.get_height() - 50
        self.player_speed = 5
    
    def handle_events(self, events):
        if self.is_paused:
            return
            
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:    # hiển thị cả khi ấn thoát
                    self.switch_to("pause")  # Chuyển sang pause menu
                # Kiểm tra thua, tự thua
                elif event.key == pygame.K_l:  # Nút L nha
                    self.lives = 0
            
                # Thêm phím tắt để cộng điểm( test thui á)
                elif event.key == pygame.K_t:  # Nhấn T để cộng 10 điểm
                    self.score += 10
                    print(f"+10 điểm! Tổng: {self.score}")
                elif event.key == pygame.K_y:  # Nhấn Y để trừ 1 mạng
                    self.lives -= 1
                    print(f"-1 mạng! Còn: {self.lives}")

            # khi ấn chuột
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Chuột trái
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Kiểm tra click vào nút cộng điểm
                    if self.score_button.collidepoint(mouse_pos):
                        self.score += 1
                        print(f"Click! +1 điểm! Tổng: {self.score}")
                    
                    # Kiểm tra click vào nút trừ mạng
                    life_button = pygame.Rect(10, 240, 100, 50)
                    if life_button.collidepoint(mouse_pos):
                        if self.lives > 0:
                            self.lives -= 1
                            print(f"-1 mạng! Còn: {self.lives}")
    
    def update(self):
        if self.is_paused:
            return
            
        # Di chuyển player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_rect.x -= self.player_speed
        if keys[pygame.K_RIGHT]:
            self.player_rect.x += self.player_speed
        if keys[pygame.K_UP]:
            self.player_rect.y -= self.player_speed
        if keys[pygame.K_DOWN]:
            self.player_rect.y += self.player_speed
        
        # Giới hạn màn hình( không chơi chơi ra ngoài)
        self.player_rect.left = max(0, self.player_rect.left)
        self.player_rect.right = min(self.screen.get_width(), self.player_rect.right)
        self.player_rect.top = max(0, self.player_rect.top)
        self.player_rect.bottom = min(self.screen.get_height(), self.player_rect.bottom)
        
        # Kiểm tra hover nút
        mouse_pos = pygame.mouse.get_pos()
        self.button_hover = self.score_button.collidepoint(mouse_pos)

        # Kiểm tra thua
        if self.lives <= 0:
            # lưu điểm tại thời điển thua
            self.game.game_over_data = {"score": self.score}
            # chuyển qua màn hình thua
            self.switch_to("game_over",self.score)
            print(f"thua do bạn quá gà!, Bạn được: {self.score}")
            return
    
    # vẽ giao diện
    def draw(self):
        # Nền
        self.screen.fill((10, 10, 30))
        
        # Vẽ player
        pygame.draw.rect(self.screen, (0, 255, 0), self.player_rect)
        
        # Vẽ UI
        score_text = self.font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 20))
        
        lives_text = self.font.render(f"LIVES: {self.lives}", True, (255, 50, 50))
        self.screen.blit(lives_text, (20, 60))

        # làm cái nút để cộng thêm điểm, test nha
        button_color = (100, 200, 100) if self.button_hover else (70, 170, 70)
        pygame.draw.rect(self.screen, button_color, self.score_button, border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 255), self.score_button, 2, border_radius=8)
        #chữ trên nút test
        button_text = self.font_suggest.render("+1 ĐIỂM", True, (255, 255, 255))
        text_rect = button_text.get_rect(center=self.score_button.center)
        self.screen.blit(button_text, text_rect)

        # nút trừ mạng
        life_button = pygame.Rect(10, 240, 100, 50)
        life_hover = life_button.collidepoint(pygame.mouse.get_pos())
        life_color = (200, 100, 100) if life_hover else (170, 70, 70)
        pygame.draw.rect(self.screen, life_color, life_button, border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 255), life_button, 2, border_radius=8)
        
        life_text = self.font_suggest.render("-1 MẠNG", True, (255, 255, 255))
        life_text_rect = life_text.get_rect(center=life_button.center)
        self.screen.blit(life_text, life_text_rect)
        
        # Hướng dẫn
        help_text = self.font_suggest.render("ESC/P: Pause Menu | L: Lose(thua ngay)", True, (200, 200, 200))
        self.screen.blit(help_text, (3*self.screen.get_width()/5, 20))
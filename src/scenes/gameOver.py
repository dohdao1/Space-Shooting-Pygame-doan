# hiển thị khi người chơi thu
import pygame
from .baseScreen import baseScreen

class gameOver(baseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.font_large = pygame.font.SysFont('arial', 72, bold=True)
        self.font_normal = pygame.font.SysFont('arial', 36)
        self.font_small = pygame.font.SysFont('arial', 28)
        
        # Lấy điểm số từ game
        self.final_score = 0
        # Các nút
        self.buttons = [
            {"text": "PLAY AGAIN", "action": "play_again", "rect": pygame.Rect(0, 0, 300, 50)},
            {"text": "MAIN MENU", "action": "main_menu", "rect": pygame.Rect(0, 0, 300, 50)},
            {"text": "QUIT", "action": "quit", "rect": pygame.Rect(0, 0, 300, 50)}
        ]
        
        # Cập nhật vị trí
        center_x = self.screen.get_width() // 2
        start_y = 350
        for i, button in enumerate(self.buttons):
            button["rect"].center = (center_x, start_y + i * 70)
    
    # xử lý khi người chơi chọn để chuyển trang hoặc chơi lại, bằng nút hoặc chuột
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.switch_to("game")
                elif event.key == pygame.K_ESCAPE:
                    self.switch_to("main_menu")
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            if button["action"] == "play_again":
                                self.switch_to("game")
                            elif button["action"] == "main_menu":
                                self.switch_to("main_menu")
                            elif button["action"] == "quit":
                                self.game.running = False
    
    # lấy dữ liệu, điểm khi thua
    def set_data(self, data):
        if data:
            self.final_score = data

    # lấy dc tọa độ chuột của người chơi
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button["hover"] = button["rect"].collidepoint(mouse_pos)
    
    # vẽ giao diện
    def draw(self):
        # Nền
        self.screen.fill((40, 10, 10))  # Đỏ đậm
        
        # Tiêu đề
        title = self.font_large.render("GAME OVER", True, (255, 50, 50))
        title_rect = title.get_rect(center=(self.screen.get_width()//2, 150))
        self.screen.blit(title, title_rect)
        
        # Điểm số
        score_text = self.font_normal.render(f"FINAL SCORE: {self.final_score}", True, (255, 255, 100))
        score_rect = score_text.get_rect(center=(self.screen.get_width()//2, 250))
        self.screen.blit(score_text, score_rect)
        
        # Vẽ các nút
        for button in self.buttons:
            color = (180, 60, 60) if button.get("hover") else (140, 40, 40)
            
            pygame.draw.rect(self.screen, color, button["rect"], border_radius=10)
            pygame.draw.rect(self.screen, (200, 200, 200), button["rect"], 3, border_radius=10)
            
            text = self.font_normal.render(button["text"], True, (255, 255, 255))
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)
        
        # Hướng dẫn
        help1 = self.font_small.render("ENTER: Play Again | ESC: Main Menu", True, (200, 200, 200))
        help1_rect = help1.get_rect(center=(self.screen.get_width()//2, 550))
        self.screen.blit(help1, help1_rect)
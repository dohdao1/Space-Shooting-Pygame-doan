#Màn hình chính hiển thị bắt khi mở game
import pygame
from .baseScreen import baseScreen

class mainMenu(baseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.font_large = pygame.font.SysFont('arial', 72, bold=True)
        self.font_normal = pygame.font.SysFont('arial', 36)
        self.font_small = pygame.font.SysFont('arial', 28)
        
        # Các nút
        self.buttons = [
            {"text": "START GAME", "action": "game", "rect": pygame.Rect(0, 0, 300, 50)},
            {"text": "SHOP", "action": "shop", "rect": pygame.Rect(0, 0, 300, 50)},
            {"text": "HOW TO PLAY", "action": "howto", "rect": pygame.Rect(0, 0, 300, 50)},
            {"text": "QUIT", "action": "quit", "rect": pygame.Rect(0, 0, 300, 50)}
        ]
        
        # Cập nhật vị trí nút
        screen_center_x = self.screen.get_width() // 2
        start_y = 300
        for i, button in enumerate(self.buttons):
            button["rect"].center = (screen_center_x, start_y + i * 70)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.switch_to("game")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click chuột trái
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            if button["action"] == "game":
                                self.switch_to("game")
                            elif button["action"] == "shop":
                                self.switch_to("shop")
                            elif button["action"] == "quit":
                                self.game.running = False
    
    def update(self):
        # Hiệu ứng hover cho nút
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button["hover"] = button["rect"].collidepoint(mouse_pos)
    
    def draw(self):
        # Nền
        self.screen.fill((20, 20, 40))
        
        # Tiêu đề
        title = self.font_large.render("SPACE SHOOTER", True, (100, 200, 255))
        title_rect = title.get_rect(center=(self.screen.get_width()//2, 150))
        self.screen.blit(title, title_rect)
        
        # Vẽ các nút
        for button in self.buttons:
            # Màu nút
            color = (70, 130, 180) if button.get("hover") else (50, 100, 150)
            
            # Vẽ nền nút
            pygame.draw.rect(self.screen, color, button["rect"], border_radius=10)
            pygame.draw.rect(self.screen, (200, 200, 200), button["rect"], 3, border_radius=10)
            
            # Vẽ chữ
            text = self.font_normal.render(button["text"], True, (255, 255, 255))
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)
        
        # Hướng dẫn
        help_text = self.font_small.render("Press ENTER to start or click buttons", True, (200, 200, 200))
        help_rect = help_text.get_rect(center=(self.screen.get_width()//2, 550))
        self.screen.blit(help_text, help_rect)
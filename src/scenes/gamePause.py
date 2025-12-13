# màn hình(hộp thoại hiển thị khi dừng khi đang chơi)
import pygame
from .baseScreen import baseScreen

class pauseMenu(baseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.font_large = pygame.font.SysFont('arial', 64, bold=True)
        self.font_normal = pygame.font.SysFont('arial', 36)
        
        # Các nút
        self.buttons = [
            {"text": "RESUME", "action": "resume", "rect": pygame.Rect(0, 0, 300, 50)},
            {"text": "MAIN MENU", "action": "main_menu", "rect": pygame.Rect(0, 0, 300, 50)},
            {"text": "QUIT", "action": "quit", "rect": pygame.Rect(0, 0, 300, 50)}
        ]
        
        # Cập nhật vị trí
        center_x = self.screen.get_width() // 2
        start_y = 250
        for i, button in enumerate(self.buttons):
            button["rect"].center = (center_x, start_y + i * 70)
    
    def handle_events(self, events):
        for event in events:
            pygame.mouse.set_visible(True)
            if event.type == pygame.KEYDOWN:
                self.game.audio_manager.play_sound("shooter_sfx", volume_scale=0.3)
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    self.switch_to("game")  # Quay lại game
                elif event.key == pygame.K_RETURN:
                    self.switch_to("game")
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.game.audio_manager.play_sound("shooter_sfx", volume_scale=0.3)
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        self.game.audio_manager.play_sound("shooter_sfx", volume_scale=0.3)
                        if button["rect"].collidepoint(mouse_pos):
                            if button["action"] == "resume":
                                self.switch_to("game")
                                # tiếp tục nhạc
                                self.game.audio_manager.play_music("gameplay")

                            elif button["action"] == "main_menu":
                                self.switch_to("main_menu")
                            elif button["action"] == "quit":
                                self.game.running = False
    
    def update(self):
        # Hiệu ứng hover
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button["hover"] = button["rect"].collidepoint(mouse_pos)
    
    def draw(self):
        # Vẽ nền mờ
        if hasattr(self.game, 'current_scene') and self.game.current_scene.__class__.__name__ == "GameScene":
            self.game.current_scene.draw()
            
            # Thêm lớp mờ đen
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))  # Đen với độ trong suốt
            self.screen.blit(overlay, (0, 0))
        else:
            self.screen.fill((30, 30, 60))
        
        # Tiêu đề
        title = self.font_large.render("GAME PAUSED", True, (255, 255, 100))
        title_rect = title.get_rect(center=(self.screen.get_width()//2, 150))
        self.screen.blit(title, title_rect)
        
        # Vẽ các nút
        for button in self.buttons:
            color = (80, 180, 80) if button.get("hover") else (60, 140, 60)
            
            pygame.draw.rect(self.screen, color, button["rect"], border_radius=10)
            pygame.draw.rect(self.screen, (200, 200, 200), button["rect"], 3, border_radius=10)
            
            text = self.font_normal.render(button["text"], True, (255, 255, 255))
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)
        
        # Hướng dẫn
        help_text = self.font_normal.render("ESC: Resume Game", True, (200, 200, 200))
        help_rect = help_text.get_rect(center=(self.screen.get_width()//2, 500))
        self.screen.blit(help_text, help_rect)
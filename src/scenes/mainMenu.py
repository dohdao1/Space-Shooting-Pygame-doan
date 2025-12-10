#Màn hình chính hiển thị bắt khi mở game
import pygame
from .baseScreen import baseScreen
from config import *

class mainMenu(baseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.font_large = pygame.font.SysFont('arial', 72, bold=True)
        self.font_normal = pygame.font.SysFont('arial', 36)
        self.font_small = pygame.font.SysFont('arial', 28)
        
        # Các nút
        self.buttons = [
            {"text": "START GAME", "action": "game", "rect": pygame.Rect(0, 0, 300, 50)},
            {"text": "ACHIEVEMENTS", "action": "stats", "rect": pygame.Rect(0, 0, 300, 50)}, # bỏ mịa cái how to đi
            {"text": "SHOP", "action": "shop", "rect": pygame.Rect(0, 0, 300, 50)},
            {"text": "QUIT", "action": "quit", "rect": pygame.Rect(0, 0, 300, 50)}
        ]
        
        # Cập nhật vị trí nút
        screen_center_x = self.screen.get_width() // 2
        start_y = 280
        for i, button in enumerate(self.buttons):
            button["rect"].center = (screen_center_x, start_y + i * 70)

        # nút bánh răng cài đặt (40x40)
        self.gear_button = pygame.Rect(self.screen.get_width() - 60, 20, 40, 40)
        self.gear_hover = False

    def on_enter(self):
        # load setting
        if hasattr(self.game, 'save_manager'):
            # Load settings mới nhất từ file
            new_settings = self.game.save_manager.load_settings()
            
            # Cập nhật settings trong game
            self.game.settings = new_settings
            
            # Cập nhật audio manager với settings mới
            if hasattr(self.game, 'audio_manager'):
                self.game.audio_manager.load_settings()
        
        # xử lý âm thanh
        if hasattr(self.game, 'audio_manager'):
            if (not self.game.audio_manager.is_music_playing() or self.game.audio_manager.current_music != "menu"):
                self.game.audio_manager.play_music("menu")
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.audio_manager.play_sound("shooter_sfx", volume_scale=0.3)
                    self.game.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click chuột trái
                    mouse_pos = pygame.mouse.get_pos()

                    # Kiểm tra nút bánh răng
                    if self.gear_button.collidepoint(mouse_pos):
                        self.game.audio_manager.play_sound("shooter_sfx", volume_scale=0.3)
                        self.switch_to("settings")
                        return
                    
                    for button in self.buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            self.game.audio_manager.play_sound("shooter_sfx", volume_scale=0.3)
                            if button["action"] == "game":
                                self.switch_to("game")
                                # bật âm thanh
                                self.game.audio_manager.play_music("gameplay")

                            elif button["action"] == "stats":
                                self.switch_to("stats")
                            elif button["action"] == "shop":
                                self.switch_to("shop")
                            elif button["action"] == "quit":
                                self.game.running = False
    
    def update(self):
        # Hiệu ứng hover cho nút
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button["hover"] = button["rect"].collidepoint(mouse_pos)

        # Hiệu ứng hover cho nút bánh răng
        self.gear_hover = self.gear_button.collidepoint(mouse_pos)

    def draw(self):
        # Nền
        bg_color = self.game.settings.get('bg_color', BLACK)
        self.screen.fill((bg_color))
        
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
        
        # nút cài đặt
        gear_color = (220, 180, 40) if self.gear_hover else (180, 140, 20)
        pygame.draw.rect(self.screen, gear_color, self.gear_button, border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 200), self.gear_button, 2, border_radius=8)
        # Vẽ icon bánh răng đơn giản
        center_x = self.gear_button.centerx
        center_y = self.gear_button.centery
        # Vẽ các cạnh bánh răng
        pygame.draw.circle(self.screen, (255, 255, 200), (center_x, center_y), 8)
        pygame.draw.circle(self.screen, gear_color, (center_x, center_y), 5)
        # Vẽ các "răng" bánh răng
        for angle in range(0, 360, 45):
            rad = angle * 3.14159 / 180
            x1 = center_x + 12 * pygame.math.Vector2(1, 0).rotate(angle).x
            y1 = center_y + 12 * pygame.math.Vector2(1, 0).rotate(angle).y
            x2 = center_x + 18 * pygame.math.Vector2(1, 0).rotate(angle).x
            y2 = center_y + 18 * pygame.math.Vector2(1, 0).rotate(angle).y
            
            pygame.draw.line(self.screen, (255, 255, 200), (x1, y1), (x2, y2), 3)
        
        # Hướng dẫn
        help_text = self.font_small.render("Press ENTER to start or click buttons", True, (200, 200, 200))
        help_rect = help_text.get_rect(center=(self.screen.get_width()//2, 550))
        self.screen.blit(help_text, help_rect)
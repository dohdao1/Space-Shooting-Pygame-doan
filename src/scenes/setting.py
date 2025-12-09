# Màn hình setting
import pygame
from .baseScreen import baseScreen
from utils.map_color import get_theme, update_settings_with_theme

class settingScreen(baseScreen):
    def __init__(self, game):
        super().__init__(game)
        
        # Tải settings từ SecureSaveManager và map theme
        if hasattr(game, 'save_manager'):
            raw_settings = game.save_manager.load_settings()
            # MAP THEME -> MÀU SẮC
            self.settings = update_settings_with_theme(raw_settings)
        else:
            # Fallback
            from utils.map_color import get_default_settings
            self.settings = get_default_settings()
        
        # Font
        self.font_title = pygame.font.SysFont('arial', 48, bold=True)
        self.font_normal = pygame.font.SysFont('arial', 32)
        self.font_small = pygame.font.SysFont('arial', 24)
        
        # Slider cho volume
        self.sliders = {
            'music': {
                'value': self.settings.get('music_volume', 0.5),
                'rect': pygame.Rect(300, 160, 200, 20),
                'dragging': False
            },
            'sfx': {
                'value': self.settings.get('sfx_volume', 0.7),
                'rect': pygame.Rect(300, 230, 200, 20),
                'dragging': False
            }
        }
        
        # Theme hiện tại
        self.selected_theme = self.settings.get('theme', 'dark')
        self.theme_info = get_theme(self.selected_theme)
        
        # Radio button cho theme
        self.theme_buttons = [
            {"name": "Dark", "value": "dark", "rect": pygame.Rect(300, 290, 200, 40)},
            {"name": "Light", "value": "light", "rect": pygame.Rect(300, 340, 200, 40)},
            {"name": "Gray", "value": "gray", "rect": pygame.Rect(300, 390, 200, 40)}
        ]
        
        # Nút Back
        self.back_button = pygame.Rect(200, 500, 150, 50)
        
        # Nút Reset Data
        self.reset_button = pygame.Rect(450, 500, 150, 50)
        
        # Checkbox cho âm nhạc/hiệu ứng
        self.music_checkbox = pygame.Rect(570, 160, 20, 20)
        self.sfx_checkbox = pygame.Rect(570, 230, 20, 20)
        
        # Cập nhật nhạc ngay lập tức
        music_enabled = self.settings.get('music_enabled', True)
        if music_enabled:
            pygame.mixer.music.set_volume(self.settings.get('music_volume', 0.5))
        else:
            pygame.mixer.music.set_volume(0)
        
        # Biến trạng thái
        self.back_hover = False
        self.reset_hover = False
        self.show_reset_confirmation = False
        
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.show_reset_confirmation:
                        self.show_reset_confirmation = False
                    else:
                        self.save_settings()
                        self.switch_to("main_menu")
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Chuột trái
                    # Nếu đang show confirmation dialog
                    if self.show_reset_confirmation:
                        yes_btn, no_btn = self.show_reset_confirmation_dialog()
                        if yes_btn.collidepoint(mouse_pos):
                            if hasattr(self.game, 'save_manager'):
                                self.game.save_manager.reset_all_data()
                                print("Đã reset tất cả dữ liệu")
                            self.show_reset_confirmation = False
                        elif no_btn.collidepoint(mouse_pos):
                            self.show_reset_confirmation = False
                        return
                    
                    # Kiểm tra click slider music
                    if self.sliders['music']['rect'].collidepoint(mouse_pos):
                        self.sliders['music']['dragging'] = True
                        self.update_slider_value('music', mouse_pos[0])
                    
                    # Kiểm tra click slider sfx
                    elif self.sliders['sfx']['rect'].collidepoint(mouse_pos):
                        self.sliders['sfx']['dragging'] = True
                        self.update_slider_value('sfx', mouse_pos[0])
                    
                    # Kiểm tra checkbox âm nhạc
                    elif self.music_checkbox.collidepoint(mouse_pos):
                        self.settings['music_enabled'] = not self.settings.get('music_enabled', True)
                        if not self.settings['music_enabled']:
                            pygame.mixer.music.set_volume(0)
                        else:
                            pygame.mixer.music.set_volume(self.settings['music_volume'])
                    
                    # Kiểm tra checkbox hiệu ứng
                    elif self.sfx_checkbox.collidepoint(mouse_pos):
                        self.settings['sfx_enabled'] = not self.settings.get('sfx_enabled', True)
                    
                    # Kiểm tra nút Back
                    elif self.back_button.collidepoint(mouse_pos):
                        self.save_settings()
                        self.switch_to("main_menu")
                    
                    # Kiểm tra nút Reset Data
                    elif self.reset_button.collidepoint(mouse_pos):
                        self.show_reset_confirmation = True

                    # Kiểm tra radio button theme
                    for theme_btn in self.theme_buttons:
                        if theme_btn['rect'].collidepoint(mouse_pos):
                            self.selected_theme = theme_btn['value']
                            self.settings['theme'] = theme_btn['value']
                            # Update theme info ngay lập tức
                            self.theme_info = get_theme(self.selected_theme)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.sliders['music']['dragging'] = False
                    self.sliders['sfx']['dragging'] = False
            
            elif event.type == pygame.MOUSEMOTION:
                # Kéo slider
                if self.sliders['music']['dragging']:
                    self.update_slider_value('music', mouse_pos[0])
                elif self.sliders['sfx']['dragging']:
                    self.update_slider_value('sfx', mouse_pos[0])
    
    # Cập nhật giá trị slide
    def update_slider_value(self, slider_name, mouse_x):
        slider = self.sliders[slider_name]
        rect = slider['rect']
        
        # Tính giá trị từ vị trí chuột
        relative_x = max(0, min(mouse_x - rect.x, rect.width))
        value = relative_x / rect.width
        
        # Cập nhật giá trị
        slider['value'] = value
        
        # Áp dụng ngay lập tức
        if slider_name == 'music':
            self.settings['music_volume'] = value
            if self.settings.get('music_enabled', True):
                pygame.mixer.music.set_volume(value)
        elif slider_name == 'sfx':
            self.settings['sfx_volume'] = value
    
    def save_settings(self):
        try:
            if hasattr(self.game, 'save_manager'):
                # Chỉ lưu 5 fields cơ bản, không lưu derived colors
                settings_to_save = {
                    'music_volume': self.settings.get('music_volume', 0.5),
                    'sfx_volume': self.settings.get('sfx_volume', 0.7),
                    'music_enabled': self.settings.get('music_enabled', True),
                    'sfx_enabled': self.settings.get('sfx_enabled', True),
                    'theme': self.settings.get('theme', 'dark'),
                }
                
                success = self.game.save_manager.save_settings(settings_to_save)
                # if success:
                #     print("Settings đã được lưu")
                # else:
                #     print("Không thể lưu settings")
            
            # Cập nhật settings trong game object
            self.game.settings = self.settings
            
            return True
        except Exception as e:
            print(f"Lỗi khi lưu settings: {e}")
            return False
    
    def update(self):
        # Kiểm tra hover
        mouse_pos = pygame.mouse.get_pos()
        self.back_hover = self.back_button.collidepoint(mouse_pos)
        self.reset_hover = self.reset_button.collidepoint(mouse_pos)
        
        # Hover cho theme buttons
        for theme_btn in self.theme_buttons:
            theme_btn['hover'] = theme_btn['rect'].collidepoint(mouse_pos)
    
    def draw(self):
        # Nền từ theme
        self.screen.fill(self.theme_info['bg_color'])
        
        # Tiêu đề
        title = self.font_title.render("SETTINGS", True, self.theme_info['ui_text'])
        self.screen.blit(title, (300, 50))
        
        # 1. Âm nhạc
        music_text = self.font_normal.render("Music Volume:", True, self.theme_info['ui_accent'])
        self.screen.blit(music_text, (100, 150))
        
        # Vẽ slider music
        slider = self.sliders['music']
        pygame.draw.rect(self.screen, self.theme_info['ui_bg'], slider['rect'])
        pygame.draw.rect(self.screen, self.theme_info['ui_accent'], 
                        (slider['rect'].x, slider['rect'].y, 
                         slider['rect'].width * slider['value'], 
                         slider['rect'].height))
        
        # Giá trị % music
        value_text = self.font_small.render(f"{int(slider['value'] * 100)}%", True, self.theme_info['ui_text'])
        self.screen.blit(value_text, (515, 155))
        
        # Checkbox âm nhạc
        pygame.draw.rect(self.screen, self.theme_info['ui_text'], self.music_checkbox, 2)
        if self.settings.get('music_enabled', True):
            pygame.draw.rect(self.screen, (0, 255, 0), (self.music_checkbox.x+4, self.music_checkbox.y+4, 12, 12))
        #text checkbox music
        checkbox_text = self.font_small.render("Enabled", True, self.theme_info['ui_text'])
        self.screen.blit(checkbox_text, (600, 155))
        
        # 2. Âm thanh hiệu ứng
        sfx_text = self.font_normal.render("SFX Volume:", True, self.theme_info['ui_accent'])
        self.screen.blit(sfx_text, (100, 220))
        
        # Vẽ slider sfx
        slider = self.sliders['sfx']
        pygame.draw.rect(self.screen, self.theme_info['ui_bg'], slider['rect'])
        pygame.draw.rect(self.screen, self.theme_info['ui_accent'], 
                        (slider['rect'].x, slider['rect'].y, 
                         slider['rect'].width * slider['value'], 
                         slider['rect'].height))
        
        # giá trị % sfx
        value_text = self.font_small.render(f"{int(slider['value'] * 100)}%", True, self.theme_info['ui_text'])
        self.screen.blit(value_text, (515, 225))
        
        # Checkbox SFX
        pygame.draw.rect(self.screen, self.theme_info['ui_text'], self.sfx_checkbox, 2)
        if self.settings.get('sfx_enabled', True):
            pygame.draw.rect(self.screen, (0, 255, 0), (self.sfx_checkbox.x+4, self.sfx_checkbox.y+4, 12, 12))
        checkbox_text = self.font_small.render("Enabled", True, self.theme_info['ui_text'])
        self.screen.blit(checkbox_text, (600, 225))
        
        # 3. Theme selection
        theme_text = self.font_normal.render("Theme:", True, self.theme_info['ui_accent'])
        self.screen.blit(theme_text, (100, 290))
        
        for theme_btn in self.theme_buttons:
            # Màu nút
            if theme_btn.get('hover'):
                btn_color = self.theme_info['ui_accent']
            else:
                btn_color = self.theme_info['ui_bg']
            
            # Vẽ nút
            pygame.draw.rect(self.screen, btn_color, theme_btn['rect'], border_radius=5)
            pygame.draw.rect(self.screen, self.theme_info['ui_text'], theme_btn['rect'], 2, border_radius=5)
            
            # Dấu chọn nếu đang chọn
            if theme_btn['value'] == self.selected_theme:
                pygame.draw.rect(self.screen, self.theme_info['ui_accent'], 
                               (theme_btn['rect'].x+5, theme_btn['rect'].y+5, 
                                theme_btn['rect'].width-10, theme_btn['rect'].height-10), 3, border_radius=3)
            
            # Tên theme
            name_text = self.font_normal.render(theme_btn['name'], True, self.theme_info['ui_text'])
            text_rect = name_text.get_rect(center=theme_btn['rect'].center)
            self.screen.blit(name_text, text_rect)
        
        # 4. Nút Back
        back_color = self.theme_info['ui_accent'] if self.back_hover else self.theme_info['ui_bg']
        pygame.draw.rect(self.screen, back_color, self.back_button, border_radius=10)
        pygame.draw.rect(self.screen, self.theme_info['ui_text'], self.back_button, 2, border_radius=10)
        
        back_text = self.font_small.render("BACK", True, self.theme_info['ui_text'])
        back_rect = back_text.get_rect(center=self.back_button.center)
        self.screen.blit(back_text, back_rect)
        
        # 5. Nút Reset Data
        reset_color = self.theme_info['ui_accent'] if self.reset_hover else self.theme_info['ui_bg']
        pygame.draw.rect(self.screen, reset_color, self.reset_button, border_radius=10)
        pygame.draw.rect(self.screen, self.theme_info['ui_text'], self.reset_button, 2, border_radius=10)
        
        reset_text = self.font_small.render("RESET DATA", True, self.theme_info['ui_text'])
        reset_rect = reset_text.get_rect(center=self.reset_button.center)
        self.screen.blit(reset_text, reset_rect)
        
        # Theme preview
        preview_text = self.font_small.render(f"Current: {self.theme_info['name']}", 
                                            True, self.theme_info['ui_accent'])
        self.screen.blit(preview_text, (100, 350))
        
        # Hướng dẫn
        help_text = self.font_small.render("ESC: Back | Click to select", True, self.theme_info['ui_text'])
        self.screen.blit(help_text, (280, 570))
        
        # Hiển thị confirmation dialog
        if self.show_reset_confirmation:
            self.show_reset_confirmation_dialog()

    def show_reset_confirmation_dialog(self):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Popup
        popup_rect = pygame.Rect(200, 200, 400, 200)
        pygame.draw.rect(self.screen, self.theme_info['ui_bg'], popup_rect, border_radius=15)
        pygame.draw.rect(self.screen, self.theme_info['ui_text'], popup_rect, 2, border_radius=15)
        
        # Tiêu đề
        title = self.font_normal.render("RESET DATA?", True, (255, 100, 100))
        self.screen.blit(title, (350, 220))
        
        # Thông báo
        msg = self.font_small.render("This will delete all game progress!", True, self.theme_info['ui_text'])
        self.screen.blit(msg, (250, 270))
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Nút Yes
        yes_btn = pygame.Rect(250, 330, 80, 40)
        yes_hover = yes_btn.collidepoint(mouse_pos)
        yes_color = (255, 80, 80) if yes_hover else (200, 60, 60)
        pygame.draw.rect(self.screen, yes_color, yes_btn, border_radius=8)
        pygame.draw.rect(self.screen, self.theme_info['ui_text'], yes_btn, 2, border_radius=8)
        yes_text = self.font_small.render("YES", True, self.theme_info['ui_text'])
        self.screen.blit(yes_text, (yes_btn.centerx - 20, yes_btn.centery - 10))
        
        # Nút No
        no_btn = pygame.Rect(470, 330, 80, 40)
        no_hover = no_btn.collidepoint(mouse_pos)
        no_color = (100, 200, 100) if no_hover else (60, 160, 60)
        pygame.draw.rect(self.screen, no_color, no_btn, border_radius=8)
        pygame.draw.rect(self.screen, self.theme_info['ui_text'], no_btn, 2, border_radius=8)
        no_text = self.font_small.render("NO", True, self.theme_info['ui_text'])
        self.screen.blit(no_text, (no_btn.centerx - 15, no_btn.centery - 10))
        
        return yes_btn, no_btn
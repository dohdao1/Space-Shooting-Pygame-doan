import pygame
from .baseScreen import baseScreen
from config import *
from utils.map_color import *

class statsScreen(baseScreen):
    def __init__(self, game):
        super().__init__(game)
        
        # Lấy stats từ save_manager
        if hasattr(game, 'save_manager'):
            self.stats = game.save_manager.load_stats()
        else:
            # không có data thì tạo
            self.stats = {
                'high_score': 0,
                'total_games': 0,
                'total_play_time': 0,
                'total_kills': 0,
                'total_deaths': 0,
                'game_history': [],
                'coin': 0
            }

        # Tải settings từ SecureSaveManager và map theme
        if hasattr(game, 'save_manager'):
            raw_settings = game.save_manager.load_settings()
            self.settings = update_settings_with_theme(raw_settings)
        else:
            # Fallback
            from utils.map_color import get_default_settings
            self.settings = get_default_settings()
                
        # Theme hiện tại
        self.selected_theme = self.settings.get('theme', 'dark')
        self.theme_info = get_theme(self.selected_theme)
        
        # Font
        self.font_title = pygame.font.SysFont('arial', 48, bold=True)
        self.font_large = pygame.font.SysFont('arial', 36, bold=True)
        self.font_normal = pygame.font.SysFont('arial', 28)
        self.font_small = pygame.font.SysFont('arial', 20)
        
        # Nút Back và Reset
        self.back_button = pygame.Rect(200, 500, 150, 50)
        self.reset_button = pygame.Rect(450, 500, 150, 50)
        self.back_hover = False
        self.reset_hover = False
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.switch_to("main_menu")
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.back_button.collidepoint(mouse_pos):
                        self.switch_to("main_menu")
                    elif self.reset_button.collidepoint(mouse_pos):
                        # Reset stats (giữ coin)
                        if hasattr(self.game, 'save_manager'):
                            # Lưu coin hiện tại
                            current_coin = self.stats.get('coin', 0)
                            
                            # Tạo stats mới
                            new_stats = {
                                'high_score': 0,
                                'total_games': 0,
                                'total_play_time': 0,
                                'total_kills': 0,
                                'total_deaths': 0,
                                'game_history': [],
                                'coin': current_coin  # Giữ coin
                            }
                            
                            # Lưu lại
                            self.game.save_manager.save_stats(new_stats)
                            self.stats = new_stats
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.back_hover = self.back_button.collidepoint(mouse_pos)
        self.reset_hover = self.reset_button.collidepoint(mouse_pos)
    
    def draw(self):
        # Nền từ theme
        self.screen.fill(self.theme_info['bg_color'])
        
        # Tiêu đề
        title = self.font_title.render("GAME STATS", True, self.theme_info['ui_accent'])
        self.screen.blit(title, (280, 20))
        
        y = 80
        
        # High score và coin
        hs_text = self.font_large.render(f"HIGH SCORE: {self.stats.get('high_score', 0)}", True, (100, 255, 100))
        self.screen.blit(hs_text, (100, y))
        
        coin_text = self.font_large.render(f"COINS: {self.stats.get('coin', 0)}", True, (255, 215, 0))
        self.screen.blit(coin_text, (500, y))
        y += 50
        
        # Thống kê tổng quan
        stats_title = self.font_normal.render("OVERALL STATS", True, self.theme_info['ui_accent'])
        self.screen.blit(stats_title, (100, y))
        y += 40
        
        total_stats = [
            f"Total Games: {self.stats.get('total_games', 0)}",
            f"Total Play Time: {int(self.stats.get('total_play_time', 0))}s",
            f"Total Kills: {self.stats.get('total_kills', 0)}",
            f"Total Deaths: {self.stats.get('total_deaths', 0)}",
            f"K/D Ratio: {self.calculate_kd_ratio()}",
        ]
        
        for stat in total_stats:
            stat_text = self.font_normal.render(stat, True, self.theme_info['ui_text'])
            self.screen.blit(stat_text, (120, y))
            y += 35
        
        y += 20
        
        # Lịch sử game gần đây
        history_title = self.font_normal.render("RECENT GAMES", True, self.theme_info['ui_accent'])
        self.screen.blit(history_title, (100, y))
        y += 40
        
        history = self.stats.get('game_history', [])
        
        if not history:
            no_history = self.font_small.render("No game history yet", True, self.theme_info['ui_text'])
            self.screen.blit(no_history, (120, y))
            y += 30
        else:
            # Hiển thị 5 game gần nhất
            for i, game in enumerate(history[:5]):
                game_date = game.get('date', 'N/A')
                game_score = game.get('score', 0)
                game_time = game.get('play_time', 0)
                
                game_text = self.font_small.render(
                    f"{game_date} - Score: {game_score} - Time: {int(game_time)}s",
                    True, self.theme_info['ui_text']
                )
                self.screen.blit(game_text, (120, y))
                y += 25
        
        # Thống kê chi tiết bên phải
        right_y = 130
        
        # hiển thị kda
        kd_title = self.font_normal.render("KILL/DEATH BREAKDOWN", True, self.theme_info['ui_accent'])
        self.screen.blit(kd_title, (450, right_y))
        right_y += 40
        
        if self.stats.get('total_games', 0) > 0:
            avg_kills = self.stats.get('total_kills', 0) / self.stats.get('total_games', 1)
            avg_deaths = self.stats.get('total_deaths', 0) / self.stats.get('total_games', 1)
            
            kd_details = [
                f"Avg Kills/Game: {avg_kills:.1f}",
                f"Avg Deaths/Game: {avg_deaths:.1f}",
                f"Best Score: {self.stats.get('high_score', 0)}",
            ]
        else:
            kd_details = ["Play your first game to see stats!"]
        
        for detail in kd_details:
            detail_text = self.font_small.render(detail, True, self.theme_info['ui_text'])
            self.screen.blit(detail_text, (470, right_y))
            right_y += 30
        right_y += 20
        
        # text
        ach_title = self.font_normal.render("ACHIEVEMENTS", True, self.theme_info['ui_accent'])
        self.screen.blit(ach_title, (450, right_y))
        right_y += 40
        
        # tính thành tựu
        achievements = self.calculate_achievements()
        for ach_name, progress in achievements.items():
            ach_text = self.font_small.render(f"{ach_name}: {progress}", True, self.theme_info['ui_text'])
            self.screen.blit(ach_text, (470, right_y))
            right_y += 25
        
        # Nút Back
        back_color = self.theme_info['ui_accent'] if self.back_hover else self.theme_info['ui_bg']
        pygame.draw.rect(self.screen, back_color, self.back_button, border_radius=10)
        pygame.draw.rect(self.screen, self.theme_info['ui_text'], self.back_button, 2, border_radius=10)
        
        back_text = self.font_small.render("BACK", True, self.theme_info['ui_text'])
        back_rect = back_text.get_rect(center=self.back_button.center)
        self.screen.blit(back_text, back_rect)
        
        # Nút Reset Stats (giữ coin)
        reset_color = self.theme_info['ui_accent'] if self.reset_hover else self.theme_info['ui_bg']
        pygame.draw.rect(self.screen, reset_color, self.reset_button, border_radius=10)
        pygame.draw.rect(self.screen, self.theme_info['ui_text'], self.reset_button, 2, border_radius=10)
        
        reset_text = self.font_small.render("RESET STATS", True, self.theme_info['ui_text'])
        reset_rect = reset_text.get_rect(center=self.reset_button.center)
        self.screen.blit(reset_text, reset_rect)
        
        # text Hướng dẫn
        help_text = self.font_small.render("ESC: Back to Menu | Click buttons to interact", True, self.theme_info['ui_text'])
        self.screen.blit(help_text, (220, 570))
    
    # tính kda
    def calculate_kd_ratio(self):
        kills = self.stats.get('total_kills', 0)
        deaths = self.stats.get('total_deaths', 0)
        
        if deaths == 0:
            return "∞" if kills > 0 else "0.00"
        
        return f"{kills/deaths:.2f}"
    
    # tính toán thành tựu, AI viết ảo vl
    def calculate_achievements(self):
        achievements = {}
        
        high_score = self.stats.get('high_score', 0)
        total_games = self.stats.get('total_games', 0)
        total_kills = self.stats.get('total_kills', 0)
        
        # Số điểm
        if high_score >= 1000:
            achievements["Score Master"] = "⭐⭐⭐"
        elif high_score >= 500:
            achievements["Score Expert"] = "⭐⭐"
        elif high_score >= 100:
            achievements["Score Beginner"] = "⭐"
        else:
            achievements["Score Beginner"] = "0/100"
        
        # só lượng game chơi
        if total_games >= 50:
            achievements["Veteran Player"] = "⭐⭐⭐"
        elif total_games >= 20:
            achievements["Regular Player"] = "⭐⭐"
        elif total_games >= 5:
            achievements["Casual Player"] = "⭐"
        else:
            achievements["Casual Player"] = f"{total_games}/5"
        
        # Tổng lượn bắn hạ
        if total_kills >= 1000:
            achievements["Killing Machine"] = "⭐⭐⭐"
        elif total_kills >= 500:
            achievements["Skilled Hunter"] = "⭐⭐"
        elif total_kills >= 100:
            achievements["Novice Hunter"] = "⭐"
        else:
            achievements["Novice Hunter"] = f"{total_kills}/100"
        
        # Tính coin sưu tập
        coin = self.stats.get('coin', 0)
        if coin >= 10000:
            achievements["Millionaire"] = "💰💰💰"
        elif coin >= 5000:
            achievements["Rich"] = "💰💰"
        elif coin >= 1000:
            achievements["Wealthy"] = "💰"
        else:
            achievements["Wealthy"] = f"{coin}/1000"
        
        return achievements
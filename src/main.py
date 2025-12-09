#file hoạt động chính của game
import pygame, random, math
import sys, os

from config import *
from scenes import mainMenu, gameScreen, pauseMenu, gameOver, settingScreen, statsScreen
from scenes import mainMenu, gameScreen, pauseMenu, gameOver, shopScreen
from managers import screenManager, SecureSaveManager, audioManager
from scenes.shopScreen import shopScreen

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Shooter")
        
        # khai báo quản lý các màn hình Screen manager
        self.screen_manager = screenManager(self)

        self.save_manager = SecureSaveManager(self)
        # load save, nếu chưa có ở máy thì tạo
        self.settings = self.save_manager.load_settings()
        self.stats = self.save_manager.load_stats()

        self.audio_manager = audioManager(self.save_manager)
        
        # Đăng ký tất cả screens
        self.screen_manager.register_screen("main_menu", mainMenu)
        self.screen_manager.register_screen("game", gameScreen)
        self.screen_manager.register_screen("shop", shopScreen)
        self.screen_manager.register_screen("pause", pauseMenu)
        self.screen_manager.register_screen("game_over", gameOver)
        self.screen_manager.register_screen("settings", settingScreen)
        self.screen_manager.register_screen("stats", statsScreen)
        
        # Bắt đầu với main menu
        self.screen_manager.switch_to("main_menu")

        # bật nhạc nền luôn
        self.audio_manager.play_music("menu")
        
        # Game state
        self.running = True
        self.clock = pygame.time.Clock()

    def handle_button_click(self, button_action):
        # Phát âm thanh SFX khi click
        if hasattr(self, 'audio_manager'):
            self.audio_manager.play_sound("shooter_sfx", volume_scale=0.3)
        
        # Trả về action để xử lý tiếp
        return button_action
    
    def run(self):
        while self.running:
            # Lấy tất cả events
            events = pygame.event.get()
            
            # Xử lý quit event
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            
            # gọi các phương thức từ quản lý màn hình
            self.screen_manager.handle_events(events)
            self.screen_manager.update()
            self.screen_manager.draw()
            
            # Cập nhật màn hình liên tục
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def quit(self):
        self.running = False
        self.screen_manager.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
#file hoạt động chính của game
import pygame, random, math
import sys, os

from config import *
from scenes import mainMenu, gameScreen, pauseMenu, gameOver
from managers.screenManager import screenManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Shooter")
        
        # khai báo quản lý các màn hình Screen manager
        self.screen_manager = screenManager(self)
        
        # Đăng ký tất cả screens
        self.screen_manager.register_screen("main_menu", mainMenu)
        self.screen_manager.register_screen("game", gameScreen)
        self.screen_manager.register_screen("pause", pauseMenu)
        self.screen_manager.register_screen("game_over", gameOver)
        
        # Bắt đầu với main menu
        self.screen_manager.switch_to("main_menu")
        
        # Game state
        self.running = True
        self.clock = pygame.time.Clock()
    
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
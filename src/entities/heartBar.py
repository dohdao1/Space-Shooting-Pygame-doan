# thanh máu người chơi
import pygame

class HeartBar:
    def __init__(self, player, width=120, height=15):
        self.player = player
        self.width = width
        self.height = height

    def draw(self, screen):
        max_hp = self.player.max_health
        hp = self.player.health

        # viền
        pygame.draw.rect(screen, (255, 255, 255), (10, 10, self.width, self.height), 2)

        # HP còn lại
        ratio = hp / max_hp
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, self.width * ratio, self.height))

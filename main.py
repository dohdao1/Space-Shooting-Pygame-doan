import pygame, random, math
import init

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Particle System Example")

#mauf
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PARTICLE_COLOR = (255, 100, 100)
BLUE = (100, 100, 255)

#nhac
pygame.mixer.init()
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)  # Play music in a loop


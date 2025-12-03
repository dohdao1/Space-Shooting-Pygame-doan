#file hoạt động chính của game
import pygame, random, math
import sys, os
from config import *

pygame.init()       # khởi tạo game
screen = pygame.display.set_mode((800, 600))    # quy định chiều dài chiều rộng game
pygame.display.set_caption("Space Shooter")

title_font = pygame.font.SysFont('arial', 64, bold=True)
normal_font = pygame.font.SysFont('arial', 36)

# Tạo chữ
title_text = title_font.render("SPACE SHOOTER", True, BLUE)
subtitle_text = normal_font.render("Press ESC to exit", True, WHITE)

# Vòng lặp game
clock = pygame.time.Clock()
running = True

while running:
    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Cập nhật màn hình
    pygame.display.flip()
    
    # Giới hạn FPS
    clock.tick(60)

# Kết thúc
pygame.quit()
print("\nGame đã thoát!")
sys.exit()
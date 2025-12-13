# ⭐ CLASS HIỆU ỨNG VỠ KHIÊN
import pygame
import random
import math


class ShieldBreakParticle(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y, color=(50, 200, 255)):
        super().__init__()
        self.color = color
        self.radius = random.randint(3, 7)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(center_x, center_y))
        
        # Tốc độ và hướng di chuyển ngẫu nhiên
        angle = random.uniform(0, 360)
        self.speed = random.uniform(2, 5)
        self.vel_x = self.speed * math.cos(math.radians(angle))
        self.vel_y = self.speed * math.sin(math.radians(angle))
        
        self.lifetime = random.randint(30, 60) # Tồn tại 30-60 frame
        self.current_frame = 0

    def update(self, dt):
        # Giảm opacity (hoặc kích thước) dần dần
        self.radius -= 0.1*dt*60  
        if self.radius <= 0:
            self.kill()
            return
            
        # Cập nhật vị trí
        self.rect.x += self.vel_x*dt*60
        self.rect.y += self.vel_y*60
        
        # Tự hủy sau khi hết thời gian
        self.lifetime -= (dt*1000)
        if self.lifetime <= 0:
            self.kill()

# gamescreen.py - thêm vào đầu file

class Shockwave(pygame.sprite.Sprite):
    def __init__(self, center_pos, duration=500):
        super().__init__()
        # Vị trí tâm điểm vụ nổ
        self.center_x, self.center_y = center_pos
        
        self.max_radius = 700  # Bán kính tối đa của sóng
        self.radius = 0
        
        self.duration = duration # Thời gian tồn tại của sóng (ms)
        self.start_time = pygame.time.get_ticks()

        # Hình ảnh rỗng ban đầu, sẽ được vẽ lại liên tục
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=center_pos)

    def update(self, dt):
        now = pygame.time.get_ticks()
        elapsed_time = now - self.start_time

        # Tính phần trăm đã trôi qua (0.0 đến 1.0)
        progress = elapsed_time / self.duration

        if progress >= 1.0:
            self.kill() # Tự hủy khi hết thời gian
            return

        # Tính toán bán kính và độ trong suốt
        # Bán kính tăng dần theo thời gian
        self.radius = int(self.max_radius * progress)
        
        # Độ trong suốt giảm dần (bắt đầu từ 255 - hoàn toàn không trong suốt)
        alpha = int(255 * (1 - progress))
        
        # --- Vẽ lại hình ảnh (vòng tròn) ---
        
        # Kích thước Surface cần đủ lớn để chứa vòng tròn hiện tại
        size = self.radius * 2
        
        # Tạo Surface mới với kênh Alpha (độ trong suốt)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Màu của sóng: Vàng (hoặc màu trắng)
        color = (255, 200, 50, alpha) # Thêm kênh alpha vào màu

        # Vẽ vòng tròn đặc (hoặc vòng tròn rỗng)
        # Vẽ vòng tròn đặc (solid circle)
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius) 

        # Cập nhật rect để tâm của nó luôn ở vị trí ban đầu
        self.rect = self.image.get_rect(center=(self.center_x, self.center_y))
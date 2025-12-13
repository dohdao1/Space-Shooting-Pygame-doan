import pygame
from .baseScreen import baseScreen

class shopScreen(baseScreen):
    def __init__(self, game):
        super().__init__(game)

        self.font_title = pygame.font.SysFont("arial", 60, bold=True)
        self.font_item = pygame.font.SysFont("arial", 28)
        self.font_small = pygame.font.SysFont("arial", 24)

        self.skin_manager = game.skin_manager

        # Load ảnh skin
        self.skin_images = {}
        self.load_skin_images()

        # Layout grid
        self.start_x = 40
        self.start_y = 150
        self.gap_x = 260
        self.gap_y = 220
        self.columns = 3  

        # Nút Back
        self.back_rect = pygame.Rect(20, 20, 120, 50)

        # Thông báo
        self.message = ""
        self.message_timer = 0

    # ----------------------------------------------------
    def load_skin_images(self):
        target_w = 110
        target_h = 110

         # Lấy tất cả skins từ skin_manager
        skins_data = self.skin_manager.get_all_skins()
        
        for skin in skins_data:
            img = pygame.image.load(skin["path"]).convert_alpha()
            img = pygame.transform.smoothscale(img, (target_w, target_h))
            self.skin_images[skin["name"]] = img

    # ----------------------------------------------------
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.switch_to("main_menu")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse = pygame.mouse.get_pos()

                    # Back
                    if self.back_rect.collidepoint(mouse):
                        self.switch_to("main_menu")

                    # Click skin
                    clicked_skin = self.detect_skin_click(mouse)
                    if clicked_skin:
                        self.buy_or_select(clicked_skin)

    # ----------------------------------------------------
    def detect_skin_click(self, mouse_pos):
        # Lấy danh sách skins
        skins = self.skin_manager.get_all_skins()
        
        for index, skin in enumerate(skins):
            col = index % self.columns
            row = index // self.columns

            x = self.start_x + col * self.gap_x
            y = self.start_y + row * self.gap_y

            rect = pygame.Rect(x, y, 200, 200)
            if rect.collidepoint(mouse_pos):
                return skin["name"]
                
        return None

    # ----------------------------------------------------
    def buy_or_select(self, skin_name):
        # Lấy thông tin skin
        skin_info = self.skin_manager.get_skin_info(skin_name)
        if not skin_info:
            self.message = "Skin not found!"
            self.message_timer = pygame.time.get_ticks()
            return
        
        # Kiểm tra đã sở hữu chưa
        if skin_info["owned"]:
            # Đã sở hữu -> chọn
            result = self.skin_manager.select_skin(skin_name)
            if result == "selected":
                self.message = f"Selected {skin_name}"
            else:
                self.message = f"Failed to select {skin_name}"
        else:
            # Chưa sở hữu -> mua
            result = self.skin_manager.buy_skin(skin_name)
            if result == "bought":
                self.message = f"Bought {skin_name}!"
            elif result == "no_coin":
                self.message = "Not enough coin!"
            elif result == "owned":
                self.message = "Already owned!"
            else:
                self.message = f"Error: {result}"
        
        self.message_timer = pygame.time.get_ticks()

    # ----------------------------------------------------
    def draw(self):
        self.screen.fill((25, 25, 45))

        # Title
        title = self.font_title.render("SKIN SHOP", True, (120, 200, 255))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 60))

        # Gold display
        gold_text = self.font_item.render(f"Coins: {self.skin_manager.coin}", True, (255, 230, 120))
        self.screen.blit(gold_text, (20, 110))

        # Back button
        pygame.draw.rect(self.screen, (70, 70, 100), self.back_rect, border_radius=10)
        pygame.draw.rect(self.screen, (200, 200, 200), self.back_rect, 2, border_radius=10)
        back_text = self.font_item.render("BACK", True, (255, 255, 255))
        self.screen.blit(back_text, back_text.get_rect(center=self.back_rect.center))

        # Vẽ danh sách skin
        skins = self.skin_manager.get_all_skins()
        
        for index, skin in enumerate(skins):
            col = index % self.columns
            row = index // self.columns

            x = self.start_x + col * self.gap_x
            y = self.start_y + row * self.gap_y

            rect = pygame.Rect(x, y, 200, 200)
            
            # Kiểm tra không đủ coin
            not_affordable = (not skin["owned"] and not self.skin_manager.can_afford_skin(skin["name"]))
            
            # Vẽ nền
            if skin["name"] == self.skin_manager.selected_skin:
                pygame.draw.rect(self.screen, (80, 120, 170), rect, border_radius=15)
            else:
                if not_affordable:
                    # Màu tối hơn cho skin không đủ coin
                    pygame.draw.rect(self.screen, (30, 30, 50), rect, border_radius=15)
                else:
                    pygame.draw.rect(self.screen, (40, 40, 70), rect, border_radius=15)

            pygame.draw.rect(self.screen, (200, 200, 200), rect, 2, border_radius=15)
            
            # Ảnh - thêm hiệu ứng mờ nếu không đủ coin
            img = self.skin_images[skin["name"]]
            
            if not_affordable:
                # Tạo bản copy mờ của ảnh
                img_copy = img.copy()
                img_copy.set_alpha(150)  # Giảm độ trong suốt
                self.screen.blit(img_copy, img.get_rect(center=(x + 100, y + 70)))
                
                # Vẽ lớp overlay đỏ nhẹ
                overlay = pygame.Surface((200, 200), pygame.SRCALPHA)
                overlay.fill((255, 50, 50, 30))  # Đỏ nhẹ
                self.screen.blit(overlay, (x, y))
            else:
                self.screen.blit(img, img.get_rect(center=(x + 100, y + 70)))

            # Tên skin
            label = self.font_small.render(skin["name"], True, (255, 255, 255))
            self.screen.blit(label, (x + 20, y + 135))

            # Trạng thái với màu sắc rõ ràng hơn
            if skin["owned"]:
                if skin["name"] == self.skin_manager.selected_skin:
                    status = self.font_small.render(" Selected ", True, (120, 255, 120))
                else:
                    status = self.font_small.render("Click to select", True, (180, 255, 180))
            else:
                if not_affordable:
                    # Màu đỏ rõ ràng cho không đủ coin
                    status = self.font_small.render(f"Need {skin['price']} coin", True, (255, 100, 100))
                    # Thêm icon cảnh báo
                    warning = self.font_small.render(" /!\ ", True, (255, 200, 50))
                    self.screen.blit(warning, (x + 160, y + 165))
                else:
                    # Màu vàng cho có thể mua
                    status = self.font_small.render(f"Buy: {skin['price']} coin", True, (255, 215, 0))

            self.screen.blit(status, (x + 20, y + 165))

        # Hiện thông báo (2 giây)
        if self.message:
            if pygame.time.get_ticks() - self.message_timer < 2000:
                msg = self.font_item.render(self.message, True, (255, 200, 0))
                self.screen.blit(msg, (self.screen.get_width() // 2 - msg.get_width() // 2, 720))
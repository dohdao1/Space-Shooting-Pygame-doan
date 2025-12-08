import pygame
from .baseScreen import baseScreen
from managers.skinManager import SkinManager

class shopScreen(baseScreen):
    def __init__(self, game):
        super().__init__(game)

        self.font_title = pygame.font.SysFont("arial", 60, bold=True)
        self.font_item = pygame.font.SysFont("arial", 28)
        self.font_small = pygame.font.SysFont("arial", 24)

        self.skin_manager = SkinManager()

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

        for name, skin in self.skin_manager.skins.items():
            img = pygame.image.load(skin["path"]).convert_alpha()
            img = pygame.transform.smoothscale(img, (target_w, target_h))
            self.skin_images[name] = img

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
        index = 0
        for name in self.skin_manager.skins:

            col = index % self.columns
            row = index // self.columns

            x = self.start_x + col * self.gap_x
            y = self.start_y + row * self.gap_y

            rect = pygame.Rect(x, y, 200, 200)
            if rect.collidepoint(mouse_pos):
                return name

            index += 1
        return None

    # ----------------------------------------------------
    def buy_or_select(self, skin_name):
        skin = self.skin_manager.skins[skin_name]

        if skin_name in self.skin_manager.owned_skins:
            self.skin_manager.select_skin(skin_name)
            self.message = f"Selected {skin_name}"
        else:
            result = self.skin_manager.buy_skin(skin_name)

            if result == "no_gold":
                self.message = "Not enough gold!"
            elif result == "bought":
                self.message = f"Bought {skin_name}!"
            elif result == "owned":
                self.message = "Already owned!"

        self.message_timer = pygame.time.get_ticks()

    # ----------------------------------------------------
    def draw(self):
        self.screen.fill((25, 25, 45))

        # Title
        title = self.font_title.render("SKIN SHOP", True, (120, 200, 255))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 60))

        # Gold display
        gold_text = self.font_item.render(f"Gold: {self.skin_manager.gold}", True, (255, 230, 120))
        self.screen.blit(gold_text, (20, 110))

        # Back button
        pygame.draw.rect(self.screen, (70, 70, 100), self.back_rect, border_radius=10)
        pygame.draw.rect(self.screen, (200, 200, 200), self.back_rect, 2, border_radius=10)
        back_text = self.font_item.render("BACK", True, (255, 255, 255))
        self.screen.blit(back_text, back_text.get_rect(center=self.back_rect.center))

        # Vẽ danh sách skin
        index = 0
        for name, skin in self.skin_manager.skins.items():

            col = index % self.columns
            row = index // self.columns

            x = self.start_x + col * self.gap_x
            y = self.start_y + row * self.gap_y

            rect = pygame.Rect(x, y, 200, 200)

            # Highlight Selected
            if name == self.skin_manager.selected_skin:
                pygame.draw.rect(self.screen, (80, 120, 170), rect, border_radius=15)
            else:
                pygame.draw.rect(self.screen, (40, 40, 70), rect, border_radius=15)

            pygame.draw.rect(self.screen, (200, 200, 200), rect, 2, border_radius=15)

            # Ảnh
            img = self.skin_images[name]
            img_rect = img.get_rect(center=(x + 100, y + 70))
            self.screen.blit(img, img_rect)

            # Tên skin
            label = self.font_small.render(name, True, (255, 255, 255))
            self.screen.blit(label, (x + 20, y + 135))

            # Trạng thái
            if name in self.skin_manager.owned_skins:
                if name == self.skin_manager.selected_skin:
                    status = self.font_small.render("Selected", True, (120, 255, 120))
                else:
                    status = self.font_small.render("Click to select", True, (180, 255, 180))
            else:
                status = self.font_small.render(f"Buy: {skin['price']}", True, (255, 180, 120))

            self.screen.blit(status, (x + 20, y + 165))

            index += 1

        # Hiện thông báo (2 giây)
        if self.message:
            if pygame.time.get_ticks() - self.message_timer < 2000:
                msg = self.font_item.render(self.message, True, (255, 200, 0))
                self.screen.blit(msg, (self.screen.get_width() // 2 - msg.get_width() // 2, 720))

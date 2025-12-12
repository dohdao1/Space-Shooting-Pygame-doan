import pygame

class Item(pygame.sprite.Sprite):
    ICONS = {
        "double_bullet": "assets/images/items/double.png",
        "triple_bullet": "assets/images/items/triple.png",
        "quad_bullet": "assets/images/items/quad.png",
        "six_bullet": "assets/images/items/six.png",
        "shield": "assets/images/items/shield.png",
        "life": "assets/images/items/life.png",
        "bomb": "assets/images/items/bomb.png"
    }
    ICON_SIZE = 40  


    def __init__(self, x, y, item_type):
        super().__init__()
        self.type = item_type

        img = Item.ICONS.get(item_type)
        if img:
            self.image = pygame.image.load(img).convert_alpha()
            self.image = pygame.transform.smoothscale(
                self.image,
                (Item.ICON_SIZE, Item.ICON_SIZE)
            )

        else:
            self.image = pygame.Surface((25, 25))
            self.image.fill((255, 255, 0))

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 150  # rơi xuống 150px/s

    def update(self, dt):
        self.rect.y += self.speed * dt
        if self.rect.top > 800:
            self.kill()

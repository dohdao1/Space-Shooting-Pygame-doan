import random
from entities.item import Item

class ItemDropper:
    def __init__(self, item_group):
        self.item_group = item_group

        # Tỉ lệ rơi (có thể chỉnh)
        self.drop_table = {
            "double_bullet": 0.1,
            "triple_bullet": 0.05,
            "quad_bullet":   0.03,
            "six_bullet":    0.02,
            "shield":        0.08,
            "life":          0.05,
            "bomb":          0.07
        }

    def try_drop(self, x, y):
        for item_type, chance in self.drop_table.items():
            if random.random() < chance:
                item = Item(x, y, item_type)
                self.item_group.add(item)
                return  # chỉ rơi 1 món

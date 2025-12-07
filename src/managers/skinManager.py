import json, os

SAVE_PATH = "src/data/save.json"

class SkinManager:
    def __init__(self):
        self.skins = {
            "default": {
                "name": "default",
                "path": "assets/images/player/player.png",
                "price": 0,
                "owned": True
            },
            "sea_eagle": {
                "name": "sea_eagle",
                "path": "assets/images/player/sea_eagle.png",
                "price": 200,
                "owned": False
            },
            "black_iron": {
                "name": "black_iron",
                "path": "assets/images/player/black_iron.png",
                "price": 300,
                "owned": False
            },
            "silver_wing": {
                "name": "silver_wing",
                "path": "assets/images/player/silver_wing.png",
                "price": 400,
                "owned": False
            },
            "chaos_phantom": {
                "name": "chaos_phantom",
                "path": "assets/images/player/chaos_phantom.png",
                "price": 500,
                "owned": False
            },
            "leviathan_omega": {
                "name": "leviathan_omega",
                "path": "assets/images/player/leviathan_omega.png",
                "price": 600,
                "owned": False
            }
        }

        self.load()

    def load(self):
        if not os.path.exists(SAVE_PATH):
            default_data = {
                "gold": 0,
                "owned_skins": ["default"],
                "selected_skin": "default"
            }
            with open(SAVE_PATH, "w") as f:
                json.dump(default_data, f, indent=4)

        with open(SAVE_PATH) as f:
            data = json.load(f)

        self.gold = data["gold"]
        self.owned_skins = data["owned_skins"]
        self.selected_skin = data["selected_skin"]

    def save(self):
        data = {
            "gold": self.gold,
            "owned_skins": self.owned_skins,
            "selected_skin": self.selected_skin
        }
        with open(SAVE_PATH, "w") as f:
            json.dump(data, f, indent=4)

    def buy_skin(self, skin_name):
        price = self.skins[skin_name]["price"]

        if skin_name in self.owned_skins:
            return "owned"

        if self.gold < price:
            return "no_gold"

        self.gold -= price
        self.owned_skins.append(skin_name)
        self.save()
        return "bought"

    def select_skin(self, skin_name):
        if skin_name not in self.owned_skins:
            return "not_owned"

        self.selected_skin = skin_name
        self.save()
        return "selected"

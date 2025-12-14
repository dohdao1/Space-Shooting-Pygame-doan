class SkinManager:
    def __init__(self, save_manager):
        self.save_manager = save_manager
        self.skins = {}
        self.owned_skins = []
        self.selected_skin = "default"
        self.coin = 0
        
        # Tải dữ liệu
        self.load()

    def load(self):
        if not self.save_manager:
            self._load_default_skins()
            return
        
        try:
            # Load từ spaces system
            spaces = self.save_manager.load_spaces()
            self.owned_skins = spaces.get('unlocked', ['default'])
            self.selected_skin = spaces.get('current', 'default')
            
            # Load coin từ stats
            stats = self.save_manager.load_stats()
            self.coin = stats.get('coin', 0)
            
            # Định nghĩa skins
            self.skins = {
                "default": {
                    "name": "default",
                    "path": "assets/images/player/player.png",
                    "price": 0,
                    "owned": "default" in self.owned_skins
                },
                "sea_eagle": {
                    "name": "sea_eagle",
                    "path": "assets/images/player/sea_eagle.png",
                    "price": 200,
                    "owned": "sea_eagle" in self.owned_skins
                },
                "black_iron": {
                    "name": "black_iron",
                    "path": "assets/images/player/black_iron.png",
                    "price": 300,
                    "owned": "black_iron" in self.owned_skins
                },
                "silver_wing": {
                    "name": "silver_wing",
                    "path": "assets/images/player/silver_wing.png",
                    "price": 400,
                    "owned": "silver_wing" in self.owned_skins
                },
                "chaos_phantom": {
                    "name": "chaos_phantom",
                    "path": "assets/images/player/chaos_phantom.png",
                    "price": 500,
                    "owned": "chaos_phantom" in self.owned_skins
                },
                "leviathan_omega": {
                    "name": "leviathan_omega",
                    "path": "assets/images/player/leviathan_omega.png",
                    "price": 600,
                    "owned": "leviathan_omega" in self.owned_skins
                }
            }
                        
        except Exception as e:
            print(f"Lỗi khi tải skins: {e}")
            self._load_default_skins()

    # laod skin mặc định
    def _load_default_skins(self):
        self.skins = {
            "default": {"name": "default", "path": "../assets/images/player/player.png", "price": 0, "owned": True},
            "sea_eagle": {"name": "sea_eagle", "path": "../assets/images/player/sea_eagle.png", "price": 200, "owned": False},
            "black_iron": {"name": "black_iron", "path": "../assets/images/player/black_iron.png", "price": 300, "owned": False},
            "silver_wing": {"name": "silver_wing", "path": "../assets/images/player/silver_wing.png", "price": 400, "owned": False},
            "chaos_phantom": {"name": "chaos_phantom", "path": "../assets/images/player/chaos_phantom.png", "price": 500, "owned": False},
            "leviathan_omega": {"name": "leviathan_omega", "path": "../assets/images/player/leviathan_omega.png", "price": 600, "owned": False}
        }
        self.owned_skins = ["default"]
        self.selected_skin = "default"
        self.coin = 0
    
    # mua skin
    def buy_skin(self, skin_name):
        if not self.save_manager:
            return "no_save_manager"
        
        if skin_name in self.owned_skins:
            return "owned"
        
        if skin_name not in self.skins:
            return "not_found"
        
        price = self.skins[skin_name]["price"]
        
        # Dùng unlock_space của save manager
        success = self.save_manager.unlock_space(skin_name, price)
        
        if success:
            # Cập nhật local data
            self.owned_skins.append(skin_name)
            self.skins[skin_name]["owned"] = True
            self.coin -= price
            return "bought"
        else:
            return "no_coin"
    
    # chọn skin
    def select_skin(self, skin_name):
        if not self.save_manager:
            return "no_save_manager"
        
        if skin_name not in self.owned_skins:
            return "not_owned"
        
        success = self.save_manager.set_current_space(skin_name)
        
        if success:
            self.selected_skin = skin_name
            return "selected"
        else:
            return "failed"
    
    # ========== Các phương thức cần cho shopScreen ==========
    # lấy dường dãn 
    def get_skin_path(self, skin_name=None):
        if skin_name is None:
            skin_name = self.selected_skin
        
        return self.skins.get(skin_name, self.skins["default"])["path"]
    
    # thông tin skin để hiển thị
    def get_skin_info(self, skin_name):
        if skin_name in self.skins:
            info = self.skins[skin_name].copy()
            info["is_owned"] = (skin_name in self.owned_skins)
            info["is_selected"] = (skin_name == self.selected_skin)
            info["can_afford"] = (self.coin >= info["price"])
            return info
        return None
    
    # lấy tất cả, để vẽ
    def get_all_skins(self):
        return list(self.skins.values())
    
    # kiểm tra mua
    def can_afford_skin(self, skin_name):
        if skin_name not in self.skins:
            return False
        return self.coin >= self.skins[skin_name]["price"]
    
    # load lại
    def refresh(self):
        self.load()
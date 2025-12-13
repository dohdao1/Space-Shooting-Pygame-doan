# quản lý màn hinh game
class screenManager:
    def __init__(self, game):
        self.game = game
        self.screens = {}  # Dictionary chứa tất cả screens
        self.current_screen = None
        self.previous_screen = None  # Lưu scene trước đó
    
    # đăng ký 1 screen mới, dùng lúc khởi tạo
    def register_screen(self, name, screen_class):
        self.screens[name] = screen_class(self.game)
        # print(f"Đăng ký screen: {name}")
    
    # chuyển màn hình
    def switch_to(self, screen_name, data=None):
        if screen_name not in self.screens:
            # print(f"ERROR: Không tìm dc '{screen_name}'!")
            return
        
        # Nếu chuyển về game, reset game state
        if screen_name == "game" and hasattr(self.screens[screen_name], 'reset_game_state'):
            # Chỉ reset nếu đang từ main menu vào, không phải từ pause
            if not (self.current_screen == "pause" and data is None):
                # data thường là score khi từ game_over vào
                # Nếu từ pause vào, data = None và current_screen = "pause"
                # Nếu từ main_menu vào, current_screen không phải "pause"
                if data is None and self.current_screen != "pause":
                    # Reset chỉ khi từ menu (không phải từ pause)
                    self.screens[screen_name].reset_game_state()
        
        # Gọi on_enter() của màn hình mới
        new_screen = self.screens[screen_name]
        if hasattr(new_screen, 'on_enter'):
            new_screen.on_enter()
            
        # Lưu scene hiện tại
        if self.current_screen:
            self.previous_screen = self.current_screen
        
        # Truyền data(điểm số cho game over)
        if data is not None:
            screen = self.screens[screen_name]
            if hasattr(screen, 'set_data'):
                screen.set_data(data)
        
        # Chuyển scene
        self.current_screen = screen_name
        # print(f"Chuyển qua: {screen_name} data hiện có là: {data}")
        
    # Quay lại màn hình trước, chắc ít dùng =)))
    def go_back(self):
        if self.previous_screen:
            self.switch_to(self.previous_screen)
            return True
        return False
    
    # Lấy scene hiện tại
    def get_current_screen(self):
        return self.screens.get(self.current_screen)
    
    # chuyển events
    def handle_events(self, events):
        screen = self.get_current_screen()
        if screen:
            screen.handle_events(events)
    
    # cập nhật screen hiện tại
    def update(self):
        screen = self.get_current_screen()
        if screen:
            screen.update()
            
            # có thể chuyển trang bằng cách đặt next screen, cái này giúp kiểm tra khi muốn chuyển trang
            if hasattr(screen, 'next_screen') and screen.next_screen:
                next_screen = screen.next_screen
                screen_data = getattr(screen, 'screen_data', None)
                screen.next_screen = None
                self.switch_to(next_screen, screen_data)
    
    # cập nhật giao diện của màn hình
    def draw(self):
        scene = self.get_current_screen()
        if scene:
            scene.draw()
    
    # dọn dẹp, giảm bộ nhớ, gọi lần lượt các màn hình
    def quit(self):
        for scene in self.screens.values():
            if hasattr(scene, 'cleanup'):
                scene.cleanup()
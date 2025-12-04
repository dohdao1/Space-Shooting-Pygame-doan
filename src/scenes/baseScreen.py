# khởi tạo class màn hình cơ bản để xây dựng các màn hình khác
class baseScreen:
    def __init__(self, game):
        self.game = game        # Tham chiếu đến game chính
        self.screen = game.screen   # trỏ đến màn hình hiện tại
        self.next_screen = None  # thuộc tính để chuyển đến màn hình tiếp theo
        self.screen_data = None     #các thông tin người chơi, chuyển qua lại giữa các màn hình

    # lấy các dữ liệu vào màn hình này, có thể là điểm người chơi,.. để tránh mất mát dữ liệu
    def set_data(self, data):
        self.screen_data = data
    
    # xử lý các sự kiên
    def handle_events(self, events):
        pass
    
    # update các lohic, (sử dụng chuột,..)
    def update(self):
        pass
    
    # cập nhật giao diện
    def draw(self):
        pass

    # dọn dẹp, dùng khi out
    def cleanup(self):
        pass
    
    # chuyển màn hình
    def switch_to(self, screen_name, data = None):
        self.next_screen = screen_name
        if data:
            self.screen_data = data
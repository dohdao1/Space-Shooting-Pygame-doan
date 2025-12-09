#tính toán âm thanh thắng hoặc thua gì đó, âm thanh khi click chọn,... đây không phải là âm thanh khi va chạm, hay âm thanh bắn, mấy cái đó nên dc xử lý ở trong entities
import pygame
import os

class audioManager:
    def __init__(self, save_manager):
        pygame.mixer.init()
        
        # Lưu reference đến save manager
        self.save_manager = save_manager
        
        # Trạng thái âm thanh (tạm thời)
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        self.music_enabled = True
        self.sfx_enabled = True
        
        # Load cài đặt từ SecureSaveManager
        self.load_settings()
        
        # Các âm thanh
        self.sounds = {}
        self.music_tracks = {}
        self.current_music = None
        
        # Tải âm thanh
        self.load_sounds()
        
    def load_settings(self):
        try:
            settings = self.save_manager.load_settings()
            
            self.music_volume = settings.get("music_volume", 0.5)
            self.sfx_volume = settings.get("sfx_volume", 0.7)
            self.music_enabled = settings.get("music_enabled", True)
            self.sfx_enabled = settings.get("sfx_enabled", True)
            
            # Cập nhật volume ngay lập tức
            if hasattr(self, 'sounds'):
                self.update_volumes()
            else:
                # Nếu sounds chưa được tạo, tải chúng trước
                self.load_sounds()
            
        except Exception as e:
            print(f"Không thể tải cài đặt âm thanh: {e}")
    
    def save_settings(self):
        try:
            # Đọc cài đặt hiện tại
            current_settings = self.save_manager.load_settings()
            
            # Cập nhật chỉ các giá trị âm thanh
            current_settings["music_volume"] = self.music_volume
            current_settings["sfx_volume"] = self.sfx_volume
            current_settings["music_enabled"] = self.music_enabled
            current_settings["sfx_enabled"] = self.sfx_enabled
            
            # Lưu thông qua SecureSaveManager
            self.save_manager.save_settings(current_settings)
            
        except Exception as e:
            print(f"Không thể lưu cài đặt âm thanh: {e}")
    
    # Load âm thanh
    def load_sounds(self):
        try:
            # KHỞI TẠO dictionary sounds TRƯỚC
            self.sounds = {}
            self.music_tracks = {}
            
            # Âm thanh khi thua
            lose_sound_path = ("assets/sounds/func/lose_voice.mp3")
            if os.path.exists(lose_sound_path):
                self.sounds["lose"] = pygame.mixer.Sound(lose_sound_path)
            else:
                print(f"WARNING: File not found: {lose_sound_path}")
        
            # SFX
            sfx_shooter_path = ("assets/sounds/sfx/sfx_space_shooter.mp3")
            if os.path.exists(sfx_shooter_path):
                self.sounds["shooter_sfx"] = pygame.mixer.Sound(sfx_shooter_path)
            else:
                print(f"WARNING: File not found: {sfx_shooter_path}")
            
            # Nhạc nền khi mở game
            bg_music_path = ("assets/sounds/music/background-music.mp3")
            if os.path.exists(bg_music_path):
                self.music_tracks["menu"] = bg_music_path
            else:
                print(f"WARNING: File not found: {bg_music_path}")
            
            # Nhạc khi chơi game
            gameplay_music_path = ("assets/sounds/music/gameplay_music.mp3")
            if os.path.exists(gameplay_music_path):
                self.music_tracks["gameplay"] = gameplay_music_path
            else:
                print(f"WARNING: File not found: {gameplay_music_path}")
            
            # Áp dụng volume
            self.update_volumes()
            
        except Exception as e:
            print(f"Lỗi khi tải âm thanh: {e}")
            import traceback
            traceback.print_exc()
    
    # Chạy nhạc nền
    def play_music(self, track_name, loops=-1):
        if not self.music_enabled:
            return
            
        if track_name in self.music_tracks:
            try:
                pygame.mixer.music.load(self.music_tracks[track_name])
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(loops=loops)
                self.current_music = track_name
            except Exception as e:
                print(f"Không thể phát nhạc {track_name}: {e}")
    
    # Dừng nhạc nền
    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None
    
    # Tạm dừng nhạc nền
    def pause_music(self):
        pygame.mixer.music.pause()
    
    # tiếp tục
    def unpause_music(self):
        if self.music_enabled and self.current_music:
            pygame.mixer.music.unpause()
    
    # âm thanh sfx
    def play_sound(self, sound_name, volume_scale=1.0):
        if not self.sfx_enabled or sound_name not in self.sounds:
            return
        
        try:
            sound = self.sounds[sound_name]
            # Áp dụng volume tổng và scale riêng
            sound.set_volume(self.sfx_volume * volume_scale)
            sound.play()
        except Exception as e:
            print(f"Không thể phát âm thanh {sound_name}: {e}")
    
    # set âm lượng nhạc nền
    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
        self.save_settings()
    
    # set âm lượng âm thanh sfx
    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))
        
        # Cập nhật volume cho tất cả âm thanh đã tải
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
        
        self.save_settings()
    
    # bật tắt nhạc nền, dùng cho enable
    def toggle_music(self, enabled=None):
        if enabled is None:
            self.music_enabled = not self.music_enabled
        else:
            self.music_enabled = enabled
        
        if not self.music_enabled:
            self.stop_music()
        elif self.current_music:
            self.play_music(self.current_music)
        else:
            # Nếu không có nhạc nào đang chơi, chơi nhạc menu mặc định
            self.play_music("menu")
        
        self.save_settings()
        return self.music_enabled
    
    # bật tắt sfx
    def toggle_sfx(self, enabled=None):
        if enabled is None:
            self.sfx_enabled = not self.sfx_enabled
        else:
            self.sfx_enabled = enabled
        
        self.save_settings()
        return self.sfx_enabled
    
    # Cập nhật cài đặt liên quan đến âm thanh
    def update_volumes(self):
        pygame.mixer.music.set_volume(self.music_volume)
        
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
    
    def fadeout_music(self, duration=1000):
        pygame.mixer.music.fadeout(duration)
        self.current_music = None
    
    # kiểm tra âm thanh
    def is_music_playing(self):
        return pygame.mixer.music.get_busy()
    
    def get_volume_info(self):
        return {
            "music_volume": self.music_volume,
            "sfx_volume": self.sfx_volume,
            "music_enabled": self.music_enabled,
            "sfx_enabled": self.sfx_enabled
        }
# Chỗ lưu data
import json
import os
import sys
import hashlib
import base64
import datetime
from cryptography.fernet import Fernet

from utils import update_settings_with_theme, get_default_settings

class SecureSaveManager:
    def __init__(self, game):
        self.game = game
        
        # xem hệ điều hành nào
        self.data_dir = self._get_platform_save_dir()
        
        # Tạo thư mục nếu chưa có
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Đường dẫn file
        self.settings_path = os.path.join(self.data_dir, "settings.dat")
        self.stats_path = os.path.join(self.data_dir, "stats.dat")
        self.spaces_path = os.path.join(self.data_dir, "spaces.dat") 
        self.key_file = os.path.join(self.data_dir, ".key")
        
        # Key mã hóa
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)
    
    # Lấy đường dẫn phì hợp cho hệ điều hành(lưu ở app data dưới dạng mã hóa á)
    def _get_platform_save_dir(self):
        app_name = "SpaceShooter"
        
        # Windows nè(C:\Users\[User]\AppData\Roaming\SpaceShooter\)này dường dẫn vào save nha
        if sys.platform == "win32":
            appdata = os.getenv('APPDATA')
            if appdata:
                return os.path.join(appdata, app_name)
        
        # Fallback(Phươn án dự phòng kk): trong thư mục game
        game_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(game_dir, "user_data")
    
    # Tạo hoặc lấy encryption key
    def _get_or_create_key(self):
        if os.path.exists(self.key_file):
            try:
                with open(self.key_file, 'rb') as f:
                    return f.read()
            except:
                pass
        
        # Tạo key mới
        key = Fernet.generate_key()
        
        # Lưu key
        with open(self.key_file, 'wb') as f:
            f.write(key)
        
        # Đặt quyền chỉ đọc trên Unix-like systems(Này k dùng k biết kk)
        try:
            if sys.platform != "win32":
                import stat
                os.chmod(self.key_file, stat.S_IREAD | stat.S_IWUSR)
        except:
            pass
        
        return key
    
    # Mã hóa data
    def _encrypt(self, data):
        json_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        encrypted = self.cipher.encrypt(json_str.encode('utf-8'))
        return base64.b64encode(encrypted).decode('ascii')
    
    # Giải mã data
    def _decrypt(self, encrypted_str):
        try:            
            # Kiểm tra base64
            encrypted = base64.b64decode(encrypted_str.encode('ascii'))
            
            decrypted = self.cipher.decrypt(encrypted)
            
            result = json.loads(decrypted.decode('utf-8'))
            return result
        except Exception as e:
            print(f"LỖI GIẢI MÃ: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    # Kiểm tra xem có bị sửa hay không(thường ae hay cheat bằng phần mềm ngoài rồi lưu lại kk)
    def _add_hash(self, data):
        data_copy = data.copy()
    
        # LÀM TRÒN CÁC SỐ FLOAT ĐỂ NHẤT QUÁN
        data_copy = self._normalize_floats(data_copy)
        
        data_str = json.dumps(
            data_copy, 
            sort_keys=True, 
            separators=(',', ':'),
            ensure_ascii=False
        )
        
        data_hash = hashlib.sha256(data_str.encode()).hexdigest()
        data_copy['_hash'] = data_hash
        
        return data_copy
    
    # Làm tròn float
    def _normalize_floats(self, obj):
        if isinstance(obj, float):
            # Làm tròn đến 3 chữ số thập phân
            return round(obj, 3)
        elif isinstance(obj, dict):
            return {k: self._normalize_floats(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._normalize_floats(item) for item in obj]
        else:
            return obj

    # Kiểm tra hash
    def _verify_hash(self, data):
        if '_hash' not in data:
            return False
        
        saved_hash = data['_hash']
        data_copy = data.copy()
        del data_copy['_hash']
        
        data_copy = self._normalize_floats(data_copy)
        
        data_str = json.dumps(
            data_copy, 
            sort_keys=True, 
            separators=(',', ':'),
            ensure_ascii=False
        )
        
        calculated_hash = hashlib.sha256(data_str.encode()).hexdigest()
                
        return saved_hash == calculated_hash
    
    # ===================================================================#
    # ==      Dưới này dùng để lấy data thêm sửa xóa trong game nè     ==#
    # ===================================================================#

    # Load id space
    def load_spaces(self):
        default_spaces = {
            'current': 'default',      # Space đang dùng
            'unlocked': ['default']    # Danh sách spaces đã mở
        }
        
        if not os.path.exists(self.spaces_path):
            return default_spaces
        
        try:
            with open(self.spaces_path, 'r', encoding='utf-8') as f:
                encrypted = f.read()
            
            decrypted = self._decrypt(encrypted)
            
            if decrypted and self._verify_hash(decrypted):
                # Merge với defaults
                merged = default_spaces.copy()
                for key in ['current', 'unlocked']:
                    if key in decrypted:
                        merged[key] = decrypted[key]
                
                return merged
            else:
                return default_spaces
        except Exception as e:
            print(f"Lỗi load spaces: {e}")
            return default_spaces
    
    # Lưu spaces
    def save_spaces(self, spaces_data):
        try:
            spaces_with_hash = self._add_hash(spaces_data)
            encrypted = self._encrypt(spaces_with_hash)
            
            with open(self.spaces_path, 'w', encoding='utf-8') as f:
                f.write(encrypted)
            
            return True
        except Exception as e:
            print(f"Lỗi lưu spaces: {e}")
            return False
    
    # Mở khóa
    def unlock_space(self, space_id, cost):
        """Mở khóa space mới"""
        spaces = self.load_spaces()
        stats = self.load_stats()
        
        # Kiểm tra đã unlock chưa
        if space_id in spaces['unlocked']:
            return True
        
        # Kiểm tra đủ coin không
        if stats['coin'] < cost:
            return False
        
        # Trừ coin và unlock
        stats['coin'] -= cost
        spaces['unlocked'].append(space_id)
        
        # Lưu lại
        self.save_stats(stats)
        self.save_spaces(spaces)
        
        return True
    
    # Đặt space dùng
    def set_current_space(self, space_id):
        spaces = self.load_spaces()
        
        # Kiểm tra space đã unlock chưa
        if space_id not in spaces['unlocked']:
            return False
        
        spaces['current'] = space_id
        self.save_spaces(spaces)
        
        return True
    
    # Lấy space id hiện đã set
    def get_current_space(self):
        spaces = self.load_spaces()
        return spaces['current']
    
    # Lấy danh sách đã mở khóa
    def get_unlocked_spaces(self):
        spaces = self.load_spaces()
        return spaces['unlocked']

    # Lưu cài đặt
    def save_settings(self, settings):
        try:
            settings_to_save = {
                'music_volume': settings.get('music_volume', 0.5),
                'sfx_volume': settings.get('sfx_volume', 0.7),
                'music_enabled': settings.get('music_enabled', True),
                'sfx_enabled': settings.get('sfx_enabled', True),
                'theme': settings.get('theme', 'dark'),
            }
            
            settings_with_hash = self._add_hash(settings_to_save)
            encrypted = self._encrypt(settings_with_hash)
            
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                f.write(encrypted)
            
            return True
        except Exception as e:
            print(f"Lỗi k lưu dc: {e}")
            return False
    
    # Load cài đặt
    def load_settings(self):
        default_settings = get_default_settings()
        
        if not os.path.exists(self.settings_path):
            return update_settings_with_theme(default_settings)
        
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                encrypted = f.read()
            
            decrypted = self._decrypt(encrypted)
            
            if decrypted and self._verify_hash(decrypted):
                # Merge với defaults (cho các key mới)
                merged = default_settings.copy()
                for key, value in decrypted.items():
                    if key not in ['_hash']:
                        merged[key] = value

                if merged.get('theme') not in ['dark', 'light', 'gray']:
                    merged['theme'] = 'dark'
                
                return update_settings_with_theme(merged)
            else:
                return update_settings_with_theme(default_settings)
                
        except Exception as e:
            print(f"Lỗi load setting file: {e}")
            return update_settings_with_theme(default_settings)
    
    # Lưu thành tích
    def save_stats(self, stats):
        try:            
            stats_with_hash = self._add_hash(stats)
            
            encrypted = self._encrypt(stats_with_hash)
                        
            with open(self.stats_path, 'w', encoding='utf-8') as f:
                f.write(encrypted)
                        
            if os.path.exists(self.stats_path):
                with open(self.stats_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            return True
        except Exception as e:
            print(f"Lỗi trong quá trình lưu: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    # Load thành tích người chơi
    def load_stats(self):
        default_stats = {
            'high_score': 0,
            'total_games': 0,
            'total_play_time': 0,
            'total_kills': 0,
            'total_deaths': 0,
            
            # Lịch sử game
            'game_history': [],
            
            # Coin( hệ thống tiền tệ riêng trong game)
            'coin' : 0
        }
                
        if not os.path.exists(self.stats_path):
            return default_stats
        
        try:
            with open(self.stats_path, 'r', encoding='utf-8') as f:
                encrypted = f.read()
            
            decrypted = self._decrypt(encrypted)
            
            if decrypted:                
                hash_valid = self._verify_hash(decrypted)
                
                if hash_valid:
                    if '_hash' in decrypted:
                        del decrypted['_hash']
                    
                    merged = default_stats.copy()  # Bắt đầu từ default
                    
                    for key, value in decrypted.items():
                        merged[key] = value
                    
                    return merged
                else:
                    return default_stats
            else:
                return default_stats
                
        except Exception as e:
            print(f"LỖI LOAD THÀNH TỰU GAME: {e}")
            import traceback
            traceback.print_exc()
            return default_stats
        
    # Cập nhật điểm cao
    def update_high_score(self, score):
        stats = self.load_stats()
        
        if score > stats['high_score']:
            stats['high_score'] = score
            success = self.save_stats(stats)
            self.save_stats(stats)
            return True
        
        return False
    
    # Thêm lịch sử
    def add_game_history(self, score, play_time, kills=0, deaths=0,status="game_over"):
        stats = self.load_stats()

        if 'game_history' not in stats:
            stats['game_history'] = []  # Tạo mới nếu chưa có
        
        game_record = {
            'score': score,
            'play_time': play_time,
            'kills': kills,
            'deaths': deaths,
            'status': status,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        # Thêm vào đầu list (giữ 20 game gần nhất)
        stats['game_history'].insert(0, game_record)
        stats['game_history'] = stats['game_history'][:10]
        
        # Cập nhật tổng
        # stats['total_games'] += 1
        # stats['total_play_time'] += play_time
        # stats['total_kills'] += kills
        # stats['total_deaths'] += deaths
        
        self.save_stats(stats)
        
    # Thêm coin đơn giản
    def add_coin(self, amount):
        stats = self.load_stats()
        stats['coin'] += amount
        self.save_stats(stats)
        return stats['coin']
    
    # Trừ coin đơn giản
    def subtract_coin(self, amount):
        stats = self.load_stats()
        if stats['coin'] >= amount:
            stats['coin'] -= amount
            self.save_stats(stats)
            return True
        return False

    # Trả về vị trí lưu, nếu lỗi
    def get_save_location(self):
        return os.path.abspath(self.data_dir)
    
    # Thông tin hệ thống lưu
    def get_system_info(self):
        info = {
            'platform': sys.platform,
            'save_dir': self.data_dir,
            'settings_file': self.settings_path,
            'stats_file': self.stats_path,
            'key_file': self.key_file,
            'exists': {
                'settings': os.path.exists(self.settings_path),
                'stats': os.path.exists(self.stats_path),
                'key': os.path.exists(self.key_file)
            }
        }
        return info
    
    # Xuất settings ra JSON plain text (cho debug)
    def export_settings_json(self, export_path):
        try:
            settings = self.load_settings()
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
            print(f"Đã xuất file ra: {export_path}")
            return True
        except Exception as e:
            print(f"Không thể xuất file: {e}")
            return False
    
    # Import save ở ngoài dưới dạng json
    def import_settings_json(self, import_path):
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            self.save_settings(settings)
            print(f"Thồng canh: {import_path}")
            return True
        except Exception as e:
            print(f"Nhập lỗi rồi: {e}")
            return False
        
    # xóa lịch sử(coin còn á)
    def clear_game_history(self):
        try:
            stats = self.load_stats()
            
            # Giữ lại các giá trị quan trọng
            coin = stats.get('coin', 0)
            
            # Tạo stats mới với điểm cao và coin cũ
            new_stats = self._get_default_stats()
            new_stats['coin'] = coin
            
            # Lưu lại
            self.save_stats(new_stats)
            return True
        except Exception as e:
            print(f"Lỗi khi xóa lịch sử: {e}")
            return False
    
    # Xóa toàn bộ data
    def reset_all_data(self):
        try:
            # Xóa các file dữ liệu
            files_to_delete = [
                self.settings_path,
                self.stats_path,
                self.spaces_path
            ]
            
            deleted_files = []
            for file_path in files_to_delete:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    deleted_files.append(os.path.basename(file_path))
                        
            return True
        except Exception as e:
            print(f"Lỗi khi xóa dữ liệu: {e}")
            return False
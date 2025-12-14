# Space-Shooting-by-Pygame
trò chơi bắn thiên thạch đơn giản bằng pygame

cần cài các module cần thiết cho game:
1. Đầu tiên:
pip install pygame nếu bạn chưa có

2. Dùng đễ mã hóa save của game, bạn cần tải nếu muốn sử dụng source
pip install cryptography

3. Đóng gói file(dùng console)
Đầu tiên cần install module sau
pip install pyinstaller

    # Dùng cách đơn giản nhất:
    pyinstaller --onefile --windowed --name "SpaceShooter" src/main.py

    # Đầy đủ hơn:
    pyinstaller --onefile --windowed --name "SpaceShooter" --icon="assets/icon.ico" --add-data="assets;assets" src/main.py

    Trong đó:
    --onefile: Gộp tất cả thành 1 file .exe duy nhất

    --windowed: Không hiển thị console (ẩn cmd)

    --name: Đặt tên file output

    --icon: Thêm icon cho file .exe

    --add-data: Thêm thư mục assets vào trong exe

    MẪU: 
    pyinstaller --noconfirm --onefile --windowed --icon "C:\learn\uthEx\nam4\DoAnThucTeCNPM\Space-Shooting-Pygame-doan\assets\icon.ico" --name "Space Shooter" --add-data "C:\learn\uthEx\nam4\DoAnThucTeCNPM\Space-Shooting-Pygame-doan\src\config.py;." --add-data "C:\learn\uthEx\nam4\DoAnThucTeCNPM\Space-Shooting-Pygame-doan\assets;assets/"  "C:\learn\uthEx\nam4\DoAnThucTeCNPM\Space-Shooting-Pygame-doan\src\main.py"

4. Dùng đóng gói bằng giao diện
pip install auto-py-to-exe
- Chạy
auto-py-to-exe
    Trong giao diện
    Script Location: Chọn src/main.py

    Onefile: ✔ Tick "One File"

    Window Based: ✔ Tick "Window Based (hide console)"

    Icon: Chọn file .ico (nếu có)

    Additional Files: Thêm thư mục assets

    Bấm CONVERT .PY TO .EXE
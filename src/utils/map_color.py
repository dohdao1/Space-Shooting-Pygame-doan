# map theme từ save về màu nền
THEMES = {
    'dark': {
        'name': 'Dark',
        'bg_color': (20, 20, 40),      # Xanh đêm
        'ui_bg': (40, 40, 60),         # Xám đậm
        'ui_text': (255, 255, 255),    # Trắng
        'ui_accent': (100, 200, 255),  # Xanh sáng
    },
    'light': {
        'name': 'Light',
        'bg_color': (240, 240, 250),   # Trắng sáng
        'ui_bg': (220, 220, 230),      # Xám nhạt
        'ui_text': (30, 30, 40),       # Đen
        'ui_accent': (30, 100, 200),   # Xanh đậm
    },
    'gray': {
        'name': 'Gray',
        'bg_color': (60, 60, 80),      # Xám đậm
        'ui_bg': (80, 80, 100),        # Xám trung
        'ui_text': (220, 220, 240),    # Trắng xám
        'ui_accent': (180, 180, 220),  # Xám xanh
    }
}

def get_theme(theme_name='dark'):
    return THEMES.get(theme_name, THEMES['dark'])

def get_bg_color(theme_name='dark'):
    return get_theme(theme_name)['bg_color']

def get_ui_bg_color(theme_name='dark'):
    return get_theme(theme_name)['ui_bg']

def get_ui_text_color(theme_name='dark'):
    return get_theme(theme_name)['ui_text']

def get_ui_accent_color(theme_name='dark'):
    return get_theme(theme_name)['ui_accent']

# setting mặc định
def get_default_settings():
    return {
        # Âm thanh
        'music_volume': 0.5,
        'sfx_volume': 0.7,
        'music_enabled': True,
        'sfx_enabled': True,
        'theme': 'dark'
    }
# cập nhật màu sắc từ theme
def update_settings_with_theme(settings):
    theme_name = settings.get('theme', 'dark')
    theme = get_theme(theme_name)
    
    # Thêm các màu derived từ theme
    settings['bg_color'] = theme['bg_color']
    settings['ui_bg'] = theme['ui_bg']
    settings['ui_text'] = theme['ui_text']
    settings['ui_accent'] = theme['ui_accent']
    
    return settings
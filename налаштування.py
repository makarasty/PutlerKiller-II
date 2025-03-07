import json
import os
from os.path import split, join, abspath
from ctypes import windll

FILE_NAME = "settings.json"

def load_settings():
    defaults = {
        "game_volume": 0.5,
        "music_volume": 0.01,
        "mouse_sens": 1.0,
        "fullscreen": True,
        "fps_limit": 144,
        "screen_width": 1920,
        "screen_height": 1080
    }
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                data = json.load(f)
            for key in defaults:
                if key not in data:
                    data[key] = defaults[key]
            return data
        except:
            return defaults
    else:
        return defaults

def save_settings(data: dict):
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        pass

CONFIG = load_settings()

game_volume  = CONFIG["game_volume"]
music_volume = CONFIG["music_volume"]
mouse_sens   = CONFIG["mouse_sens"]
fullscreen   = CONFIG["fullscreen"]
fps_limit    = CONFIG["fps_limit"]
screen_width = CONFIG["screen_width"]
screen_height= CONFIG["screen_height"]

Гра_ширина = screen_width
Гра_висота = screen_height
FPS = fps_limit

ii = 0
блік = False
рівень = 1
убийств = 0
рахунок = 0
постріли = 0
пропущенні = 0
рахунок_ЗаВбивство = 2
максимально_пропущенних = 3
прокачувати_рівень_кожні = 10
Ворог_k = [0, 0, 0, 0]
Ворог_k_ = False
Ворог_k_pos = 0
Максимальний_боєзапас = 10

Масив_зiрки = []
Масив_зiрки_2 = []
Максимально_зiрок = 200

ініціалізація_гри = False

користувач = windll.user32
СИСТЕМА_ширина = користувач.GetSystemMetrics(0)
СИСТЕМА_висота = користувач.GetSystemMetrics(1)

папка_з_грою = split(abspath(__file__))[0]
папка_з_датою = join(папка_з_грою, 'src')

def update_and_save_settings(new_game_volume=None, new_music_volume=None, new_mouse_sens=None,
                             new_fullscreen=None, new_fps_limit=None, new_screen_width=None, new_screen_height=None):
    global game_volume, music_volume, mouse_sens, fullscreen, fps_limit, screen_width, screen_height, Гра_ширина, Гра_висота, FPS
    updated = False
    if new_game_volume is not None:
        game_volume = new_game_volume
        CONFIG["game_volume"] = new_game_volume
        updated = True
    if new_music_volume is not None:
        music_volume = new_music_volume
        CONFIG["music_volume"] = new_music_volume
        updated = True
    if new_mouse_sens is not None:
        mouse_sens = new_mouse_sens
        CONFIG["mouse_sens"] = new_mouse_sens
        updated = True
    if new_fullscreen is not None:
        fullscreen = new_fullscreen
        CONFIG["fullscreen"] = new_fullscreen
        updated = True
    if new_fps_limit is not None:
        fps_limit = new_fps_limit
        CONFIG["fps_limit"] = new_fps_limit
        FPS = new_fps_limit
        updated = True
    if new_screen_width is not None:
        screen_width = new_screen_width
        CONFIG["screen_width"] = new_screen_width
        Гра_ширина = new_screen_width
        updated = True
    if new_screen_height is not None:
        screen_height = new_screen_height
        CONFIG["screen_height"] = new_screen_height
        Гра_висота = new_screen_height
        updated = True
    if updated:
        save_settings(CONFIG)

import pygame
import налаштування as дата

from src import функції
from src import ворог
from src import зброя

from random import choice
from os import listdir
from os.path import isfile, join
from time import time

pygame.init()
pygame.font.init()

# --- Шрифти ---
шрифт_м = pygame.font.Font(join(дата.папка_з_датою, 'LeelawUI.ttf'), 16)
шрифт_в = pygame.font.Font(join(дата.папка_з_датою, 'LeelawUI.ttf'), 30)

# Глобальна змінна для екрану
Гра = None

def set_display_mode():
    """Встановлює режим відображення згідно з налаштуваннями."""
    global Гра
    flags = pygame.FULLSCREEN if дата.fullscreen else 0
    Гра = pygame.display.set_mode((дата.Гра_ширина, дата.Гра_висота), flags)
    pygame.display.set_caption("Putler killer II")
    return Гра

# Ініціалізація дисплея:
Гра = set_display_mode()

# --- Створення спрайтів ---
курсор_з_прицiлом = зброя.приціл()
Зброя = зброя.зброя()

Спрайти = pygame.sprite.Group()
Спрайти_верх = pygame.sprite.Group()
Спрайти_верх.add(Зброя, курсор_з_прицiлом)

# --- Перший ворог ---
Ворог = ворог.путлер()
Спрайти.add(Ворог)

# --- Звуки ---
Звук_постріл       = функції.Завантаити_звук('звуки/shot.wav',   0.02 * дата.game_volume * 2)
Звук_немаєПатронів = функції.Завантаити_звук('звуки/empty.wav',  0.03 * дата.game_volume * 2)
Звук_перезарядка   = функції.Завантаити_звук('звуки/reload.wav', 0.03 * дата.game_volume * 2)

# --- Фон ---
фон = функції.Завантаити_фон()

# --- Статусбар та логотип ---
Картинка_статусбар = pygame.image.load(join(дата.папка_з_датою, 'картинки/статусбар.png'))
Картинка_лого      = pygame.image.load(join(дата.папка_з_датою, 'картинки/лого.png'))

# --- Фонова музика ---
папка_музики = join(дата.папка_з_датою, "звуки/музика")
масив_пісні = [ф for ф in listdir(папка_музики) if isfile(join(папка_музики, ф))]
фонова_музика = функції.Завантаити_музику(f'звуки/музика/{choice(масив_пісні)}')
pygame.mixer.music.set_volume(дата.music_volume)
фонова_музика.play(-1)

# --- Генерація зірок ---
функції.Генерація_зірок()

# --- Стан гри ---
Постріл = None
гра_робить = True
назва_кімнати = 'меню'

# --- Поля вводу для налаштувань ---
mouse_sens_input_box = pygame.Rect(400, 195, 100, 30)
mouse_sens_str = ""
mouse_sens_active = False

fps_limit_input_box = pygame.Rect(400, 325, 100, 30)
fps_limit_str = ""
fps_limit_active = False

resolution_box = pygame.Rect(50, 250, 300, 30)
resolution_options = pygame.display.list_modes() or [(1366, 768)]
current_res = (дата.Гра_ширина, дата.Гра_висота)
resolution_index = resolution_options.index(current_res) if current_res in resolution_options else 0

# --- Клас для слайдерів ---
class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, value):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = value
        self.active = False
        self.handle_radius = height * 2

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        handle_x = self.rect.x + int(ratio * self.rect.width)
        handle_y = self.rect.y + self.rect.height // 2
        pygame.draw.circle(surface, (255, 255, 0), (handle_x, handle_y), self.handle_radius)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.update_value(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.active = False
        elif event.type == pygame.MOUSEMOTION and self.active:
            self.update_value(event.pos[0])

    def update_value(self, mouse_x):
        rel_x = max(0, min(mouse_x - self.rect.x, self.rect.width))
        ratio = rel_x / self.rect.width
        self.value = self.min_val + ratio * (self.max_val - self.min_val)
        return self.value

slider_sfx = Slider(200, 110, 300, 8, 0.0, 1.0, дата.game_volume)
slider_music = Slider(200, 160, 300, 8, 0.0, 1.0, дата.music_volume)

clock = pygame.time.Clock()

def center_text(surface, text_surf, y):
    x = (surface.get_width() - text_surf.get_width()) // 2
    surface.blit(text_surf, (x, y))

while гра_робить:
    дата.ii += 1
    if дата.ii % 50 == 0:
        дата.блік = not дата.блік

    clock.tick(дата.FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            гра_робить = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if назва_кімнати == 'гра':
                    функції.clear()
                    Зброя.боєзапас = дата.Максимальний_боєзапас
                    Ворог.kill()
                    Ворог = ворог.путлер()
                    Спрайти.add(Ворог)
                    назва_кімнати = 'меню'
                elif назва_кімнати == 'налаштування':
                    назва_кімнати = 'меню'
                else:
                    назва_кімнати = 'вихід'
                    гра_робить = False

            if event.key == pygame.K_SPACE:
                if назва_кімнати in ['меню', 'вихід']:
                    функції.clear()
                    Зброя.боєзапас = дата.Максимальний_боєзапас
                    Ворог.kill()
                    Ворог = ворог.путлер()
                    Спрайти.add(Ворог)
                    назва_кімнати = 'гра'

            if event.key == pygame.K_s and назва_кімнати == 'меню':
                назва_кімнати = 'налаштування'

            if назва_кімнати == 'налаштування' and event.key == pygame.K_f:
                new_state = not дата.fullscreen
                дата.update_and_save_settings(new_fullscreen=new_state)
                set_display_mode()

            if назва_кімнати == 'налаштування' and mouse_sens_active:
                if event.key == pygame.K_RETURN:
                    try:
                        val = float(mouse_sens_str)
                        if val < 0.1: val = 0.1
                        elif val > 2.0: val = 2.0
                        дата.update_and_save_settings(new_mouse_sens=val)
                    except:
                        pass
                    mouse_sens_str = ""
                    mouse_sens_active = False
                elif event.key == pygame.K_BACKSPACE:
                    mouse_sens_str = mouse_sens_str[:-1]
                else:
                    if event.unicode.isdigit() or event.unicode in ['.', ',']:
                        mouse_sens_str += '.' if event.unicode == ',' else event.unicode

            if назва_кімнати == 'налаштування' and fps_limit_active:
                if event.key == pygame.K_RETURN:
                    try:
                        val = int(fps_limit_str)
                        if val < 30: val = 30
                        elif val > 1000: val = 1000
                        дата.update_and_save_settings(new_fps_limit=val)
                    except:
                        pass
                    fps_limit_str = ""
                    fps_limit_active = False
                elif event.key == pygame.K_BACKSPACE:
                    fps_limit_str = fps_limit_str[:-1]
                else:
                    if event.unicode.isdigit():
                        fps_limit_str += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if назва_кімнати == 'налаштування':
                if mouse_sens_input_box.collidepoint(event.pos):
                    mouse_sens_active = True
                else:
                    mouse_sens_active = False
                if fps_limit_input_box.collidepoint(event.pos):
                    fps_limit_active = True
                else:
                    fps_limit_active = False
                if not дата.fullscreen and resolution_box.collidepoint(event.pos):
                    resolution_index = (resolution_index + 1) % len(resolution_options)
                    new_res = resolution_options[resolution_index]
                    дата.update_and_save_settings(new_screen_width=new_res[0], new_screen_height=new_res[1])
                    set_display_mode()

            if назва_кімнати == 'налаштування':
                slider_sfx.handle_event(event)
                slider_music.handle_event(event)

        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP):
            if назва_кімнати == 'налаштування':
                slider_sfx.handle_event(event)
                slider_music.handle_event(event)

    if назва_кімнати == 'налаштування':
        if abs(slider_sfx.value - дата.game_volume) > 0.001:
            дата.update_and_save_settings(new_game_volume=slider_sfx.value)
            Звук_постріл.set_volume(0.02 * дата.game_volume * 2)
            Звук_немаєПатронів.set_volume(0.03 * дата.game_volume * 2)
            Звук_перезарядка.set_volume(0.03 * дата.game_volume * 2)
        if abs(slider_music.value - дата.music_volume) > 0.001:
            дата.update_and_save_settings(new_music_volume=slider_music.value)
            pygame.mixer.music.set_volume(дата.music_volume)

    Миш_Кнопка_Ліва, _, Миш_Кнопка_Права = pygame.mouse.get_pressed()
    screen_w, screen_h = Гра.get_size()

    if назва_кімнати == 'меню':
        pygame.mouse.set_visible(True)
        Гра.fill((0, 0, 0))
        функції.зірки(Гра)
        x_logo = (screen_w - Картинка_лого.get_width()) // 2
        Гра.blit(Картинка_лого, (x_logo, screen_h // 4))
        if дата.блік:
            txt_start = шрифт_в.render("PRESS SPACE TO START", True, (255, 255, 255))
            center_text(Гра, txt_start, screen_h // 2 + 60)
        інфо = шрифт_м.render("Press [S] for Settings", True, (255, 255, 255))
        center_text(Гра, інфо, screen_h // 2 + 120)
        pygame.display.update()

    elif назва_кімнати == 'налаштування':
        pygame.mouse.set_visible(True)
        Гра.fill((50, 50, 50))
        заголовок = шрифт_в.render("Settings", True, (255, 255, 255))
        center_text(Гра, заголовок, 30)
        label_sfx = шрифт_м.render("SFX Volume", True, (255, 255, 255))
        Гра.blit(label_sfx, (50, 100))
        slider_sfx.draw(Гра)
        label_music = шрифт_м.render("Music Volume", True, (255, 255, 255))
        Гра.blit(label_music, (50, 150))
        slider_music.draw(Гра)
        label_ms = шрифт_м.render("Mouse Sensitivity (0.1-2.0)", True, (255, 255, 255))
        Гра.blit(label_ms, (50, 200))
        pygame.draw.rect(Гра, (40, 40, 40), mouse_sens_input_box)
        text_ms = шрифт_м.render(mouse_sens_str if mouse_sens_active else str(round(дата.mouse_sens, 2)), True, (255, 255, 0))
        Гра.blit(text_ms, (mouse_sens_input_box.x + 5, mouse_sens_input_box.y + 5))
        if not дата.fullscreen:
            label_res = шрифт_м.render("Resolution (click to change)", True, (255, 255, 255))
            Гра.blit(label_res, (50, 220))
            pygame.draw.rect(Гра, (40, 40, 40), resolution_box)
            current_res_text = f"{resolution_options[resolution_index][0]} x {resolution_options[resolution_index][1]}"
            text_res = шрифт_м.render(current_res_text, True, (255, 255, 0))
            Гра.blit(text_res, (resolution_box.x + 5, resolution_box.y + 5))
        label_fps = шрифт_м.render("FPS Limit (30-1000)", True, (255, 255, 255))
        Гра.blit(label_fps, (50, 330))
        pygame.draw.rect(Гра, (40, 40, 40), fps_limit_input_box)
        text_fps = шрифт_м.render(fps_limit_str if fps_limit_active else str(дата.FPS), True, (255, 255, 0))
        Гра.blit(text_fps, (fps_limit_input_box.x + 5, fps_limit_input_box.y + 5))
        instr1 = шрифт_м.render("Press F to toggle Fullscreen", True, (200, 200, 200))
        instr2 = шрифт_м.render("Press ESC to return to Menu", True, (200, 200, 200))
        Гра.blit(instr1, (50, 400))
        Гра.blit(instr2, (50, 430))
        pygame.display.update()

    elif назва_кімнати == 'гра':
        pygame.mouse.set_visible(False)
        if not дата.ініціалізація_гри:
            pygame.mouse.set_pos([screen_w // 2, screen_h // 2])
            дата.ініціалізація_гри = True
        # --- Логіка пострілів та перевірка попадань ---
        if Миш_Кнопка_Ліва and Зброя.боєзапас > 0:
            if not Постріл:
                if pygame.sprite.collide_mask(Ворог, курсор_з_прицiлом):
                    Вибух = ворог.вибух()
                    Спрайти.add(Вибух)
                    дата.Ворог_k = [дата.рахунок_ЗаВбивство * дата.рівень,
                                     Вибух.rect.x, Вибух.rect.y, int(time())]
                    дата.Ворог_k_pos = 0
                    дата.Ворог_k_ = True
                    Ворог.kill()
                    Ворог = ворог.путлер()
                    Спрайти.add(Ворог)
                    дата.убийств += 1
                    if дата.убийств % дата.прокачувати_рівень_кожні == 0:
                        дата.рівень += 1
                    функції.Прорахувати_рахунок()
        if Миш_Кнопка_Ліва and not Постріл:
            if Зброя.боєзапас > 0:
                Звук_постріл.play()
                # Створюємо постріл із передачею положення зброї
                Постріл = зброя.постріл(Зброя.rect)
                Спрайти.add(Постріл)
                дата.постріли += 1
                Зброя.боєзапас -= 1
            else:
                Звук_немаєПатронів.play()
        Постріл = Миш_Кнопка_Ліва
        if not Миш_Кнопка_Ліва and Миш_Кнопка_Права and Зброя.боєзапас == 0:
            Звук_перезарядка.play()
            Зброя.боєзапас = дата.Максимальний_боєзапас
        if (Ворог.rect.x > screen_w or Ворог.rect.y > screen_h or
            Ворог.rect.x < -Ворог.Спрайт_розмір or Ворог.rect.y < -Ворог.Спрайт_розмір):
            Ворог.kill()
            Ворог = ворог.путлер()
            Спрайти.add(Ворог)
            дата.пропущенні += 1
            if дата.пропущенні >= дата.максимально_пропущенних:
                дата.ініціалізація_гри = False
                назва_кімнати = 'вихід'
        if дата.Ворог_k_:
            дата.Ворог_k_pos += 1
        if дата.Ворог_k[3] + 1 < int(time()):
            дата.Ворог_k = [0, -200, -200, 0]
            дата.Ворог_k_pos = 0
            дата.Ворог_k_ = False
        Спрайти.update()
        Спрайти_верх.update()
        Гра.fill((0, 0, 0))
        Гра.blit(фон, (0, 0))
        функції.зірки(Гра)
        функції.пулі(Гра, Зброя.боєзапас)
        функції.статусбар(Гра, Картинка_статусбар, шрифт_м)
        функції.убивство(Гра, шрифт_м, дата.Ворог_k[0],
                         дата.Ворог_k[1], дата.Ворог_k[2], дата.Ворог_k[3])
        Спрайти.draw(Гра)
        Спрайти_верх.draw(Гра)
        pygame.display.update()

    elif назва_кімнати == 'вихід':
        pygame.mouse.set_visible(True)
        if not дата.ініціалізація_гри:
            Ворог.kill()
            дата.ініціалізація_гри = True
        Гра.fill((0, 0, 0))
        функції.зірки(Гра)
        функції.гра_завершенна(Гра, шрифт_в, шрифт_м)
        pygame.display.update()

pygame.quit()

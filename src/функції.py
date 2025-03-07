import pygame
import налаштування as дата
from os.path import join, isfile
from os import listdir
from random import randint, choice

white   = (255, 255, 255)
black   = (0,   0,   0)

def Ініціалізуватив_вікно_гри(Вікно_ширина, Вікно_висота, весьЕкран, колір, підпис):
    вікно = pygame.display.set_mode((Вікно_ширина, Вікно_висота), весьЕкран)
    pygame.display.set_caption(підпис)
    вікно.fill(колір)
    return вікно

def Завантаити_звук(НазваФайлу, базова_гучність=1.0):
    звук = pygame.mixer.Sound(join(дата.папка_з_датою, НазваФайлу))
    звук.set_volume(базова_гучність * дата.game_volume)
    return звук

def Завантаити_музику(fileName):
    pygame.mixer.music.load(join(дата.папка_з_датою, fileName))
    pygame.mixer.music.set_volume(дата.music_volume)
    return pygame.mixer.music

def Завантаити_фон():
    return pygame.transform.scale(
        pygame.image.load(join(дата.папка_з_датою, 'картинки/фон.jpg')),
        (дата.Гра_ширина, дата.Гра_висота)
    )

def пулі(гра, боєзапас):
    for пуля in range(0, боєзапас):
        гра.blit(
            pygame.image.load(join(дата.папка_з_датою, 'картинки/патрон.png')),
            (дата.Гра_ширина - 32 - (пуля * 16), 16)
        )
    if боєзапас == 0:
        гра.blit(
            pygame.image.load(join(дата.папка_з_датою, 'картинки/перезарядка.png')),
            (дата.Гра_ширина - 510, -20)
        )

def статусбар(гра, статусбар_картинка, шрифт):
    гра.blit(статусбар_картинка, (12, 12))
    гра.blit(шрифт.render(str(дата.рівень if дата.рівень >= 10 else '0'+str(дата.рівень)), True, white), (184, 29))
    гра.blit(шрифт.render(str(дата.убийств), True, white), (78, 26))
    гра.blit(шрифт.render(str(дата.пропущенні), True, white), (78, 63))
    гра.blit(шрифт.render(str(дата.рахунок), True, white), (100, 95))

def зірки(гра):
    for зірка in дата.Масив_зiрки:
        pygame.draw.line(гра, white, (зірка[0], зірка[1]), (зірка[0], зірка[1]))
        зірка[0] = зірка[0] - 1
        if зірка[0] < 0:
            зірка[0] = дата.Гра_ширина
            зірка[1] = randint(0, дата.Гра_висота)
    for зірка in дата.Масив_зiрки_2:
        pygame.draw.line(гра, white, (зірка[0], зірка[1]), (зірка[0], зірка[1]))
        зірка[0] = зірка[0] - 2
        if зірка[0] < 0:
            зірка[0] = дата.Гра_ширина
            зірка[1] = randint(0, дата.Гра_висота)

def меню(гра, шрифт):
    if дата.блік:
        txt = шрифт.render('PRESS SPACE TO START THE GAME', True, (255,255,255))
        гра.blit(txt, txt.get_rect(center=(дата.Гра_ширина / 2, дата.Гра_висота / 2 + 60)))
    txt2 = шрифт.render('PRESS [S] FOR SETTINGS', True, (255,255,255))
    гра.blit(txt2, txt2.get_rect(center=(дата.Гра_ширина / 2, дата.Гра_висота / 2 + 120)))

def гра_завершенна(гра, шрифт_в, шрифт_м):
    if дата.блік:
        a = шрифт_в.render('PRESS SPACE TO RESTART THE GAME', True, (255,255,255))
        гра.blit(a, a.get_rect(center=(дата.Гра_ширина / 2, дата.Гра_висота / 2 + 60)))
    s = шрифт_в.render(f'Your record: {дата.рахунок}', True, (255,255,255))
    гра.blit(s, s.get_rect(center=(дата.Гра_ширина / 2, дата.Гра_висота / 2)))

def убивство(гра, шрифт, рахунок, x, y, _час):
    t = шрифт.render('KILL', True, (255,255,255))
    гра.blit(t, t.get_rect(center=(x + 100, y + 100 - дата.Ворог_k_pos)))

def clear():
    дата.убийств = 0
    дата.рахунок = 0
    дата.постріли = 0
    дата.пропущенні = 0
    дата.рівень = 1
    дата.ініціалізація_гри = False

def Генерація_зірок():
    from random import randint
    дата.Масив_зiрки = [[randint(0, дата.Гра_ширина), randint(0, дата.Гра_висота)] for _ in range(дата.Максимально_зiрок)]
    дата.Масив_зiрки_2 = [[randint(0, дата.Гра_ширина), randint(0, дата.Гра_висота)] for _ in range(дата.Максимально_зiрок)]

def Прорахувати_рахунок():
    дата.рахунок += (дата.рахунок_ЗаВбивство * дата.рівень)

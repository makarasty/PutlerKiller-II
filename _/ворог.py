#
# ! При створюванні проекту використовувалось
# *
# * (офіційна документація pygame)                   === https://www.pygame.org/docs/tut/newbieguide.html
# * (безкоштовні шрифти від google)                  === https://fonts.google.com/
# * (безкоштовний сервіс анімацій, картинкок, відео) === https://www.istockphoto.com/
# * (Приклади інших робіт з бібліотекою pygame)      === https://github.com/search?q=pygame
# *
# ! Гру створив MaKarastY
#

import pygame
import налаштування as дата
from random import randint, choice
from os import listdir
from os.path import isfile, join


class путлер(pygame.sprite.Sprite):
    Вибрана_позиція = 'ліво'
    швидкість = 0
    Спрайт_розмір = 200

    def __init__(self):
        super().__init__()
        # ? завантажуємо випадковий спрайт «путлера»
        self.image = pygame.image.load(
            join(дата.папка_з_датою, f'картинки/ворог/putlers/putler-{choice(range(4))}.png')
        )
        self.rect = self.image.get_rect()
        self.швидкість = 4 + дата.рівень
        self.mask = pygame.mask.from_surface(self.image)

        # ? Випадкова позиція появи (з 4 сторін)
        self.Вибрана_позиція = choice(('ліво', 'право', 'верх', 'низ'))

        # * Визначаємо центр спрайта (важливо int(...), щоб randint працював)
        if self.Вибрана_позиція == 'ліво':
            self.rect.center = (
                0,
                randint(self.Спрайт_розмір // 2, дата.Гра_висота - self.Спрайт_розмір // 2)
            )
        elif self.Вибрана_позиція == 'право':
            self.rect.center = (
                дата.Гра_ширина,
                randint(self.Спрайт_розмір // 2, дата.Гра_висота - self.Спрайт_розмір // 2)
            )
        elif self.Вибрана_позиція == 'верх':
            self.rect.center = (
                randint(self.Спрайт_розмір // 2, дата.Гра_ширина - self.Спрайт_розмір // 2),
                0
            )
        else:  # 'низ'
            self.rect.center = (
                randint(self.Спрайт_розмір // 2, дата.Гра_ширина - self.Спрайт_розмір // 2),
                дата.Гра_висота
            )

    def update(self):
        # ? робимо колір (0,0,0) прозорим
        self.image.set_colorkey((0, 0, 0))

        # ? Рух відповідно до вибраної позиції
        if self.Вибрана_позиція == 'ліво':
            self.rect.x += self.швидкість
        elif self.Вибрана_позиція == 'право':
            self.rect.x -= self.швидкість
        elif self.Вибрана_позиція == 'верх':
            self.rect.y += self.швидкість
        else:  # 'низ'
            self.rect.y -= self.швидкість


class вибух(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.i = 0
        self.index = 0
        папка_з_кадрами = "_/картинки/ворог/вибух/"
        кадри = [
            ф for ф in listdir(папка_з_кадрами)
            if isfile(join(папка_з_кадрами, ф))
        ]

        self.images = []
        for frame in кадри:
            self.images.append(pygame.image.load(join(папка_з_кадрами, frame)))

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        mousePos = pygame.mouse.get_pos()
        self.rect.x = mousePos[0] - 90
        self.rect.y = mousePos[1] - 115

    def update(self):
        # ? Якщо анімація «вибуху» дійшла до кінця – видаляємо спрайт
        if self.index >= len(self.images):
            self.kill()
        else:
            self.image = self.images[self.index]

        # ? Невелике «сповільнення» анімації
        if self.i % 2 == 0:
            self.index += 1

        self.i += 1

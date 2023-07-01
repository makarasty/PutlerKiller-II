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

import pygame  # ? головна бібліотека
# ? функції які безліч разів використовуються в коді, закинув іх в інший файл щоб скоротити синтаксис
import налаштування as дата

from random import randint, choice
# ? randint Випадкова цифра віт - до
# ? choice Виберає випадковий елемент із не порожньої послідовності.

from os import listdir
# ? listdir все що знаходиться в папці
from os.path import isfile, join
# ? isfile перевіряє файл
# ? join з'єднує елементи


class путлер(pygame.sprite.Sprite):
    # ? Конструктор
    Вибрана_позиція = 'ліво'
    швидкість = 0
    Спрайт_розмір = 200

    def __init__(self):
        # ? дає сигнал для конструктору батьківського класу (Sprite)
        pygame.sprite.Sprite.__init__(self)
        # ? ініціалізувати картинку в Pygame
        self.image = pygame.image.load(join(
            дата.папка_з_датою, f'картинки/ворог/putlers/putler-{choice(range(4))}.png'))
        self.rect = self.image.get_rect()                   # ? дізнатись інформацію
        self.швидкість = 4 + дата.рівень                    # ? швидкість спрайта
        self.mask = pygame.mask.from_surface(
            self.image)    # ? маска для картики
        # ! Ворог з’явитися в 4 різних місцях на екрані і почине рухатися в 4 різних можливих місця
        self.Вибрана_позиція = choice(
            ('ліво', 'право', 'верх', 'низ'))  # ? випадкова позиція

        # * визначає центр спрайта
        if self.Вибрана_позиція == 'ліво':
            self.rect.center = (0, randint(
                self.Спрайт_розмір/2, дата.Гра_висота - self.Спрайт_розмір/2))
        elif self.Вибрана_позиція == 'право':
            self.rect.center = (дата.Гра_ширина, randint(
                self.Спрайт_розмір/2,  дата.Гра_висота - self.Спрайт_розмір/2))
        elif self.Вибрана_позиція == 'верх':
            self.rect.center = (
                randint(self.Спрайт_розмір/2, дата.Гра_ширина - self.Спрайт_розмір/2), 0)
        else:
            self.rect.center = (randint(
                self.Спрайт_розмір/2, дата.Гра_ширина - self.Спрайт_розмір/2), дата.Гра_висота)

    def update(self):
        # ? робимо фон від еффекту пострілу порожнім \ ніяким
        self.image.set_colorkey((0, 0, 0))
        # * направляє спрайт в певну сторону зі швидкостю
        if self.Вибрана_позиція == 'ліво':
            self.rect.x += self.швидкість
        elif self.Вибрана_позиція == 'право':
            self.rect.x -= self.швидкість
        elif self.Вибрана_позиція == 'верх':
            self.rect.y += self.швидкість
        else:
            self.rect.y -= self.швидкість


class вибух(pygame.sprite.Sprite):
    # ? Конструктор
    def __init__(self):
        # ? дає сигнал для конструктору батьківського класу (Sprite)
        pygame.sprite.Sprite.__init__(self)
        self.i = 0  # ? лічильник
        self.index = 0  # ? ініціалізувати індекс

        папка_з_кадрами = "_/картинки/ворог/вибух/"  # ? розташування папки з кадрами
        кадри = [
            # ? створюємо масив зі всіми кадрами в папці
            ф for ф in listdir(папка_з_кадрами) if isfile(join(папка_з_кадрами, ф))
        ]

        self.images = []
        # ? ініціалізувати список кадрів в Pygame
        for frame in кадри:
            self.images.append(pygame.image.load(папка_з_кадрами + frame))

        # ? вибираємо кадр з масиву по індексу
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()   # ? дізнатись інформацію

        mousePos = pygame.mouse.get_pos()  # ? беремо позицію миши користувача (x, y)
        self.rect.x = mousePos[0] - 90
        self.rect.y = mousePos[1] - 115

    def update(self):
        # ? Анімувати і вбити після анімації
        if self.index >= len(self.images):
            self.kill()
        else:
            self.image = self.images[self.index]

        if self.i % 2 == 0:     # ? Це сповільнить анімацію
            self.index += 1     # ? збільшуєм індекс на 1
        self.i += 1             # ? i += 1

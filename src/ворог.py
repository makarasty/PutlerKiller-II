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
        self.image = pygame.image.load(
            join(дата.папка_з_датою, f'картинки/ворог/putlers/putler-{choice(range(5))}.png')
        )
        self.rect = self.image.get_rect()
        self.швидкість = 4 + дата.рівень
        self.mask = pygame.mask.from_surface(self.image)

        self.Вибрана_позиція = choice(('ліво', 'право', 'верх', 'низ'))

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
        self.image.set_colorkey((0,0,0))
        if self.Вибрана_позиція == 'ліво':
            self.rect.x += self.швидкість
        elif self.Вибрана_позиція == 'право':
            self.rect.x -= self.швидкість
        elif self.Вибрана_позиція == 'верх':
            self.rect.y += self.швидкість
        else:
            self.rect.y -= self.швидкість

class вибух(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.i = 0
        self.index = 0
        папка_з_кадрами = join(дата.папка_з_датою, "картинки/ворог/вибух/")
        кадри = [
            ф for ф in listdir(папка_з_кадрами) if isfile(join(папка_з_кадрами, ф))
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
        if self.index >= len(self.images):
            self.kill()
            return
        self.image = self.images[self.index]
        self.image.set_colorkey((0,0,0))

        if self.i % 2 == 0:
            self.index += 1
        self.i += 1

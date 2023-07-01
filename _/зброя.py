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

from os import listdir
# ? listdir все що знаходиться в папці
from os.path import isfile, join
# ? isfile перевіряє файл
# ? join з'єднує елементи

# * спрайт прицілу


class приціл(pygame.sprite.Sprite):
    # ? Конструктор
    def __init__(self):
        # ? дає сигнал для конструктору батьківського класу (Sprite)
        pygame.sprite.Sprite.__init__(self)

        self.x = 16  # ? ініціалізуємо х
        self.y = 16  # ? ініціалізуємо у

        # ? ініціалізувати картинку в Pygame
        self.image = pygame.image.load(
            join(дата.папка_з_датою, 'картинки\приціл.png'))
        self.rect = self.image.get_rect()  # ? дізнатись інформацію

    def update(self):
        миш = pygame.mouse.get_pos()  # ? беремо позицію миши користувача (x, y)
        # ? задати кординату х обьекта кординаті х миши
        self.rect.x = миш[0] - self.x
        # ? задати кординату у обьекта кординаті у миши
        self.rect.y = миш[1] - self.y

# * спрайт зброї


class зброя(pygame.sprite.Sprite):
    # ? Конструктор
    def __init__(self):
        # ? дає сигнал для конструктору батьківського класу (Sprite)
        pygame.sprite.Sprite.__init__(self)

        self.боєзапас = дата.Максимальний_боєзапас  # ? ініціалізувати боєзапас

        # ? ініціалізувати картинку в Pygame
        self.image = pygame.image.load(
            join(дата.папка_з_датою, 'картинки\зброя.png'))
        self.rect = self.image.get_rect()  # ? дізнатись інформацію

    def update(self):
        # ? беремо позицію миши користувача (x, y)
        миш = pygame.mouse.get_pos()

        # ? задати кординату х обьекта кординаті х миши
        self.rect.x = миш[0] + 80

        # ? переносить зброю на низ екрану, відносно миші
        self.rect.y = дата.Гра_висота - 245 - (миш[1] / -5)


# * спрайт еффекту пострілу


class постріл(pygame.sprite.Sprite):
    # ? Конструктор
    def __init__(self):
        # ? дає сигнал для конструктору батьківського класу (Sprite)
        pygame.sprite.Sprite.__init__(self)

        self.images = []  # ? ініціалізувати масив з кадрами
        self.index = 0    # ? ініціалізувати індекс
        self.i = 0        # ? ініціалізувати і

        розташування = "_/картинки/постріл/"  # ? розташування папки з кадрами
        масив_кадри = [
            # ? створюємо масив зі всіми кадрами в папці
            ф for ф in listdir(розташування) if isfile(join(розташування, ф))
        ]

        # ? ініціалізувати список кадрів в Pygame
        for кадр in масив_кадри:
            self.images.append(pygame.image.load(розташування + кадр))

        self.image = self.images[self.index]  # ? вибрати перший кадр
        self.rect = self.image.get_rect()     # ? дізнатись інформацію

        # ? Позиція еффекту вибуху коли відбуваеться постріл
        миш = pygame.mouse.get_pos()  # ? беремо позицію миши користувача (x, y)
        # ? додає та розташовує еффект правильно
        self.rect.x = миш[0] + 170
        # ? переносить еффект пострілу на низ екрану, відносно миші
        self.rect.y = дата.Гра_висота - 270 - (миш[1] / -5)

    def update(self):
        # ? перевіряємо якщо індекс більше суми кадрів в масиві
        if self.index >= len(self.images):
            self.kill()  # ? вбити обьєект (себе)
        else:
            # ? вибираємо кадр з масиву по індексу
            self.image = self.images[self.index]
            # ? робимо фон від еффекту пострілу порожнім \ ніяким
            self.image.set_colorkey((0, 0, 0))

            if self.i % 2 == 0:  # ? Це сповільнить анімацію
                self.index += 1  # ? збільшуєм індекс на 1
            self.i += 1          # ? i += 1

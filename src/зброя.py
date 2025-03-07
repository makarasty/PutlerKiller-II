import pygame
import налаштування as дата
from os.path import join, isfile
from os import listdir

class приціл(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 16
        self.y = 16
        self.image = pygame.image.load(join(дата.папка_з_датою, 'картинки/приціл.png'))
        self.rect = self.image.get_rect()

    def update(self):
        миш = pygame.mouse.get_pos()
        self.rect.x = int(миш[0] * дата.mouse_sens) - self.x
        self.rect.y = int(миш[1] * дата.mouse_sens) - self.y
        self.image.set_colorkey((0, 0, 0))

class зброя(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.боєзапас = дата.Максимальний_боєзапас
        self.image = pygame.image.load(join(дата.папка_з_датою, 'картинки/зброя.png'))
        self.rect = self.image.get_rect()

    def update(self):
        миш = pygame.mouse.get_pos()
        base_x = int(миш[0] * дата.mouse_sens)
        base_y = int(миш[1] * дата.mouse_sens)
        self.rect.x = base_x + 80
        self.rect.y = дата.СИСТЕМА_висота - 245 - int(base_y * 0.05)

class постріл(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = []
        self.index = 0
        self.i = 0
        шлях = join(дата.папка_з_датою, "картинки/постріл/")
        кадри = [f for f in listdir(шлях) if isfile(join(шлях, f))]
        for ф in кадри:
            img = pygame.image.load(join(шлях, ф))
            self.images.append(img)

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        миш = pygame.mouse.get_pos()
        x_mouse = int(миш[0] * дата.mouse_sens)
        # Невеликий паралакс
        y_mouse = int(миш[1] * дата.mouse_sens * 0.05)
        self.rect.x = x_mouse + 170
        self.rect.y = дата.СИСТЕМА_висота - 270 - y_mouse

    def update(self):
        if self.index >= len(self.images):
            self.kill()
        else:
            self.image = self.images[self.index]
            self.image.set_colorkey((0, 0, 0))
            if self.i % 2 == 0:
                self.index += 1
            self.i += 1

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
        mouse_x, mouse_y = pygame.mouse.get_pos()
        offset_factor = 0.5
        offset_x = int((mouse_x - (дата.Гра_ширина / 2)) * offset_factor)
        offset_y = int((mouse_y - (дата.Гра_висота / 2)) * offset_factor)
        default_margin_x = 50
        if дата.Гра_ширина > 1920:
            default_margin_x = (дата.Гра_ширина - 1920) // 2 + 50
        baseline_x = дата.Гра_ширина - self.image.get_width() - default_margin_x
        baseline_y = дата.Гра_висота - int(self.image.get_height() * 0.9)
        new_x = baseline_x + offset_x
        new_y = baseline_y + offset_y
        if new_y < baseline_y:
            new_y = baseline_y
        self.rect.x = new_x
        self.rect.y = new_y

class постріл(pygame.sprite.Sprite):
    def __init__(self, weapon_rect):
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
        # Позиціювання пострілу відносно зброї.
        # Налаштуйте offset_x та offset_y під ваше зображення зброї.
        offset_x = -82
        offset_y = 82
        self.rect.centerx = weapon_rect.centerx + offset_x
        self.rect.centery = weapon_rect.centery - offset_y

    def update(self):
        if self.index >= len(self.images):
            self.kill()
        else:
            self.image = self.images[self.index]
            self.image.set_colorkey((0, 0, 0))
            if self.i % 4 == 0:
                self.index += 1
            self.i += 1

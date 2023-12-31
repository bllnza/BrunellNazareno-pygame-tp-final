import pygame
from constantes import *
from auxiliar import Auxiliar


class Plataforma():
    def __init__(self, x, y, w, h, type = 0) -> None:
        self.image = pygame.image.load('assets\platform\platform.png')
        self.image = pygame.transform.scale(self.image, (w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect_ground_collition = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, GROUND_RECT_H)


    def draw(self, screen):
        if (DEBUG):
            pygame.draw.rect(screen, ROJO, self.rect)
        screen.blit(self.image, self.rect)
        if (DEBUG):
            pygame.draw.rect(screen, VERDE, self.rect_ground_collition)
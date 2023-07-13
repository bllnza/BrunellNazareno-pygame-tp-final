import pygame


class Proyectil:
    def __init__(self, path, x, y) -> None:
        self.imagen = pygame.image.load(path)
        self.rect = self.imagen.get_rect()
        self.velocidadDisparo = 5
        self.rect.y = y
        self.rect.x = x

    def trayectoria(self):
        self.rect.x = self.rect.x + self.velocidadDisparo


    def draw(self, screen):
        screen.blit(self.imagen, self.rect)
    

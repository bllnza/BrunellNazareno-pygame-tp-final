import pygame
from constantes import *
from auxiliar import Auxiliar
from proyectil import Proyectil
from random import randint


class Enemigo:
    def __init__(self, x, y, gravity, frame_rate, move_rate, direction):
        self.stay_right = Auxiliar.getSurfaceFromSpriteSheet("assets\spritesheets\enemies\stay.png", 5, 1)
        self.stay_left = Auxiliar.getSurfaceFromSpriteSheet("assets\spritesheets\enemies\stay.png", 5, 1, True)
        self.frame = 0
        self.mover_x = 0
        self.mover_y = 0
        self.gravity = gravity
        self.direction = direction
        if self.direction == DIRECTION_L:
            self.animation = self.stay_left
        elif self.direction == DIRECTION_R:
            self.animation = self.stay_right
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tiempo_transcurrido = 0
        self.frate_rate_ms = frame_rate
        self.tiempo_transcurrido_move = 0
        self.move_rate = move_rate
        self.tiempo_transcurrido_animation = 0
        self.shoot_timer = 0
        
        self.rect_ground_collition = pygame.Rect(self.rect.x + self.rect.w / 4, self.rect.y + self.rect.h - GROUND_RECT_H, self.rect.w / 2, GROUND_RECT_H)

        self.lista_disparo = []
        self.sonido_disparo = pygame.mixer.Sound('assets/sounds/disparoe.wav')




    def stay(self):
        if self.animation != self.stay_right and self.animation != self.stay_left:
            if self.direction == DIRECTION_R:
                self.animation = self.stay_right
            else:
                self.animation = self.stay_left
            self.mover_x = 0
            self.mover_y = 0
            self.frame = 0
    


    def ataque(self):
        if self.shoot_timer >= 1500:
            self.shoot()
            self.shoot_timer = 0

    def shoot(self):
        x,y = self.rect.center
        if self.direction == DIRECTION_R:
                disparo = Proyectil('assets\proyectiles\proyectilenemigo.png',x, y - 20)
        else:
                disparo = Proyectil('assets\proyectiles\proyectilenemigo.png',x - self.rect.w, y - 20)
                disparo.velocidadDisparo *= -1 
        self.lista_disparo.append(disparo)
        self.sonido_disparo.play()

    def do_movement(self, lista_plataformas):

            self.add_y(self.mover_y)

            if (not self.is_on_platform(lista_plataformas)):
                self.add_y(self.gravity)



    def is_on_platform(self, lista_plataformas):
        retorno = False
        if(self.rect.y >= GROUND_LEVEL):
            retorno = True
        else:
            for plataforma in lista_plataformas:
                if(self.rect_ground_collition.colliderect(plataforma.rect_ground_collition)):
                    retorno = True
                    break
        return retorno
    

    def add_x(self, delta_x):
        self.rect.x += delta_x
        self.rect_ground_collition.x += delta_x
    def add_y(self, delta_y):
        self.rect.y += delta_y
        self.rect_ground_collition.y += delta_y



    def do_animation(self, delta_ms):
        self.ataque()
        self.tiempo_transcurrido_animation += delta_ms
        self.shoot_timer += delta_ms
        if self.tiempo_transcurrido_animation >= self.frate_rate_ms:
            self.tiempo_transcurrido_animation = 0

            if(self.frame < len(self.animation) - 1):
                self.frame += 1
            else:
                self.frame = 0
            
            

    
    def update(self, delta_ms, lista_plataformas):
        self.do_movement(lista_plataformas)
        self.do_animation(delta_ms)

    def draw(self, screen):
        if (DEBUG):
            pygame.draw.rect(screen, ROJO, self.rect)
            pygame.draw.rect(screen, VERDE, self.rect_ground_collition)
        self.image = self.animation[self.frame]
        screen.blit(self.image, self.rect)
        

def cargar_enemigos(lista_enemigos, x, y, gravity, frame_rate, move_rate, direction):
    enemigo = Enemigo(x, y, gravity, frame_rate, move_rate, direction)
    lista_enemigos.append(enemigo)
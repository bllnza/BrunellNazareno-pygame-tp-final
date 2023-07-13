import pygame
from constantes import *
from auxiliar import Auxiliar
from proyectil import Proyectil


class Player:
    def __init__(self, x, y, speed_walk, gravity, jump, frame_rate, move_rate) -> None:
        self.walk_right = Auxiliar.getSurfaceFromSpriteSheet("assets/spritesheets/walk.png", 11, 1)
        self.walk_left = Auxiliar.getSurfaceFromSpriteSheet("assets/spritesheets/walk.png", 11, 1, True)
        self.stay_right = Auxiliar.getSurfaceFromSpriteSheet("assets/spritesheets/stay.png", 4, 1)
        self.stay_left = Auxiliar.getSurfaceFromSpriteSheet("assets/spritesheets/stay.png", 4, 1, True)
        self.jump_right = Auxiliar.getSurfaceFromSpriteSheet("assets/spritesheets/jump.png", 7, 1, False, 2)
        self.jump_left = Auxiliar.getSurfaceFromSpriteSheet("assets/spritesheets/jump.png", 7, 1, True, 2)
        self.frame = 0
        self.score = 0
        self.mover_x = 0
        self.mover_y = 0
        self.speed_walk = speed_walk
        self.gravity = gravity
        self.jump_distance = jump
        self.animation = self.stay_right
        self.direction = DIRECTION_R
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isjump = False
        self.tiempo_transcurrido = 0
        self.frate_rate_ms = frame_rate
        self.tiempo_transcurrido_move = 0
        self.move_rate = move_rate
        self.tiempo_transcurrido_animation = 0
        self.y_start_jump = 0
        
        self.rect_ground_collition = pygame.Rect(self.rect.x + self.rect.w / 4, self.rect.y + self.rect.h - GROUND_RECT_H, self.rect.w / 2, GROUND_RECT_H)
        self.lista_disparo = []
        self.sonido_disparo = pygame.mixer.Sound('assets\sounds\disparop.wav')
        self.win_flag = False


    def walk(self, direction):
        if(self.direction != direction or (self.animation != self.walk_right and self.animation != self.walk_left)):
            self.frame = 0
            self.direction = direction
            if direction == DIRECTION_R:
                self.mover_x = self.speed_walk
                self.animation = self.walk_right
            else:
                self.mover_x = -self.speed_walk
                self.animation = self.walk_left
               

    def jump(self, on_off = True):
        if on_off and self.isjump == False:
            self.y_start_jump = self.rect.y
            if self.direction == DIRECTION_R:
                self.mover_x = self.speed_walk
                self.mover_y = -self.jump_distance
                self.animation = self.jump_right
            else:
                self.mover_x = -self.speed_walk
                self.mover_y = -self.jump_distance
                self.animation = self.jump_left
            self.frame = 0 
            self.isjump = True
        if(on_off == False):
            self.isjump = False
            self.stay()

    def stay(self):
        if self.animation != self.stay_right and self.animation != self.stay_left:
            if self.direction == DIRECTION_R:
                self.animation = self.stay_right
            else:
                self.animation = self.stay_left
            self.mover_x = 0
            self.mover_y = 0
            self.frame = 0

    def shoot(self):
        x,y = self.rect.center
        if self.direction == DIRECTION_R:
            disparo = Proyectil('assets/proyectiles/proyectil.png', x, y - 20)  # Disparo hacia la derecha
        else:
            disparo = Proyectil('assets/proyectiles/proyectil.png',x - self.rect.w, y - 20)
            disparo.velocidadDisparo *= -1  # Disparo hacia la izquierda
        self.lista_disparo.append(disparo)
        self.sonido_disparo.play()



    def do_movement(self, delta_ms, lista_plataformas):
        if self.win_flag == False:
            self.tiempo_transcurrido_move += delta_ms
            if self.tiempo_transcurrido_move >= self.move_rate:
                if abs(self.y_start_jump) - abs(self.rect.y) > self.jump_distance and self.isjump:
                    self.mover_y = 0
                self.tiempo_transcurrido_move = 0
                self.add_x(self.mover_x)
                self.add_y(self.mover_y)

                if (not self.is_on_platform(lista_plataformas)):
                    self.add_y(self.gravity)
                elif self.isjump:
                    self.jump(False)

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
        self.tiempo_transcurrido_animation += delta_ms
        if self.tiempo_transcurrido_animation >= self.frate_rate_ms:
            self.tiempo_transcurrido_animation = 0

            if(self.frame < len(self.animation) - 1):
                self.frame += 1
            else:
                self.frame = 0
            
            

    
    def update(self, delta_ms, lista_plataformas):
        self.do_movement(delta_ms, lista_plataformas)
        self.do_animation(delta_ms)


    def draw(self, screen):
        if (DEBUG):
            pygame.draw.rect(screen, ROJO, self.rect)
            pygame.draw.rect(screen, VERDE, self.rect_ground_collition)
        self.image = self.animation[self.frame]
        screen.blit(self.image, self.rect)
        



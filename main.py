import pygame
import sys
from constantes import *
from player import Player
from plataforma import Plataforma
from enemigo import *
from nivel import *



screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

pygame.init()
clock = pygame.time.Clock()
imagen_fondo = pygame.image.load("assets/background/bglevel1.png")
imagen_fondo = pygame.transform.scale(imagen_fondo,((ANCHO_VENTANA, ALTO_VENTANA)))
pygame.mixer.music.load('assets/sounds/bgmusic.wav')
pygame.mixer.music.play(3)

font = pygame.font.SysFont('Arial', 30)
text = font.render('Fin del juego', 0,(VERDE))

nivel_actual = 1

player, plataformas, enemigos = cargar_nivel(nivel_actual)

en_juego = True



reloj = pygame.time.Clock()
while True:
    
    
    reloj.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                player.shoot()

    if en_juego:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            player.walk(DIRECTION_L)
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            player.walk(DIRECTION_R)
        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not keys[pygame.K_SPACE]:
            player.stay()
        if keys[pygame.K_RIGHT] and keys[pygame.K_LEFT] and not keys[pygame.K_SPACE]:
            player.stay()
        if keys[pygame.K_SPACE]:
            player.jump(True)

        delta_ms = clock.tick(FPS)
        screen.blit(imagen_fondo, imagen_fondo.get_rect())


        for plataforma in plataformas:
            plataforma.draw(screen)

        if len(player.lista_disparo) > 0:
            for i in player.lista_disparo:
                i.draw(screen)
                i.trayectoria()
                for enemigo in enemigos:
                    if i.rect.colliderect(enemigo.rect):
                        enemigos.remove(enemigo)
                        player.lista_disparo.remove(i)

        if len(enemigos) > 0:
            for enemigo in enemigos:
                if len(enemigo.lista_disparo) > 0:
                    for i in enemigo.lista_disparo:
                        i.draw(screen)
                        i.trayectoria()
                        if i.rect.colliderect(player.rect):
                            en_juego = False
                            player.win_flag = True
                        else:
                            for disparo in player.lista_disparo:
                                if i.rect.colliderect(disparo.rect):
                                    player.lista_disparo.remove(disparo)
                                    enemigo.lista_disparo.remove(i)
                enemigo.update(delta_ms, plataformas)
                enemigo.draw(screen)

                if enemigo.rect.colliderect(player.rect):
                    en_juego = False
                    player.win_flag = True
        else:
            en_juego = False
            player.win_flag = True
            nivel_actual += 1
            if nivel_actual <= TOTAL_NIVELES:
                # Cargar el siguiente nivel
                player, plataformas, enemigos = cargar_nivel(nivel_actual)
                en_juego = True
            else:
                # Fin del juego
                pygame.mixer.music.fadeout(3000)
                screen.blit(text, (300, 300))
                pygame.display.flip()
                pygame.time.wait(3000)  # Esperar 3 segundos antes de salir del juego
                pygame.quit()
                sys.exit()
        
        
        player.update(delta_ms, plataformas)
        player.draw(screen)

    if not en_juego:
        pygame.mixer.music.fadeout(1000)
        screen.blit(text, (300, 300))
        pygame.display.flip()
        pygame.time.wait(2000)

        nivel_actual = 1
        player, plataformas, enemigos = cargar_nivel(nivel_actual)
        en_juego = True
        pygame.mixer.music.play(3)

    pygame.display.flip()
from constantes import *
from plataforma import Plataforma
from enemigo import *
from player import Player

def cargar_nivel(nivel):
    player = Player(0, 380, 8, 8, 50, 80, 80)

    plataformas = []
    if nivel == 1:
        plataformas.append(Plataforma(70, 340, 60, 20))
        plataformas.append(Plataforma(256, 360, 60, 20))
    elif nivel == 2:
        plataformas.append(Plataforma(0, 360, 60, 20))
        plataformas.append(Plataforma(256, 360, 60, 20))
        plataformas.append(Plataforma(384, 320, 60, 20))
    elif nivel == 3:
        plataformas.append(Plataforma(0, 360, 60, 20))
        plataformas.append(Plataforma(128, 340, 60, 20))
        plataformas.append(Plataforma(256, 320, 60, 20))
        plataformas.append(Plataforma(384, 300, 60, 20))

    enemigos = []
    if nivel == 1:
        cargar_enemigos(enemigos, 70, 0, 6, 50, 80, DIRECTION_R)
    elif nivel == 2:
        cargar_enemigos(enemigos, 256, 0, 6, 50, 80, DIRECTION_L)
        cargar_enemigos(enemigos, 384, 0, 6, 50, 80, DIRECTION_L)
    elif nivel == 3:
        cargar_enemigos(enemigos, 128, 0, 6, 50, 80, DIRECTION_R)
        cargar_enemigos(enemigos, 384, 0, 6, 50, 80, DIRECTION_L)

    return player, plataformas, enemigos

import pygame as pg
import sys

def fin_juego()
    pg.quit()
    sys.exit()

pg.init()
pantalla = pg.display.set_mode((600, 400))
pg.display.set_caption("Hola")

game_over = False

while not game_over:
    # Gestion de eventos
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            game_over = True

    # Gestion del estado  
    print("Hola mundo")

    # Refrescar pantalla

    pantalla.fill((0, 255, 0))
    pg.display.flip()

fin_juego()
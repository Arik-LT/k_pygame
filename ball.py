import pygame as pg
import sys
from random import randint


ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
BLACK = [0, 0, 0]
ANCHO = 800
ALTO = 600

pg.init()
pantalla = pg.display.set_mode((ANCHO, ALTO))
reloj = pg.time.Clock()

class Bola():
    def __init__(self, x, y ,vx = 5, vy = 5, color = (255, 255, 255), radio=10):
        self.x = x 
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.radio = radio

    def actualizar(self):
        self.x += self.vx
        self.y += self.vy

        if self.y <= 0 or self.y >= ALTO:
            self.vy = -self.vy
    
        if self.x <= 0 or self.x >= ANCHO:
            self.vx = -self.vx

    
    def dibujar(self, pantalla):
        pg.draw.circle(pantalla, self.color, (self.x, self.y), self.radio)


ranges =[randint(-10, -5), randint(5, 10)]
bolas = []
for _ in range(10):
    bola = Bola(randint(0, ANCHO), 
                randint(0, ALTO),
                (ranges[randint(0,1)]),
                (ranges[randint(0,1)]),
                (randint(0, 255), randint(0, 255), randint(0, 255)))

    bolas.append(bola)

game_over = False
while not game_over:
    reloj.tick(120)
    # gestion de eventos
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            game_over = True

    # Modificacion de estado
    for bola in bolas:
        bola.actualizar()

    # Gestion de la pantalla
    pantalla.fill(BLACK)
    for bola in bolas:
        bola.dibujar(pantalla)

    pg.display.flip()

pg.quit()
sys.exit()
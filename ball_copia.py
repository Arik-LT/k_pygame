import pygame as pg
import sys
from random import randint, choice

ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ANCHO = 800
ALTO = 600

pg.init()
pantalla = pg.display.set_mode((ANCHO, ALTO))
reloj = pg.time.Clock()

class Bola():
    def __init__(self, x, y, vx=5, vy=5, color= (255, 255, 255), radio=10):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.anchura = radio*2
        self.altura = radio*2

    def actualizar(self):
        self.x += self.vx
        self.y += self.vy
        if self.y <=0:
            self.vy = -self.vy
        if self.x <=0 or self.x >=ANCHO:
            self.vx = -self.vx
        if self.y >=ALTO:
            self.x = ANCHO // 2
            self.y = ALTO // 2
            self.vx = randint(5,10)*choice([-1, 1])
            self.vy = randint(5,10)*choice([-1, 1])
            return True
        return False
    
    def dibujar(self, lienzo):
        pg.draw.circle(lienzo, self.color, (self.x, self.y), self.anchura//2)
    
    def comprueba_colision(self, objeto):
        choqueX = self.x >= objeto.x and self.x <= objeto.x+objeto.anchura or \
           self.x+self.anchura >= objeto.x and self.x+self.anchura <= objeto.x + objeto.anchura
        choqueY = self.y >= objeto.y and self.y <= objeto.y+objeto.altura or \
           self.y+self.altura >= objeto.y and self.y+self.altura <= objeto.y + objeto.altura
        if choqueX and choqueY:
            self.vy *= -1

class Raqueta():
    def __init__(self, x=0, y=0):
        self.altura = 10
        self.anchura = 100
        self.color = (255, 255, 255)
        self.x = (ANCHO - self.anchura) // 2
        self.y = ALTO - self.altura - 15
        self.vy = 0
        self.vx = 13

    def dibujar(self, lienzo):
        rect = pg.Rect(self.x, self.y, self.anchura, self.altura)
        pg.draw.rect(lienzo, self.color, rect)
    
    def actualizar(self):
        teclas_pulsadas = pg.key.get_pressed() 
        if teclas_pulsadas[pg.K_LEFT] and self.x > 0:
            self.x -= self.vx
        if teclas_pulsadas[pg.K_RIGHT] and self.x < ANCHO - self.anchura:
            self.x += self.vx

vidas = 3
#creacion de instancias
bola = Bola(randint(0, ANCHO),
            randint(0, ALTO),
            randint(5, 10)*choice([-1, 1]),
            randint(5, 10)*choice([-1, 1]),
            AZUL)
raqueta = Raqueta()

fuente = pg.font.SysFont("Arial", 35)

game_over = False
while not game_over and vidas > 0:
    
    v = reloj.tick(60)
    
    #Gestion de eventos
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            game_over = True
    
    # Modificación de estado
    raqueta.actualizar()
    pierdebola = bola.actualizar()
    if pierdebola:
        vidas -= 1
    bola.comprueba_colision(raqueta)

    # Gestión de la pantalla
    pantalla.fill(NEGRO)
    bola.dibujar(pantalla)
    raqueta.dibujar(pantalla)
    
    pg.display.flip()
    if pierdebola:
        if vidas == 0:
            texto = fuente.render("GAME OVER", True, BLANCO)
            pantalla.fill(NEGRO)
            pantalla.blit(texto, (300, 280))
            pg.display.flip()
            pg.time.delay(2000)
        else:
            pg.time.delay(500)

pg.quit()
sys.exit()
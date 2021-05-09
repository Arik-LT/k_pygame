import pygame as pg
import sys
import random
from enum import Enum

ANCHO = 800
ALTO = 600
FPS = 60

class Marcador(pg.sprite.Sprite):

    plantilla = "{}"

    def __init__(self, x, y, justificado = "topleft", fontsize=25, color=(255,255,255)):
        super().__init__()
        self.fuente = pg.font.Font(None, fontsize)
        self.text = ""
        self.color = color
        self.x = x
        self.y = y
        self.justificado = justificado
        self.image = None

    def update(self, dt):
        self.image = self.fuente.render(str(self.text), True, self.color)
        d = {self.justificado: (self.x, self.y)}
        self.rect = self.image.get_rect(**d)

class Ladrillo(pg.sprite.Sprite):
    disfraces = ["greenTile.png", "redTile.png", "redTileBreak.png"]

    def __init__(self, x, y, esDuro = False):
        super().__init__()
        self.imagenes = self.cargaImagenes()
        self.esDuro = esDuro
        self.imagen_actual = 1 if self.esDuro else 0
        self.image = self.imagenes[self.imagen_actual]
        self.rect = self.image.get_rect(topleft = (x,y))
        self.numGolpes = 0    
    
    def cargaImagenes(self):
        imagenes = []
        for fichero in self.disfraces:
            imagenes.append(pg.image.load("assets_ball/{}".format(fichero)))
        return imagenes

    def update(self, dt):
        if self.esDuro and self.numGolpes == 1:
            self.imagen_actual = 2
            self.image = self.imagenes[self.imagen_actual]

    def desaparece (self):
        self.numGolpes += 1
        return self.numGolpes > 0 and not self.esDuro or self.numGolpes > 1 and self.esDuro
            
class Raqueta(pg.sprite.Sprite):
    disfraces = ['electric00.png', 'electric01.png', 'electric02.png']

    def __init__(self, x, y):

        super().__init__()
        self.imagenes = self.cargaImagenes()
        self.imagen_actual = 0
        self.milisegundos_para_cambiar = 1000 // FPS * 5
        self.milisegundos_acumulados = 0
        self.image = self.imagenes[self.imagen_actual]
        self.rect = self.image.get_rect(centerx = x, bottom = y)
        self.vx = 7

    def cargaImagenes(self):
        imagenes = []
        for fichero in self.disfraces:
            imagenes.append(pg.image.load("assets_ball/{}".format(fichero)))
        return imagenes

    def update(self, dt):
        teclas_pulsadas = pg.key.get_pressed()

        if teclas_pulsadas[pg.K_LEFT]:
            self.rect.x -= self.vx

        if teclas_pulsadas[pg.K_RIGHT]:
            self.rect.x += self.vx

        if self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.right >= ANCHO:
            self.rect.right = ANCHO

        self.milisegundos_acumulados += dt
        if self.milisegundos_acumulados >= self.milisegundos_para_cambiar:
            self.imagen_actual += 1

            if self.imagen_actual >= len(self.disfraces):
                self.imagen_actual = 0
            self.milisegundos_acumulados = 0
        self.image = self.imagenes[self.imagen_actual]

class Bola(pg.sprite.Sprite):
    disfraces = ["ball1.png", "ball2.png", "ball3.png", "ball4.png", "ball5.png", "ball5.png", "ball5.png"]

    class Estado(Enum):
        viva = 0
        agonizando = 1
        muerta = 2

    def __init__(self, x, y,):
        super().__init__()
        self.imagenes = self.cargaImagenes()
        self.imagen_actual = 0
        self.image = self.imagenes[self.imagen_actual]

        self.milisegundos_acumulados = 0
        self.milisegundos_para_cambiar = 1000 // FPS * 4
        
        self.rect = self.image.get_rect(center=(x,y))
        self.xOriginal = x
        self.yOriginal = y
        self.estado = Bola.Estado.viva

        self.vx = random.randint(5, 10) * random.choice([-1, 1])
        self.vy = random.randint(5, 10) * random.choice([-1, 1])

    def prueba_colision(self, grupo):
        candidatos = pg.sprite.spritecollide(self, grupo, False)
        if len(candidatos) > 0:
            self.vy *= -1
        
    def prueba_colision(self, grupo):
        candidatos = pg.sprite.spritecollide(self, grupo, False)
        if len(candidatos) > 0:
            self.vy *= -1
        return candidatos

    def cargaImagenes(self):
            imagenes = []
            for fichero in self.disfraces:
                imagenes.append(pg.image.load("assets_ball/{}".format(fichero)))
            return imagenes

    def update(self, dt):
        if self.estado == Bola.Estado.viva:
            self.rect.x += self.vx
            self.rect.y += self.vy
            if self.rect.left <= 0 or self.rect.right >= ANCHO:
                self.vx *= -1 
            if self.rect.top <= 0:
                self.vy *= -1
            if self.rect.bottom >= ALTO:
                self.estado = Bola.Estado.agonizando
                self.rect.bottom = ALTO

        elif self.estado == Bola.Estado.agonizando:
            self.milisegundos_acumulados += dt
            if self.milisegundos_acumulados >= self.milisegundos_para_cambiar:
                self.imagen_actual += 1
                self.milisegundos_acumulados = 0

                if self.imagen_actual >= len(self.disfraces):
                    self.estado = Bola.Estado.muerta
                    self.imagen_actual = 0
                self.image = self.imagenes[self.imagen_actual]

        else:
            self.rect.center = (self.xOriginal, self.yOriginal)
            self.vx = random.randint(5, 10) * random.choice([-1, 1])
            self.vy = random.randint(5, 10) * random.choice([-1, 1])
            self.estado = Bola.Estado.viva

class Game(): 
    def __init__(self):
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        self.vidas = 3
        self.puntuacion = 0
        self.game_state = "intro"

        self.todoGrupo = pg.sprite.Group()
        self.grupoJugador = pg.sprite.Group()
        self.grupoLadrillos = pg.sprite.Group()

        for fila in range(4):
            for columna in range(8):
                x = columna * 100 + 5
                y = fila * 40 + 5
                esDuro = random.randint(1,5) == 1
                ladrillo = Ladrillo (x, y, esDuro)
                self.grupoLadrillos.add(ladrillo)

        self.cuentaPuntos = Marcador(10,10)
        self.cuentaVidas = Marcador(790, 10, "topright")
        self.intro_texto = Marcador(ANCHO//2, ALTO//2, "center", 50)
        
        self.fondo = pg.image.load("assets_ball/background.png")
        
        self.bola = Bola(ANCHO // 2, ALTO // 2) 
        self.todoGrupo.add(self.bola)    
        
        self.raqueta = Raqueta(x = ANCHO//2, y = ALTO - 40)
        self.grupoJugador.add(self.raqueta)

        self.todoGrupo.add(self.grupoJugador, self.grupoLadrillos)
        self.todoGrupo.add(self.cuentaPuntos, self.cuentaVidas)

    def bucle_principal(self):
        self.game_over = False
        self.reloj = pg.time.Clock()
        contador_milisegundos = 0
        segundero = 0

        while not self.game_over and self.vidas > 0: 
            game.state_manager()

    def intro(self):
        teclas_pulsadas = pg.key.get_pressed()
        ready_text = pg.image.load("assets_ball/text_ready.png")
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                self.game_over = True
            
            if teclas_pulsadas[pg.K_SPACE]:
                self.game_state = "main_game"
            
        self.pantalla.blit(self.fondo, (0,0))
        self.pantalla.blit(ready_text, (ANCHO//2 - 115, ALTO//2 - 33))
        pg.display.flip()

    def main_game(self):
        dt = self.reloj.tick(FPS)

        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                self.game_over = True

        self.cuentaPuntos.text = (f"Puntos: {self.puntuacion}")
        self.cuentaVidas.text = (f"Vidas: {self.vidas}")

        self.bola.prueba_colision(self.grupoJugador)
        
        tocados= self.bola.prueba_colision(self.grupoLadrillos)
        for ladrillo in tocados:
            self.puntuacion += 5
            if ladrillo.desaparece():
                self.grupoLadrillos.remove(ladrillo)
                self.todoGrupo.remove(ladrillo)

        self.todoGrupo.update(dt)

        if self.bola.estado == Bola.Estado.muerta:
            self.vidas -= 1

        self.pantalla.blit(self.fondo, (0,0))
        self.todoGrupo.draw(self.pantalla)
        
        pg.display.flip()

    def state_manager(self):
        if self.game_state == "intro":
            return self.intro()
        if self.game_state == "main_game":
            return self.main_game()


if __name__ == '__main__':
    pg.init()
    game = Game()
    game.bucle_principal()
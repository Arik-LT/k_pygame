import pygame as pg
import sys
import random

FPS = 60
WIDTH, HEIGHT = 800, 400

class Marcador():
    def __init__(self, x, y, fontsize = 25, color = (255,255,255)):
        self.fuente = pg.font.SysFont("Arial", fontsize)
        self.x = x
        self.y = y
        self.color = color

    def dibuja(self, text, lienzo):
        image = self.fuente.render(str(text), True, self.color)
        lienzo.blit(image, (self.x, self.y))


class Bola(pg.sprite.Sprite):
    def __init__ (self, x, y):
        super().__init__()
        self.image = pg.image.load("assets_ball/ball1.png")
        self.rect = self.image.get_rect(center = (x, y))

        self.vx = random.randint(5, 10) * random.choice([-1, 1])
        self.vy = random.randint(5, 10) * random.choice([-1, 1])

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.vx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vy *= -1

class Game():
    def __init__ (self):
        self.pantalla = pg.display.set_mode((WIDTH, HEIGHT))
        self.botes = 0
        self.cuentaGolpes = Marcador(10, 10)

        self.ballGroup = pg.sprite.Group()
        for ball in range(20):
            bola = Bola(random.randint(1, WIDTH), random.randint(1, HEIGHT))
            self.ballGroup.add(bola)

    def bucle_principal(self):
        clock = pg.time.Clock()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            pg.display.flip()
            self.ballGroup.update()
            self.pantalla.fill((0,0,0))
            self.cuentaGolpes.dibuja("hola", self.pantalla)
            self.ballGroup.draw(self.pantalla)
            clock.tick(FPS)



if __name__ == "__main__":
    pg.init()
    game = Game()
    game.bucle_principal()
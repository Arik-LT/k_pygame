import pygame
import sys
import random

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def shoot(self):
        pygame.sprite.spritecollide(crosshair, target_group, True)

class Target(pygame.sprite.Sprite):
    def __init__ (self, picture_path, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]



pygame.init()
clock = pygame.time.Clock()

# Game screen
WIDTH, HEIGHT = 1920, 1080
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("assets_Range/Stall/bg_blue.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
pygame.mouse.set_visible(False)

crosshair = Crosshair("assets_Range/HUD/crosshair_white_large.png")
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)


target_group = pygame.sprite.Group()
for target in range(20):
    new_target = Target("assets_Range/Objects/target_red1.png",
    random.randrange(0,WIDTH), random.randrange(0, HEIGHT))
    target_group.add(new_target)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if event.type == pygame.MOUSEBUTTONDOWN:
        crosshair.shoot()

    pygame.display.flip()
    screen.blit(background, (0,0))
    target_group.draw(screen)
    crosshair_group.draw(screen)
    crosshair_group.update()
    clock.tick(FPS)

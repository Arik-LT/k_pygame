import pygame, sys, random

#Game Variables
WIDTH, HEIGHT = 576, 1024
FPS = 120
gravity = 0.25
bird_movement = 0
GAME_ACTIVE = True

#operation needs
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#Functions
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos,900))
    screen.blit(floor_surface, (floor_x_pos + 576,900))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipe_list:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    if bird_rect.top <= 100 or bird_rect.bottom >= HEIGHT:
            return False

    return True

#surfaces
#Background
bg_surface = pygame.image.load("assetsFlappy/background-day.png").convert()
bg_surface = pygame.transform.scale2x(bg_surface)

#Floor & moving floor
floor_surface = pygame.image.load("assetsFlappy/base.png").convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

#bird
bird_surface = pygame.image.load("assetsFlappy/bluebird-midflap.png").convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center = (100, HEIGHT//2))

#Pipes
pipe_surface = pygame.image.load("assetsFlappy/pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1000)
pipe_height = [400, 600, 800]

#Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and GAME_ACTIVE:
                bird_movement = 0
                bird_movement -= 8
            if event.key == pygame.K_SPACE and GAME_ACTIVE == False:
                GAME_ACTIVE = True
                pipe_list.clear()
                bird_rect.center = (100,512)
                bird_movement = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    #Introducing screens in game
    screen.blit(bg_surface, (0, 0))

    if GAME_ACTIVE:
        #Bird movement
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_surface,bird_rect)
        GAME_ACTIVE = check_collision(pipe_list)

        #Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    #Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0
    
    
    pygame.display.update()
    clock.tick(FPS)

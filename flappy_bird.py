import pygame
import sys 
import random

pygame.init()

def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos-700))
    return bottom_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes

def draw_pipe(pipes):
    for pipe in pipes: 
        if pipe.bottom >= 700:
            screen.blit(pipe_surface, pipe)
        else: 
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True

def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement*3, 1) #xoay hình ảnh bird 1 góc nhất định theo tham số
    '''
        + bird1: ảnh bird
        + bird_movement (-/+)->chiều xoay, *3->góc
        + 1-> thay đổi độ dài co dãn
    '''
    return new_bird

screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
bg = pygame.image.load('img/bg.png').convert_alpha()
floor = pygame.image.load('img/ground.png').convert_alpha()
floor_x_pos = 0

bird = pygame.image.load('img/bird1.png').convert_alpha()
bird_rect = bird.get_rect(center=(100, 384))

gavity = 0.25
bird_movement = -7

pipe_surface = pygame.image.load('img/pipe.png').convert_alpha()
spawnpipe = pygame.USEREVENT

'''
    USEREVENT: tạo sự kiện người dùng tùy chỉnh
'''

pygame.time.set_timer(spawnpipe, 2000)
pipe_list = []
pipe_height = [300, 200, 400]

game_active = True

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = -7
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
    
    screen.blit(bg, (0,0))

    if game_active:
        bird_movement += gavity
        bird_rect.centery += bird_movement
        rotated_bird = rotate_bird(bird)
        screen.blit(rotated_bird, bird_rect)
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        game_active = check_collision(pipe_list)

    floor_x_pos -= 1
    draw_floor()

    if floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
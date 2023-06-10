import pygame as pg
import os
from sys import exit

pg.init()
pg.font.init()

FPS = 60
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 600

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Pong")

start_screen_surf = pg.image.load(os.path.join("OneDrive", "Desktop", "pong_game", "sprites", "start_screen.png"))
start_screen_surf_bigger = pg.transform.scale(start_screen_surf, (SCREEN_WIDTH, SCREEN_HEIGHT))

middle_line_surf = pg.image.load(os.path.join("OneDrive", "Desktop", "pong_game", "sprites", "middle_line.png"))

background_surf = pg.image.load(os.path.join("OneDrive", "Desktop", "pong_game", "sprites", "background.png"))
background_surf_bigger = pg.transform.scale(background_surf, (SCREEN_WIDTH, SCREEN_HEIGHT))

player01_surf = pg.image.load(os.path.join("OneDrive", "Desktop", "pong_game", "sprites", "player.png")).convert_alpha()
player01_rect = player01_surf.get_rect(center=(25, SCREEN_HEIGHT/2))

player02_surf = pg.image.load(os.path.join("OneDrive", "Desktop", "pong_game", "sprites", "player.png")).convert_alpha()
player02_rect = player01_surf.get_rect(center=(725, SCREEN_HEIGHT/2))

ball_surf = pg.image.load(os.path.join("OneDrive", "Desktop", "pong_game", "sprites", "ball.png")).convert_alpha()
ball_rect = ball_surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
ball_direction = [5, 5]

player_01_score = 0
player01_score_font = pg.font.SysFont("Arial", 60)
player01_score_surface = player01_score_font.render(f"{player_01_score}", False, (180,180,180))

player_02_score = 0
player02_score_font = pg.font.SysFont("Arial", 60)
player02_score_surface = player02_score_font.render(f"{player_02_score}", False, (180,180,180))

def ai_movement():
    if player02_rect.y != ball_rect.y:
        player02_rect.y = ball_rect.y

def increase_score():
    global player_01_score, player_02_score, player01_score_surface, player02_score_surface
    if ball_rect.x < 0:
        ball_rect.x, ball_rect.y = SCREEN_WIDTH/2, SCREEN_HEIGHT/2
        player_02_score += 1
        player02_score_surface = player02_score_font.render(f"{player_02_score}", False, (180,180,180))
        player01_rect.center = (25, SCREEN_HEIGHT/2)
        player02_rect.center = (725, SCREEN_HEIGHT/2)
    if ball_rect.x > 750:
        ball_rect.x, ball_rect.y = SCREEN_WIDTH/2, SCREEN_HEIGHT/2
        player_01_score += 1
        player01_score_surface = player01_score_font.render(f"{player_01_score}", False, (180,180,180))
        player01_rect.center = (25, SCREEN_HEIGHT/2)
        player02_rect.center = (725, SCREEN_HEIGHT/2)

def move_ball():
    ball_rect.x += ball_direction[0]
    ball_rect.y += ball_direction[1]

    if ball_rect.y >= SCREEN_HEIGHT - ball_rect.height or ball_rect.y <= 0:
        ball_direction[1] *= -1

def collision():
    if ball_rect.colliderect(player02_rect):
        ball_direction[0] *= -1
    if ball_rect.colliderect(player01_rect):
        ball_direction[0] *= -1

def player01_movement():
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        player01_rect.top -= 5
    if keys[pg.K_s]:
        player01_rect.bottom += 5

def player02_movement():
    keys = pg.key.get_pressed()
    if keys[pg.K_UP]:
        player02_rect.top -= 5
    if keys[pg.K_DOWN]:
        player02_rect.bottom += 5

def border():
    if player01_rect.bottom >= SCREEN_HEIGHT:
        player01_rect.bottom = SCREEN_HEIGHT
    if player01_rect.top <= 0:
        player01_rect.top = 0
    
    if player02_rect.bottom >= SCREEN_HEIGHT:
        player02_rect.bottom = SCREEN_HEIGHT
    if player02_rect.top <= 0:
        player02_rect.top = 0

def draw_window():
    screen.blit(background_surf_bigger, (0, 0))
    screen.blit(middle_line_surf, (SCREEN_WIDTH/2, 0))
    screen.blit(player01_surf, player01_rect)
    screen.blit(player02_surf, player02_rect)
    screen.blit(ball_surf, ball_rect)
    screen.blit(player01_score_surface, (SCREEN_WIDTH/4,0))
    screen.blit(player02_score_surface, (550,0))

start_screen = True
versus = False
ai_opponent = False

clock = pg.time.Clock()
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_v:
                versus = True
                start_screen = False
            if event.key == pg.K_a:
                ai_opponent = True
                start_screen = False

    if start_screen:
        screen.blit(start_screen_surf_bigger, (0,0))
        
    if versus == True:
        increase_score()
        collision()
        move_ball()
        border()
        player01_movement()
        player02_movement()
        draw_window()
    
    if ai_opponent == True:
        increase_score()
        collision()
        move_ball()
        border()
        ai_movement()
        player01_movement()
        draw_window()

    clock.tick(FPS)
    pg.display.update()
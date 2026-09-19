import pygame as pg
from sys import exit
import player
import render
import obstacles
import settings

pg.init()

PLAYER = player.PLAYER

window = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
pg.display.set_caption("DodgeIT")
clock = pg.time.Clock()
last_spawn_time = pg.time.get_ticks()
running = True

obstacles_list = []

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            exit()
    
    keys = pg.key.get_pressed()
    PLAYER.handle_input(keys)
    
    current_time = pg.time.get_ticks()
    if current_time - last_spawn_time > settings.NEW_OBS_MIN:
        obstacles.spawn_obstacle(obstacles_list)
        last_spawn_time = current_time
    
    window.fill(settings.BACKGROUND)
    render.draw_player(window, PLAYER)
    obstacles.update_obstacles(obstacles_list)
    render.draw_obstacles(window, obstacles_list)
    
    pg.display.flip()
    
    clock.tick(settings.FPS)
    
pg.quit
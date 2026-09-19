#Imports
import pygame as pg
from sys import exit
import player
import render
import obstacles
import settings

#Pygame
pg.init()

#Player
PLAYER = player.PLAYER

#Variables
window = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
pg.display.set_caption("DodgeIT")
clock = pg.time.Clock()
last_spawn_time = pg.time.get_ticks()
running = True
obstacles_list = []
background = pg.image.load(settings.BACKGROUND)
background = pg.transform.scale(background, (settings.WIDTH, settings.HEIGHT))

#Loop
while running:
    #Quit
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            exit()
    
    #input
    keys = pg.key.get_pressed()
    PLAYER.handle_input(keys)
    
    #Obstacles spawn
    current_time = pg.time.get_ticks()
    if current_time - last_spawn_time > settings.NEW_OBS_MIN:
        obstacles.spawn_obstacle(obstacles_list)
        last_spawn_time = current_time
    
    #Render
    window.blit(background, (0,0))
    render.draw_player(window, PLAYER)
    obstacles.update_obstacles(obstacles_list)
    render.draw_obstacles(window, obstacles_list)
    
    #Update
    pg.display.flip()
    clock.tick(settings.FPS)
    
pg.quit
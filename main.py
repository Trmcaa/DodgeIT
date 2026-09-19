#Imports
import pygame as pg
from sys import exit

pg.init()

import player
import render
import obstacles
import effects
import settings

#Player
PLAYER = player.PLAYER

#Variables
window = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
pg.display.set_caption("DodgeIT")
clock = pg.time.Clock()
running = True

background = pg.image.load(settings.BACKGROUND)
background = pg.transform.scale(background, (settings.WIDTH, settings.HEIGHT))

obstacles_list = []
active_effects = []
last_spawn_time = pg.time.get_ticks()

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
    PLAYER.animate()
    
    #Obstacles spawn
    current_time = pg.time.get_ticks()
    if current_time - last_spawn_time > settings.NEW_OBS_MIN:
        obstacles.spawn_obstacle(obstacles_list)
        last_spawn_time = current_time
    
    #Render
    landed_obstacles = obstacles.update_obstacles(obstacles_list)

    for obstacle in landed_obstacles:
        active_effects.append(
            effects.create_ground_effect((obstacle.rect.centerx, settings.HEIGHT))
        )

    for obstacle in obstacles_list[:]:
        if obstacle.rect.colliderect(PLAYER.rect):
            active_effects.append(effects.create_hit_effect(obstacle.rect.center))
            obstacles_list.remove(obstacle)

    for effect in active_effects:
        effect.update()
    active_effects[:] = [effect for effect in active_effects if not effect.finished]
    
    window.blit(background, (0,0))
    render.draw_player(window, PLAYER)
    render.draw_obstacles(window, obstacles_list)
    render.draw_effects(window, active_effects)
    
    #Update
    pg.display.flip()
    clock.tick(settings.FPS)
    
pg.quit
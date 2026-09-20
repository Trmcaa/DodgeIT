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
game_over = False
chaos_mode = False
game_over_time = 0
score_start_time = pg.time.get_ticks()
score = 0

#Loop
while running:
    #Quit
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            exit()
        if (
            event.type == pg.KEYDOWN
            and event.key == pg.K_RETURN
            and game_over
            and pg.time.get_ticks() - game_over_time >= settings.RESPAWN_DELAY
        ):
            obstacles_list.clear()
            active_effects.clear()
            PLAYER.rect.topleft = (settings.STARTING_POS_W, settings.STARTING_POS_H)
            PLAYER.set_animation("idle")
            PLAYER.last_update_time = pg.time.get_ticks()
            game_over = False
            chaos_mode = False
            score_start_time = pg.time.get_ticks()
            score = 0
            last_spawn_time = score_start_time
    
    current_time = pg.time.get_ticks()

    #input
    keys = pg.key.get_pressed()
    if not game_over:
        PLAYER.handle_input(keys)
        score = (current_time - score_start_time) // 1000
    PLAYER.animate()
    
    #Obstacles spawn
    if game_over and not chaos_mode and current_time - game_over_time >= settings.GAME_OVER_DELAY:
        chaos_mode = True
        last_spawn_time = current_time

    spawn_interval = settings.CHAOS_SPAWN_INTERVAL if chaos_mode else settings.NEW_OBS_MIN
    if (not game_over or chaos_mode) and current_time - last_spawn_time > spawn_interval:
        obstacles.spawn_obstacle(obstacles_list, chaos_mode)
        last_spawn_time = current_time
    
    #Render
    landed_obstacles = obstacles.update_obstacles(obstacles_list)

    for obstacle in landed_obstacles:
        active_effects.append(
            effects.create_ground_effect((obstacle.rect.centerx, settings.HEIGHT))
        )

    for obstacle in obstacles_list[:]:
        if not game_over and obstacle.rect.colliderect(PLAYER.rect):
            active_effects.append(effects.create_hit_effect(obstacle.rect.center))
            obstacles_list.remove(obstacle)
            game_over = True
            game_over_time = current_time
            score = (current_time - score_start_time) // 1000

    for effect in active_effects:
        effect.update()
    active_effects[:] = [effect for effect in active_effects if not effect.finished]
    
    window.blit(background, (0,0))
    render.draw_player(window, PLAYER)
    render.draw_obstacles(window, obstacles_list)
    render.draw_effects(window, active_effects)
    render.draw_score(window, score)
    if game_over:
        respawn_ready = current_time - game_over_time >= settings.RESPAWN_DELAY
        render.draw_game_over(window, chaos_mode, respawn_ready)
    
    #Update
    pg.display.flip()
    clock.tick(settings.FPS)
    
pg.quit
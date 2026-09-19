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
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            exit()
    
    keys = pg.key.get_pressed()
    PLAYER.handle_input(keys)
    
    window.fill(settings.BACKGROUND)
    render.draw_player(window, PLAYER)
    
    pg.display.flip()
    
    clock.tick(settings.FPS)
    
pg.quit
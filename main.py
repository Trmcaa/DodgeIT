import pygame as pg
from sys import exit
import player
import render
import obstacles
import settings

pg.init()

window = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
pg.display.set_caption("DodgeIT")
clock = pg.time.Clock()
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            exit()
            
    window.fill("pink")
    
    pg.display.flip()
    
    FPS = 60
    clock.tick(FPS)
    
pg.quit
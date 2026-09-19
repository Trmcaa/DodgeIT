import pygame as pg
import settings

class Player():
    def __init__(self):
        self.rect = pg.Rect(settings.STARTING_POS_W, settings.STARTING_POS_H, settings.PLAYER_W, settings.PLAYER_H)
        self.color = "black"
        
    def handle_input(self, keys):
        if keys[pg.K_a]:
            self.rect.x -= settings.PLAYER_SPEED
        if keys[pg.K_d]:
            self.rect.x += settings.PLAYER_SPEED
            
PLAYER = Player()
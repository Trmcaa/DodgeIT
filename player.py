import pygame as pg
import settings

class Player():
    def __init__(self):
        self.rect = pg.Rect(settings.STARTING_POS_W, settings.STARTING_POS_H, settings.PLAYER_W, settings.PLAYER_H)
        
    def handle_input(self, keys):
        self.keys = keys
        self.keys = pg.key.get_pressed()
        if self.keys == pg.K_a:
            self.rect.x -= settings.PLAYER_SPEED
        if self.keys == pg.K_d:
            self.rect.x += settings.PLAYER_SPEED
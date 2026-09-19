import pygame as pg
import settings

class Player():
    def __init__(self):
        self.rect = pg.Rect(settings.STARTING_POS_W, settings.STARTING_POS_H, settings.PLAYER_W, settings.PLAYER_H)
        
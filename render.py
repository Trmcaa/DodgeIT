import pygame as pg
import main
import settings
import player

class Render():
    def __init__(self):
        self.background = main.window.fill(settings.BACKGROUND)
        
    def draw_player(self, window, player):
        
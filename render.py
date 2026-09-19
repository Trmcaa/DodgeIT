import pygame as pg
import settings
import player

def draw_player(window, player):
    pg.draw.rect(window, player.color, player.rect)
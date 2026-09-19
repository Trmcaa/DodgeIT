import pygame as pg

def draw_player(window, player):
    pg.draw.rect(window, player.color, player.rect)
    
def draw_obstacles(window, list):
    for obstacle in list:
        pg.draw.rect(window, obstacle.color, obstacle.rect)
import pygame as pg

def draw_player(window, player):
    window.blit(player.image, player.rect)
    
def draw_obstacles(window, list):
    for obstacle in list:
        window.blit(obstacle.image, obstacle.rect)
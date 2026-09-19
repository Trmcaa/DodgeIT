import pygame as pg

def draw_player(window, player):
    window.blit(player.image, player.rect)
    
def draw_obstacles(window, list):
    for obstacle in list:
        window.blit(obstacle.flight_effect.image, obstacle.flight_effect.rect)
        window.blit(obstacle.image, obstacle.rect)

def draw_effects(window, list):
    for effect in list:
        window.blit(effect.image, effect.rect)
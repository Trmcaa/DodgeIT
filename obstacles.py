import pygame as pg
from random import randint
import settings

class Obstacle():
    def __init__(self):
        width = randint(settings.OBS_W_MIN, settings.OBS_W_MAX)
        height = randint(settings.OBS_H_MIN, settings.OBS_H_MAX)
        x = randint(0, settings.WIDTH - width)
        y = -height
        self.rect = pg.Rect(x, y, width, height)
        self.speed = randint(settings.OBS_SPEED_MIN, settings.OBS_SPEED_MAX)
        self.color = "blue"

    def update(self):
        self.rect.y += self.speed

def spawn_obstacle(list):
    list.append(Obstacle())

def update_obstacles(list):
    still_visible = []
    
    for obstacle in list:
        obstacle.update()
        if obstacle.rect.top < settings.HEIGHT:
            still_visible.append(obstacle)
            
    list[:] = still_visible
"""Meteor creation, animation, movement, and cleanup."""

import pygame as pg
from random import randint
import settings
import effects


_base_meteor_frames = None
_scaled_meteor_frames = {}


def get_meteor_frames(meteor_size):
    """Load and scale meteor frames once for each requested size."""
    global _base_meteor_frames
    if _base_meteor_frames is None:
        _base_meteor_frames = [
            pg.image.load(path).convert_alpha()
            for path in settings.METEOR_FRAMES
        ]

    if meteor_size not in _scaled_meteor_frames:
        _scaled_meteor_frames[meteor_size] = tuple(
            pg.transform.scale(frame, meteor_size)
            for frame in _base_meteor_frames
        )
    return _scaled_meteor_frames[meteor_size]


class Obstacle():
    """One animated meteor with a random size and falling speed."""

    def __init__(self, difficulty):
        difficulty_settings = settings.DIFFICULTIES[difficulty]
        scale = randint(
            int(difficulty_settings["scale_min"] * 100),
            int(difficulty_settings["scale_max"] * 100),
        ) / 100
        meteor_size = (
            round(settings.METEOR_WIDTH * scale),
            round(settings.METEOR_HEIGHT * scale),
        )
        self.frames = get_meteor_frames(meteor_size)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        x = randint(0, settings.WIDTH - meteor_size[0])
        y = -meteor_size[1]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.flight_effect = effects.create_flight_effect(
            self.rect.center,
            (self.rect.width * 2, self.rect.height * 2),
        )
        base_speed = randint(
            difficulty_settings["speed_min"],
            difficulty_settings["speed_max"],
        )
        speed_bonus = (difficulty_settings["scale_max"] - scale) * 0.8
        self.speed = max(1, round(base_speed + speed_bonus))
        self.last_update_time = pg.time.get_ticks()

    def update(self):
        """Move and advance the meteor animation."""
        self.rect.y += self.speed
        self.flight_effect.update(self.rect.center)
        current_time = pg.time.get_ticks()
        if current_time - self.last_update_time > settings.METEOR_ANIMATION_SPEED:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.last_update_time = current_time

def spawn_obstacle(list, difficulty):
    """Add one meteor to the active meteor list."""
    list.append(Obstacle(difficulty))


def update_obstacles(list):
    """Update meteors and return those that reached the ground."""
    still_visible = []
    landed = []
    
    for obstacle in list:
        obstacle.update()
        if obstacle.rect.top < settings.HEIGHT:
            still_visible.append(obstacle)
        else:
            landed.append(obstacle)
            
    list[:] = still_visible
    return landed
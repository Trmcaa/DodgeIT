import pygame as pg
from random import choice, randint, uniform


class Effect:
    def __init__(self, path, columns, rows, position, size, frame_time, loop=False):
        sheet = pg.image.load(path).convert_alpha()
        frame_width = sheet.get_width() // columns
        frame_height = sheet.get_height() // rows
        self.frames = []
        for row in range(rows):
            for column in range(columns):
                frame = sheet.subsurface((
                    column * frame_width,
                    row * frame_height,
                    frame_width,
                    frame_height,
                ))
                self.frames.append(pg.transform.smoothscale(frame, size))

        self.position = position
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=position)
        self.frame_time = frame_time
        self.current_frame = 0
        self.last_update_time = pg.time.get_ticks()
        self.loop = loop
        self.finished = False

    def update(self, position=None):
        if position is not None:
            self.position = position
        self.rect = self.image.get_rect(center=self.position)

        current_time = pg.time.get_ticks()
        if current_time - self.last_update_time < self.frame_time:
            return

        self.current_frame += 1
        self.last_update_time = current_time
        if self.current_frame >= len(self.frames):
            if not self.loop:
                self.finished = True
                return
            self.current_frame = 0

        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, window):
        window.blit(self.image, self.rect)


class GroundDebris:
    def __init__(self, position):
        paths = [
            "assets/vfx/dirt_01_a.png",
            "assets/vfx/dirt_02_a.png",
            "assets/vfx/dirt_03_a.png",
        ]
        self.particles = []
        for _ in range(14):
            image = pg.image.load(choice(paths)).convert_alpha()
            size = randint(12, 28)
            image = pg.transform.smoothscale(image, (size, size))
            self.particles.append({
                "image": image,
                "position": [position[0] + uniform(-12, 12), position[1] - randint(2, 10)],
                "velocity": [uniform(-4.5, 4.5), uniform(-8.5, -3.5)],
                "age": 0,
                "lifetime": randint(280, 440),
            })
        self.finished = False

    def update(self):
        elapsed = 16
        active_particles = 0
        for particle in self.particles:
            particle["age"] += elapsed
            if particle["age"] >= particle["lifetime"]:
                continue

            active_particles += 1
            particle["velocity"][1] += 0.35
            particle["position"][0] += particle["velocity"][0]
            particle["position"][1] += particle["velocity"][1]
            alpha = round(255 * (1 - particle["age"] / particle["lifetime"]))
            particle["image"].set_alpha(alpha)

        self.finished = active_particles == 0

    def draw(self, window):
        for particle in self.particles:
            if particle["age"] < particle["lifetime"]:
                image = particle["image"]
                rect = image.get_rect(center=particle["position"])
                window.blit(image, rect)


def create_flight_effect(position, size):
    return Effect(
        "assets/vfx/fire_point_6x5.png",
        6,
        5,
        position,
        size,
        50,
        loop=True,
    )


def create_hit_effect(position):
    return Effect(
        "assets/vfx/explosion_6x5.png",
        6,
        5,
        position,
        (180, 180),
        45,
    )


def create_ground_effect(position):
    return GroundDebris(position)

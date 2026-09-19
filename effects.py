import pygame as pg


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
    return Effect(
        "assets/vfx/fire_ring_6x5.png",
        6,
        5,
        position,
        (150, 125),
        45,
    )

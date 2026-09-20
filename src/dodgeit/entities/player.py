"""Player animation, movement, upgrades, and hit handling."""

import pygame as pg

from ..config import settings


class Player(pg.sprite.Sprite):
    """The player character and its persistent upgrade state."""

    def __init__(self):
        super().__init__()

        self.animations = {
            "idle": self.load_frames(settings.PLAYER_IDLE),
            "left": self.load_frames(settings.PLAYER_LEFT),
            "right": self.load_frames(settings.PLAYER_RIGHT),
        }
        self.current_animation = "idle"
        self.frames = self.animations[self.current_animation]
        
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect: pg.Rect = self.image.get_rect()
        self.rect.x = settings.STARTING_POS_W
        self.rect.y = settings.STARTING_POS_H
        self.speed = settings.PLAYER_SPEED
        self.speed_upgraded = False
        self.max_hits = 1
        self.hits_remaining = self.max_hits
        
        self.last_update_time = pg.time.get_ticks()

    @staticmethod
    def load_frames(path):
        """Split one horizontal spritesheet into animation frames."""
        sprite_sheet = pg.image.load(path)
        frames = []
        for i in range(settings.FRAME_COUNT):
            frame = sprite_sheet.subsurface((
                i * settings.FRAME_WIDTH,
                0,
                settings.FRAME_WIDTH,
                settings.FRAME_HEIGHT,
            ))
            frames.append(frame)
        return frames

    def set_animation(self, animation):
        if self.current_animation != animation:
            self.current_animation = animation
            self.frames = self.animations[animation]
            self.current_frame = 0
            self.image = self.frames[self.current_frame]

    def handle_input(self, keys):
        """Move horizontally and keep the player inside the display."""
        if keys[pg.K_a]:
            self.rect.x -= self.speed
            self.set_animation("left")
        if keys[pg.K_d]:
            self.rect.x += self.speed
            self.set_animation("right")
        self.rect.x = max(0, min(self.rect.x, settings.WIDTH - self.rect.width))
        if not keys[pg.K_a] and not keys[pg.K_d]:
            self.set_animation("idle")

    def upgrade_speed(self):
        """Apply the one-time movement speed upgrade."""
        if not self.speed_upgraded:
            self.speed += settings.SPEED_UPGRADE
            self.speed_upgraded = True

    def upgrade_survivability(self):
        """Unlock one additional meteor hit per round."""
        if self.max_hits < 2:
            self.max_hits = 2
            self.hits_remaining = self.max_hits

    def reset_hits(self):
        """Restore the hit counter when a new round starts."""
        self.hits_remaining = self.max_hits

    def animate(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_update_time >settings.ANIMATION_SPEED:
            self.current_frame = (self.current_frame + 1) % settings.FRAME_COUNT
            self.image = self.frames[self.current_frame]
            self.last_update_time = current_time
            
PLAYER = Player()
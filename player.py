import pygame as pg
import settings

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.sprite_sheet = pg.image.load("assets/idle.png")
        print(self.sprite_sheet.get_size())
        
        self.frames = []
        for i in range(settings.FRAME_COUNT):
            frame = self.sprite_sheet.subsurface((i * settings.FRAME_WIDTH, 0, settings.FRAME_WIDTH, settings.FRAME_HEIGHT))
            self.frames.append(frame)
        
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = settings.STARTING_POS_W
        self.rect.y = settings.STARTING_POS_H
        
        self.last_update_time = pg.time.get_ticks()
        
    def handle_input(self, keys):
        if keys[pg.K_a]:
            self.rect.x -= settings.PLAYER_SPEED
        if keys[pg.K_d]:
            self.rect.x += settings.PLAYER_SPEED
            
    def animate(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_update_time >settings.ANIMATION_SPEED:
            self.current_frame = (self.current_frame + 1) % settings.FRAME_COUNT
            self.image = self.frames[self.current_frame]
            self.last_update_time = current_time
            
PLAYER = Player()
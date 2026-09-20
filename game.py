"""Main game session and state transitions."""

import pygame as pg

import effects
import obstacles
import player
import render
import settings
import upgrades


class Game:
    """Own the game loop, runtime state, input, updates, and drawing."""

    def __init__(self):
        self.window = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pg.display.set_caption("DodgeIT")
        self.clock = pg.time.Clock()
        self.background = pg.transform.scale(
            pg.image.load(settings.BACKGROUND),
            (settings.WIDTH, settings.HEIGHT),
        )
        self.player = player.PLAYER
        self.obstacles = []
        self.active_effects = []
        self.running = True
        self.last_spawn_time = pg.time.get_ticks()
        self.game_over = False
        self.chaos_mode = False
        self.game_over_time = 0
        self.score_start_time = pg.time.get_ticks()
        self.score = 0
        self.score_adjustment = 0
        self.upgrade_menu = False

    def run(self):
        """Run frames until the window is closed."""
        while self.running:
            current_time = pg.time.get_ticks()
            self.handle_events(current_time)
            self.update(current_time)
            self.draw(current_time)
            self.clock.tick(settings.FPS)

    def handle_events(self, current_time):
        """Handle window events and keyboard actions."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                return

            if event.type != pg.KEYDOWN:
                continue

            if event.key == pg.K_u and not self.game_over:
                self.upgrade_menu = not self.upgrade_menu
                continue

            if event.key == pg.K_RETURN and self.can_respawn(current_time):
                self.respawn()
                continue

            if not self.game_over and self.upgrade_menu:
                new_score = upgrades.handle_purchase(
                    event,
                    self.player,
                    self.score,
                )
                self.score_adjustment += new_score - self.score
                self.score = new_score

    def can_respawn(self, current_time):
        return self.game_over and current_time - self.game_over_time >= settings.RESPAWN_DELAY

    def respawn(self):
        """Reset the round while keeping purchased upgrades."""
        self.obstacles.clear()
        self.active_effects.clear()
        self.player.rect.topleft = (settings.STARTING_POS_W, settings.STARTING_POS_H)
        self.player.set_animation("idle")
        self.player.last_update_time = pg.time.get_ticks()
        self.player.reset_hits()
        self.game_over = False
        self.chaos_mode = False
        self.upgrade_menu = False
        self.score_start_time = pg.time.get_ticks()
        self.score = 0
        self.score_adjustment = 0
        self.last_spawn_time = self.score_start_time

    def update(self, current_time):
        """Advance player, meteor, effect, score, and game-over state."""
        keys = pg.key.get_pressed()
        if not self.game_over:
            self.player.handle_input(keys)
            self.score = (current_time - self.score_start_time) // 1000 + self.score_adjustment
        self.player.animate()

        # After the delay, the old meteor field becomes an uncontrolled challenge.
        if (
            self.game_over
            and not self.chaos_mode
            and current_time - self.game_over_time >= settings.GAME_OVER_DELAY
        ):
            self.chaos_mode = True
            self.last_spawn_time = current_time

        self.spawn_meteors(current_time)
        self.update_meteors(current_time)
        self.update_effects()

    def spawn_meteors(self, current_time):
        spawn_interval = (
            settings.CHAOS_SPAWN_INTERVAL
            if self.chaos_mode
            else settings.NEW_OBS_MIN
        )
        if (not self.game_over or self.chaos_mode) and current_time - self.last_spawn_time > spawn_interval:
            obstacles.spawn_obstacle(self.obstacles, self.chaos_mode)
            self.last_spawn_time = current_time

    def update_meteors(self, current_time):
        landed = obstacles.update_obstacles(self.obstacles)
        for meteor in landed:
            self.active_effects.append(
                effects.create_ground_effect((meteor.rect.centerx, settings.HEIGHT))
            )

        for meteor in self.obstacles[:]:
            if not self.game_over and meteor.rect.colliderect(self.player.rect):
                self.active_effects.append(effects.create_hit_effect(meteor.rect.center))
                self.obstacles.remove(meteor)
                self.player.hits_remaining -= 1
                if self.player.hits_remaining <= 0:
                    self.game_over = True
                    self.game_over_time = current_time
                    self.score = (current_time - self.score_start_time) // 1000 + self.score_adjustment

    def update_effects(self):
        for effect in self.active_effects:
            effect.update()
        self.active_effects[:] = [
            effect for effect in self.active_effects if not effect.finished
        ]

    def draw(self, current_time):
        """Draw the current frame and any state overlays."""
        self.window.blit(self.background, (0, 0))
        render.draw_player(self.window, self.player)
        render.draw_obstacles(self.window, self.obstacles)
        render.draw_effects(self.window, self.active_effects)
        render.draw_score(self.window, self.score)
        render.draw_upgrade_menu(
            self.window,
            self.upgrade_menu,
            self.score,
            self.player,
        )

        if self.game_over:
            respawn_ready = current_time - self.game_over_time >= settings.RESPAWN_DELAY
            render.draw_game_over(self.window, self.chaos_mode, respawn_ready)

        pg.display.flip()

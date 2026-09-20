"""Main game session and state transitions."""

import pygame as pg

from .config import settings
from .entities import obstacles, player
from .systems import effects, stats, upgrades
from .ui import render


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
        self.game_over_time = 0
        self.score_start_time = pg.time.get_ticks()
        self.score = 0
        self.lifetime_stats = stats.load()
        self.best_score = self.lifetime_stats["best_score"]
        self.score_adjustment = 0
        self.upgrade_menu = False
        self.paused = False
        self.difficulty = None
        self.show_menu = True
        self.hits_taken = 0
        self.run_recorded = False
        self.purchased_upgrades = {"speed": 0, "survivability": 0}

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

            if event.key == pg.K_m and (self.game_over or self.paused):
                self.return_to_menu()
                continue

            if self.show_menu:
                difficulty_keys = {
                    pg.K_1: "easy",
                    pg.K_2: "medium",
                    pg.K_3: "hard",
                }
                if event.key in difficulty_keys:
                    self.start_run(difficulty_keys[event.key])
                continue

            if event.key == pg.K_u and not self.game_over:
                self.upgrade_menu = not self.upgrade_menu
                continue

            if event.key == pg.K_p and not self.game_over:
                self.paused = not self.paused
                continue

            if event.key == pg.K_RETURN and self.can_respawn(current_time):
                self.respawn()
                continue

            if not self.game_over and self.upgrade_menu:
                old_score = self.score
                new_score = upgrades.handle_purchase(
                    event,
                    self.player,
                    self.score,
                )
                self.score_adjustment += new_score - old_score
                self.score = new_score
                if new_score != old_score:
                    if event.key in (pg.K_LSHIFT, pg.K_RSHIFT):
                        self.purchased_upgrades["speed"] = 1
                    elif event.key in (pg.K_LCTRL, pg.K_RCTRL):
                        self.purchased_upgrades["survivability"] = 1

    def start_run(self, difficulty):
        """Start a fresh run using the selected difficulty profile."""
        self.difficulty = difficulty
        self.show_menu = False
        self.game_over = False
        self.score_start_time = pg.time.get_ticks()
        self.last_spawn_time = self.score_start_time

    def return_to_menu(self):
        """Leave a paused or finished run without losing lifetime progress."""
        self.obstacles.clear()
        self.active_effects.clear()
        self.player.rect.topleft = (settings.STARTING_POS_W, settings.STARTING_POS_H)
        self.player.set_animation("idle")
        self.player.reset_hits()
        self.difficulty = None
        self.show_menu = True
        self.game_over = False
        self.paused = False
        self.upgrade_menu = False
        self.score = 0
        self.score_adjustment = 0

    def calculate_score(self, current_time):
        """Calculate survival score using the selected difficulty multiplier."""
        elapsed_seconds = (current_time - self.score_start_time) // 1000
        score_rate = settings.DIFFICULTIES[self.difficulty]["score_rate"]
        return int(elapsed_seconds * score_rate) + self.score_adjustment

    def record_current_run(self):
        """Persist the run once, when the player is defeated."""
        if self.run_recorded:
            return
        stats.record_run(
            self.lifetime_stats,
            self.difficulty,
            self.score,
            self.hits_taken,
            self.purchased_upgrades,
        )
        self.best_score = self.lifetime_stats["best_score"]
        self.run_recorded = True

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
        self.upgrade_menu = False
        self.score_start_time = pg.time.get_ticks()
        self.score = 0
        self.score_adjustment = 0
        self.last_spawn_time = self.score_start_time
        self.paused = False
        self.hits_taken = 0
        self.run_recorded = False

    def update(self, current_time):
        """Advance player, meteor, effect, score, and game-over state."""
        if self.show_menu or self.paused:
            return

        keys = pg.key.get_pressed()
        if not self.game_over:
            self.player.handle_input(keys)
            self.score = self.calculate_score(current_time)
            self.best_score = max(self.best_score, self.score)
        self.player.animate()

        self.spawn_meteors(current_time)
        self.update_meteors(current_time)
        self.update_effects()

    def spawn_meteors(self, current_time):
        spawn_interval = settings.DIFFICULTIES[self.difficulty]["spawn_interval"]
        if not self.game_over and current_time - self.last_spawn_time > spawn_interval:
            obstacles.spawn_obstacle(self.obstacles, self.difficulty)
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
                self.hits_taken += 1
                if self.player.hits_remaining <= 0:
                    self.game_over = True
                    self.game_over_time = current_time
                    self.score = self.calculate_score(current_time)
                    self.record_current_run()

    def update_effects(self):
        for effect in self.active_effects:
            effect.update()
        self.active_effects[:] = [
            effect for effect in self.active_effects if not effect.finished
        ]

    def draw(self, current_time):
        """Draw the current frame and any state overlays."""
        self.window.blit(self.background, (0, 0))
        if self.show_menu:
            render.draw_main_menu(self.window, self.lifetime_stats)
            pg.display.flip()
            return

        render.draw_player(self.window, self.player)
        render.draw_obstacles(self.window, self.obstacles)
        render.draw_effects(self.window, self.active_effects)
        render.draw_hud(
            self.window,
            self.score,
            self.best_score,
            self.player,
            self.difficulty,
        )
        render.draw_upgrade_menu(
            self.window,
            self.upgrade_menu,
            self.score,
            self.player,
        )

        if self.game_over:
            respawn_ready = current_time - self.game_over_time >= settings.RESPAWN_DELAY
            render.draw_game_over(self.window, respawn_ready)
        elif self.paused:
            render.draw_paused(self.window)

        pg.display.flip()

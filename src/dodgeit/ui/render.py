"""All drawing functions used by the game session."""

import pygame as pg

from ..config import settings

_score_font = pg.font.Font(None, 42)
_hint_font = pg.font.Font(None, 32)
_title_font = pg.font.Font(None, 32)
_option_font = pg.font.Font(None, 27)
_game_over_title_font = pg.font.Font(None, 96)
_game_over_subtitle_font = pg.font.Font(None, 42)


def draw_player(window, player):
    """Draw the current player animation frame."""
    window.blit(player.image, player.rect)


def draw_obstacles(window, list):
    """Draw meteor trails behind their meteor sprites."""
    for obstacle in list:
        window.blit(obstacle.flight_effect.image, obstacle.flight_effect.rect)
        window.blit(obstacle.image, obstacle.rect)


def draw_effects(window, list):
    """Draw one-shot and particle effects above the game world."""
    for effect in list:
        effect.draw(window)


def draw_hud(window, score, best_score, player, difficulty):
    """Draw score, best score, remaining hits, and the current difficulty."""
    score_text = _score_font.render(f"SCORE: {score}", True, (255, 240, 190))
    best_text = _option_font.render(f"BEST: {best_score}", True, (205, 220, 235))
    hits_text = _option_font.render(
        f"HITS: {player.hits_remaining}/{player.max_hits}",
        True,
        (255, 190, 150),
    )
    mode_text = _option_font.render(
        f"{settings.DIFFICULTIES[difficulty]['label']} MODE  x{settings.DIFFICULTIES[difficulty]['score_rate']}",
        True,
        (255, 210, 140),
    )
    window.blit(score_text, (20, 18))
    window.blit(best_text, (20, 53))
    window.blit(hits_text, (20, 82))
    window.blit(mode_text, (20, 111))


def draw_score(window, score):
    """Draw only the score label for simple callers."""
    score_text = _score_font.render(f"SCORE: {score}", True, (255, 240, 190))
    window.blit(score_text, (20, 18))


def draw_upgrade_menu(window, is_open, score, player):
    hint = _hint_font.render('PRESS "U" FOR UPGRADES', True, (255, 240, 190))
    hint_rect = hint.get_rect(topright=(window.get_width() - 20, 18))
    window.blit(hint, hint_rect)

    if not is_open:
        return

    panel = pg.Surface((390, 150), pg.SRCALPHA)
    panel.fill((10, 12, 30, 225))
    panel_rect = panel.get_rect(topright=(window.get_width() - 20, 58))
    window.blit(panel, panel_rect)

    window.blit(_title_font.render("UPGRADES - 100 SCORE", True, (255, 220, 120)), (panel_rect.x + 16, panel_rect.y + 12))
    speed_state = "OWNED" if player.speed_upgraded else "BUY"
    hits_state = "OWNED" if player.max_hits >= 2 else "BUY"
    window.blit(_option_font.render(f"SHIFT  Speed +{settings.SPEED_UPGRADE}: {speed_state}", True, (230, 240, 255)), (panel_rect.x + 16, panel_rect.y + 52))
    window.blit(_option_font.render(f"CTRL   Survive 2 hits: {hits_state}", True, (230, 240, 255)), (panel_rect.x + 16, panel_rect.y + 82))
    window.blit(_option_font.render(f"Available score: {score}", True, (180, 210, 180)), (panel_rect.x + 16, panel_rect.y + 112))

def draw_game_over(window, respawn_ready):
    overlay = pg.Surface(window.get_size(), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 145))
    window.blit(overlay, (0, 0))

    title = _game_over_title_font.render("GAME OVER", True, (255, 80, 70))
    if respawn_ready:
        subtitle_text = "PRESS ENTER TO RESPAWN  |  M FOR MENU"
    else:
        subtitle_text = "PRESS ENTER AFTER THE COUNTDOWN  |  M FOR MENU"
    subtitle = _game_over_subtitle_font.render(subtitle_text, True, (255, 220, 150))
    window.blit(title, title.get_rect(center=(window.get_width() // 2, window.get_height() // 2 - 35)))
    window.blit(subtitle, subtitle.get_rect(center=(window.get_width() // 2, window.get_height() // 2 + 45)))


def draw_paused(window):
    """Show a pause overlay while keeping the current scene visible."""
    overlay = pg.Surface(window.get_size(), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 125))
    window.blit(overlay, (0, 0))
    title = _game_over_title_font.render("PAUSED", True, (255, 240, 190))
    subtitle = _game_over_subtitle_font.render("PRESS P TO CONTINUE  |  M FOR MENU", True, (230, 240, 255))
    window.blit(title, title.get_rect(center=(window.get_width() // 2, window.get_height() // 2 - 35)))
    window.blit(subtitle, subtitle.get_rect(center=(window.get_width() // 2, window.get_height() // 2 + 45)))


def draw_main_menu(window, lifetime_stats):
    """Draw difficulty selection and lifetime statistics."""
    overlay = pg.Surface(window.get_size(), pg.SRCALPHA)
    overlay.fill((3, 5, 20, 185))
    window.blit(overlay, (0, 0))

    title = _game_over_title_font.render("DODGE IT", True, (255, 235, 170))
    subtitle = _game_over_subtitle_font.render("SELECT YOUR DIFFICULTY", True, (230, 240, 255))
    window.blit(title, title.get_rect(center=(window.get_width() // 2, 115)))
    window.blit(subtitle, subtitle.get_rect(center=(window.get_width() // 2, 180)))

    options = [("1", "EASY  x0.75"), ("2", "MEDIUM  x1.0"), ("3", "HARD  x1.5")]
    for index, (key, label) in enumerate(options):
        y = 260 + index * 58
        option = _title_font.render(f"{key}   {label}", True, (255, 220, 130))
        window.blit(option, option.get_rect(center=(window.get_width() // 2, y)))

    stats_x = window.get_width() // 2 + 210
    stats_y = 250
    stats_title = _title_font.render("LIFETIME STATS", True, (255, 220, 130))
    window.blit(stats_title, (stats_x, stats_y))
    lifetime_lines = [
        f"Runs: {lifetime_stats['total_runs']}",
        f"Best score: {lifetime_stats['best_score']}",
        f"Total score: {lifetime_stats['total_score']}",
        f"Hits taken: {lifetime_stats['total_hits_taken']}",
    ]
    for index, line in enumerate(lifetime_lines):
        window.blit(_option_font.render(line, True, (220, 230, 240)), (stats_x, stats_y + 38 + index * 28))

    footer = _option_font.render("A / D move   |   U upgrades   |   P pause   |   M menu", True, (190, 210, 220))
    window.blit(footer, footer.get_rect(center=(window.get_width() // 2, 600)))
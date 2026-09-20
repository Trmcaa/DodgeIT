"""All drawing functions used by the game session."""

import pygame as pg
import settings


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


def draw_score(window, score):
    font = pg.font.Font(None, 42)
    score_text = font.render(f"SCORE: {score}", True, (255, 240, 190))
    window.blit(score_text, (20, 18))


def draw_upgrade_menu(window, is_open, score, player):
    hint_font = pg.font.Font(None, 32)
    hint = hint_font.render('PRESS "U" FOR UPGRADES', True, (255, 240, 190))
    hint_rect = hint.get_rect(topright=(window.get_width() - 20, 18))
    window.blit(hint, hint_rect)

    if not is_open:
        return

    panel = pg.Surface((390, 150), pg.SRCALPHA)
    panel.fill((10, 12, 30, 225))
    panel_rect = panel.get_rect(topright=(window.get_width() - 20, 58))
    window.blit(panel, panel_rect)

    title_font = pg.font.Font(None, 32)
    option_font = pg.font.Font(None, 27)
    window.blit(title_font.render("UPGRADES - 100 SCORE", True, (255, 220, 120)), (panel_rect.x + 16, panel_rect.y + 12))
    speed_state = "OWNED" if player.speed_upgraded else "BUY"
    hits_state = "OWNED" if player.max_hits >= 2 else "BUY"
    window.blit(option_font.render(f"SHIFT  Speed +{settings.SPEED_UPGRADE}: {speed_state}", True, (230, 240, 255)), (panel_rect.x + 16, panel_rect.y + 52))
    window.blit(option_font.render(f"CTRL   Survive 2 hits: {hits_state}", True, (230, 240, 255)), (panel_rect.x + 16, panel_rect.y + 82))
    window.blit(option_font.render(f"Available score: {score}", True, (180, 210, 180)), (panel_rect.x + 16, panel_rect.y + 112))

def draw_game_over(window, chaos_mode, respawn_ready):
    overlay = pg.Surface(window.get_size(), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 145))
    window.blit(overlay, (0, 0))

    title_font = pg.font.Font(None, 96)
    subtitle_font = pg.font.Font(None, 42)
    title = title_font.render("GAME OVER", True, (255, 80, 70))
    if respawn_ready:
        subtitle_text = "PRESS ENTER TO RESPAWN"
    elif chaos_mode:
        subtitle_text = "CHAOS MODE - METEORS ARE OUT OF CONTROL"
    else:
        subtitle_text = "CHAOS MODE STARTS IN 3 SECONDS"
    subtitle = subtitle_font.render(subtitle_text, True, (255, 220, 150))
    window.blit(title, title.get_rect(center=(window.get_width() // 2, window.get_height() // 2 - 35)))
    window.blit(subtitle, subtitle.get_rect(center=(window.get_width() // 2, window.get_height() // 2 + 45)))
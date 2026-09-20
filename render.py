import pygame as pg

def draw_player(window, player):
    window.blit(player.image, player.rect)
    
def draw_obstacles(window, list):
    for obstacle in list:
        window.blit(obstacle.flight_effect.image, obstacle.flight_effect.rect)
        window.blit(obstacle.image, obstacle.rect)

def draw_effects(window, list):
    for effect in list:
        effect.draw(window)

def draw_game_over(window, chaos_mode):
    overlay = pg.Surface(window.get_size(), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 145))
    window.blit(overlay, (0, 0))

    title_font = pg.font.Font(None, 96)
    subtitle_font = pg.font.Font(None, 42)
    title = title_font.render("GAME OVER", True, (255, 80, 70))
    subtitle_text = "CHAOS MODE" if chaos_mode else "METEORY SE VRACI ZA 3 SEKUNDY"
    subtitle = subtitle_font.render(subtitle_text, True, (255, 220, 150))
    window.blit(title, title.get_rect(center=(window.get_width() // 2, window.get_height() // 2 - 35)))
    window.blit(subtitle, subtitle.get_rect(center=(window.get_width() // 2, window.get_height() // 2 + 45)))
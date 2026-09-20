"""Upgrade purchase rules."""

import pygame as pg

import settings


def purchase_speed(player, score):
    """Buy the speed upgrade once and return the updated score."""
    if score < settings.UPGRADE_COST or player.speed_upgraded:
        return score

    player.upgrade_speed()
    return score - settings.UPGRADE_COST


def purchase_survivability(player, score):
    """Buy the extra-hit upgrade once and return the updated score."""
    if score < settings.UPGRADE_COST or player.max_hits >= 2:
        return score

    player.upgrade_survivability()
    return score - settings.UPGRADE_COST


def handle_purchase(event, player, score):
    """Apply the upgrade matching a key press, if the purchase is valid."""
    if event.key in (pg.K_LSHIFT, pg.K_RSHIFT):
        return purchase_speed(player, score)
    if event.key in (pg.K_LCTRL, pg.K_RCTRL):
        return purchase_survivability(player, score)
    return score

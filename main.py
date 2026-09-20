"""Application entry point."""

import pygame as pg


def main():
    pg.init()
    from src.dodgeit.game import Game

    Game().run()
    pg.quit()


if __name__ == "__main__":
    main()

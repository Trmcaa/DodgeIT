<div align="center">

# DODGE IT

### Survive the fall. Learn the pattern. Then survive the chaos.

<img src="assets/background.png" alt="DodgeIT neon night landscape" width="720" />

<br />

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.x-00A86B?style=for-the-badge&logo=python&logoColor=white)](https://www.pygame.org/)
[![Status](https://img.shields.io/badge/Status-Playable-EA4C89?style=for-the-badge)](#gameplay)

</div>

---

## The Game

**Dodge It** is a fast arcade survival game built with Python and Pygame. Move through a neon night, read the falling patterns, and stay alive as long as possible while animated meteors become faster, more frequent, and increasingly unforgiving.

Every second matters. Every upgrade is a choice. Every impact changes the run.

## Gameplay

- Dodge animated meteors falling from above.
- Meteors spawn with different sizes and speeds.
- Smaller meteors are faster and harder to read.
- Flying meteors carry a looping fire trail.
- Missed meteors burst into flying debris when they hit the ground.
- A direct hit triggers an impact explosion.
- After death, the arena escalates into **Chaos Mode**.
- Survive longer to earn more score and buy permanent upgrades.

## Controls

| Action | Key |
| --- | --- |
| Move left | `A` |
| Move right | `D` |
| Open or close upgrades | `U` |
| Buy speed upgrade | `SHIFT` |
| Buy survivability upgrade | `CTRL` |
| Respawn after the countdown | `ENTER` |

The upgrade panel appears in the top-right corner. Each upgrade costs **100 score** and can be purchased once per run profile.

## Upgrade System

| Upgrade | Effect |
| --- | --- |
| `SHIFT` - Speed Boost | Increases horizontal movement speed. |
| `CTRL` - Reinforced Suit | Lets the player survive one additional meteor hit. |

Purchased upgrades remain active after respawning, while the score and current round reset.

## Game Flow

```text
Normal Run
    |
    |  meteor collision
    v
Game Over
    |
    |  3 seconds
    v
Chaos Mode
    |
    |  5 seconds total + ENTER
    v
Respawn and try again
```

Chaos Mode is intentionally uncontrolled: meteors fall faster and spawn at a much higher rate. It is a pressure phase, not a pause screen.

## Project Structure

```text
DodgeIT/
├── main.py        # Application entry point
├── game.py        # Game session, loop, state transitions, and orchestration
├── player.py      # Player movement, animation, upgrades, and hit state
├── obstacles.py   # Meteor loading, scaling, animation, movement, and cleanup
├── effects.py     # Flight, impact, explosion, and ground-debris effects
├── render.py      # All drawing and HUD functions
├── settings.py    # Display, asset, gameplay, and timing configuration
├── upgrades.py    # Upgrade purchase rules and keyboard mapping
└── assets/
    ├── meteor/    # Meteor animation frames
    ├── player/    # Idle, left, and right player spritesheets
    └── vfx/       # Explosion, fire, and debris effects
```

The project keeps responsibilities deliberately small: `game.py` coordinates the systems, while the individual modules own their own behavior.

## Getting Started

### Requirements

- Python 3.10 or newer
- Pygame 2.x

### Install

```bash
python -m pip install pygame
```

### Run

From the project directory:

```bash
python main.py
```

On Windows, this also works if the Python launcher is configured:

```powershell
py main.py
```

## Performance Notes

Dodge It caches decoded and scaled meteor frames, visual-effects spritesheets, debris textures, and HUD fonts. This keeps expensive image processing out of the frame loop and helps the game stay responsive as Chaos Mode fills the screen.

## Credits

- Game code and integration: **Dodge It project**
- Visual-effects sprites: **Brackeys VFX Bundle**
- Player and meteor sprites: project assets
- Background artwork: project asset

When redistributing the project, preserve the original asset licenses and credits bundled with the source assets.

## License

The code in this repository is available for personal and educational use. Asset licensing may differ from the code, so check the original license for any third-party visual assets before redistribution.

---

<div align="center">

**Stay sharp. Keep moving. Do not look up.**

</div>

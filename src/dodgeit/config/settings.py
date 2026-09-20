#Exe fix
import sys
import os

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Display
WIDTH = 1280
HEIGHT = 720
# Assets
BACKGROUND = resource_path("assets/background.png")
PLAYER_IDLE = resource_path("assets/player/idle.png")
PLAYER_RIGHT = resource_path("assets/player/right.png")
PLAYER_LEFT = resource_path("assets/player/left.png")
METEOR_FRAMES = [
	resource_path("assets/meteor/FB001.png"),
	resource_path("assets/meteor/FB002.png"),
	resource_path("assets/meteor/FB003.png"),
	resource_path("assets/meteor/FB004.png"),
	resource_path("assets/meteor/FB005.png"),
]

# Player
FRAME_WIDTH = 64
FRAME_HEIGHT = 128
FRAME_COUNT = 8
ANIMATION_SPEED = 150
PLAYER_W = 64
PLAYER_H = 128
STARTING_POS_W = WIDTH/2
STARTING_POS_H = HEIGHT - PLAYER_H
PLAYER_SPEED = 5
UPGRADE_COST = 100
SPEED_UPGRADE = 3

# Meteors
METEOR_WIDTH = 32
METEOR_HEIGHT = 64
METEOR_SCALE_MIN = 0.6
METEOR_SCALE_MAX = 1.6
METEOR_ANIMATION_SPEED = 100
RESPAWN_DELAY = 5000
DIFFICULTIES = {
	"easy": {
		"label": "EASY",
		"score_rate": 0.75,
		"spawn_interval": 850,
		"speed_min": 3,
		"speed_max": 6,
		"scale_min": 0.8,
		"scale_max": 1.3,
	},
	"medium": {
		"label": "MEDIUM",
		"score_rate": 1.0,
		"spawn_interval": 600,
		"speed_min": 4,
		"speed_max": 8,
		"scale_min": 0.7,
		"scale_max": 1.5,
	},
	"hard": {
		"label": "HARD",
		"score_rate": 1.5,
		"spawn_interval": 380,
		"speed_min": 6,
		"speed_max": 11,
		"scale_min": 0.6,
		"scale_max": 1.6,
	},
}

# Timing
FPS = 60
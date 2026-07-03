import os

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Game title
GAME_TITLE = "FLAPPY BIRD"

# Physics Settings
GRAVITY = 0.25
FLAP_STRENGTH = -6.0
MAX_FALL_SPEED = 10.0
BIRD_ROTATION_FACTOR = 3.0  # Scales rotation based on y-velocity

# Bird Settings
BIRD_START_X = 80
BIRD_START_Y = SCREEN_HEIGHT // 2
BIRD_SIZE = (38, 26)  # Width, Height

# Pipe Settings
PIPE_WIDTH = 80
PIPE_MIN_HEIGHT = 50
PIPE_MAX_HEIGHT = SCREEN_HEIGHT - 200  # Leave room for floor and gap
BASE_PIPE_SPEED = 3.0
PIPE_SPEED_INCREMENT = 0.5  # Add this speed per 10 points
PIPE_SPAWN_INTERVAL = 2000  # Milliseconds (2 seconds)
BASE_PIPE_GAP = 140
MIN_PIPE_GAP = 110
PIPE_GAP_DECREMENT = 5  # Reduce gap size per 10 points

# Floor Settings
FLOOR_HEIGHT = 50
FLOOR_Y = SCREEN_HEIGHT - FLOOR_HEIGHT

# Colors (modern palette)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_SKY = (112, 197, 206)
COLOR_GREEN = (115, 191, 46)
COLOR_ORANGE = (252, 120, 88)
COLOR_YELLOW = (250, 222, 63)
COLOR_UI_TEXT = (255, 255, 255)
COLOR_SHADOW = (40, 40, 40)
COLOR_OVERLAY = (0, 0, 0, 150)  # RGBA for semi-transparent overlay

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
HIGHSCORE_FILE = os.path.join(BASE_DIR, "highscore.txt")

# Image Paths
BIRD_IMAGE_PATH = os.path.join(ASSETS_DIR, "bird.png")
BACKGROUND_IMAGE_PATH = os.path.join(ASSETS_DIR, "background.png")
PIPE_IMAGE_PATH = os.path.join(ASSETS_DIR, "pipe.png")

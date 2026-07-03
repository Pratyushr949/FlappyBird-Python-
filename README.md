# Flappy Bird Clone in Pygame

A polished, high-performance, and object-oriented implementation of the classic Flappy Bird game built in Python using the `pygame` library. It features retro-style programmatically generated graphics, smooth physics, difficulty scaling, game state transitions, and persistent local high-scoring.

## Game Description
Flappy Bird is a side-scrolling arcade game where the player controls a bird, attempting to fly between columns of green pipes without hitting them. The game requires precise timing as gravity constantly pulls the bird downward.

## Features
* **Physics-Based Flight:** Smooth acceleration due to gravity and instant upward impulses upon flapping.
* **Auto-Generating Assets:** No missing image resources; a built-in generator programmatically creates the game sprites (bird, background gradient, city hills silhouette, and green pipes) on initial launch.
* **Pixel-Perfect Collisions:** Utilizes Pygame's mask collision system rather than simple bounding boxes for a fair, frustratingly fun gameplay experience.
* **Difficulty Scaling:** The game speed increases slightly and the pipe gap decreases for every 10 points scored, maintaining a balanced challenge.
* **Persistent High Scores:** Saves the best local score to `highscore.txt` so players can challenge their personal record.
* **Modern Aesthetic:** Features scrolling backgrounds, parallax scrolling floor stripes, dynamic bird rotation based on velocity, and shadowed typography overlays.
* **Full State Controller:** Implements distinct states for Start Screen, Playing, Paused, and Game Over.

## Folder Structure
```text
flappy-bird-pygame/
├── main.py              # Main entry point (resolves assets, spawns game)
├── settings.py          # Central configurations, constants, physics parameters, and color palettes
├── game.py              # Contains classes for Bird, PipePair, Game, and State handling
├── generate_assets.py   # Draws and exports retro-style png sprite files
├── assets/              # Generated sprite folder (created automatically on run)
│   ├── bird.png
│   ├── background.png
│   └── pipe.png
├── highscore.txt        # Local text file storing high score
├── requirements.txt     # Python package requirements
└── README.md            # Game documentation
```

## Installation Instructions

1. Ensure you have Python 3.8 or higher installed on your system.
2. Clone the repository and navigate to the project directory:
   ```bash
   cd flappy-bird-pygame
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

Launch the game using python:
```bash
python main.py
```

## Controls List

* **SPACE:** Flap upward (when playing) / Start the game (from Start Screen)
* **P:** Pause / Resume the game
* **R:** Restart the game (from Game Over Screen)
* **ESC:** Exit/Quit the game (from Game Over Screen)
* **Close Window:** Exit/Quit the game (at any time)

## Future Improvements
* **Audio Integration:** Add sound effects for flapping, scoring, and colliding, along with a toggle mute option.
* **Skin Shop:** Let users purchase custom bird skins (e.g., retro, robotic, firebird) using coins collected during gameplay.
* **Varying Pipe Types:** Introduce moving pipes (vertically) and wind currents to make higher difficulty levels even more dynamic.
* **Particle System:** Add feather particles when flapping or crashing.

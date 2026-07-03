import os
import sys
from settings import BIRD_IMAGE_PATH, BACKGROUND_IMAGE_PATH, PIPE_IMAGE_PATH

def ensure_assets():
    # Check if all assets exist
    assets_exist = (
        os.path.exists(BIRD_IMAGE_PATH) and
        os.path.exists(BACKGROUND_IMAGE_PATH) and
        os.path.exists(PIPE_IMAGE_PATH)
    )
    
    if not assets_exist:
        print("Required assets not found. Generating assets programmatically...")
        try:
            from generate_assets import create_assets
            create_assets()
        except ImportError:
            print("Error: Could not import asset generator! Pillow library may not be installed.")
            print("Please run: pip install Pillow pygame")
            sys.exit(1)
        except Exception as e:
            print(f"Error generating assets: {e}")
            sys.exit(1)

def main():
    # Ensure assets are generated first
    ensure_assets()
    
    # Import and run the game
    try:
        from game import Game
        game = Game()
        game.main_loop()
    except Exception as e:
        print(f"An error occurred while running the game: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

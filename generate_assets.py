import os
import math
from PIL import Image, ImageDraw

def create_assets():
    # Define directories
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    print("Generating assets...")

    # 1. Generate background.png (400 x 600)
    bg_width, bg_height = 400, 600
    bg = Image.new("RGBA", (bg_width, bg_height))
    draw = ImageDraw.Draw(bg)

    # Draw sky gradient (from soft blue to light turquoise)
    for y in range(bg_height):
        # Calculate interpolation factor
        ratio = y / bg_height
        r = int(112 + (197 - 112) * ratio)
        g = int(197 + (228 - 197) * ratio)
        b = int(206 + (240 - 206) * ratio)
        draw.line([(0, y), (bg_width, y)], fill=(r, g, b, 255))

    # Draw some fluffy clouds (white with soft outlines)
    def draw_cloud(cx, cy, scale):
        cloud_color = (255, 255, 255, 200)
        draw.ellipse([cx - 20 * scale, cy - 10 * scale, cx + 20 * scale, cy + 10 * scale], fill=cloud_color)
        draw.ellipse([cx - 10 * scale, cy - 20 * scale, cx + 10 * scale, cy + 5 * scale], fill=cloud_color)
        draw.ellipse([cx + 5 * scale, cy - 15 * scale, cx + 25 * scale, cy + 5 * scale], fill=cloud_color)

    draw_cloud(80, 120, 1.2)
    draw_cloud(280, 180, 1.5)
    draw_cloud(180, 80, 0.8)
    draw_cloud(340, 90, 1.0)

    # Draw city/hills silhouette at the bottom (above floor y=550)
    floor_y = 550
    # Far hills (darker turquoise-blue)
    hill_color = (130, 209, 196, 255)
    points = [
        (0, floor_y),
        (0, floor_y - 40),
        (80, floor_y - 60),
        (160, floor_y - 30),
        (240, floor_y - 70),
        (320, floor_y - 50),
        (400, floor_y - 40),
        (400, floor_y)
    ]
    draw.polygon(points, fill=hill_color)

    # Near bushes/hills (greener)
    bush_color = (117, 196, 88, 255)
    points_near = [
        (0, floor_y),
        (0, floor_y - 20),
        (60, floor_y - 35),
        (120, floor_y - 15),
        (200, floor_y - 40),
        (280, floor_y - 20),
        (350, floor_y - 30),
        (400, floor_y - 25),
        (400, floor_y)
    ]
    draw.polygon(points_near, fill=bush_color)

    bg.save(os.path.join(assets_dir, "background.png"))
    print("Saved background.png")

    # 2. Generate bird.png (38 x 26) - Cute Yellow Pixel Bird
    bird_w, bird_h = 38, 26
    bird = Image.new("RGBA", (bird_w, bird_h), (0, 0, 0, 0))
    draw_bird = ImageDraw.Draw(bird)

    # Colors
    yellow = (250, 222, 63, 255)
    dark_yellow = (220, 185, 30, 255)
    orange = (252, 120, 88, 255)
    white = (255, 255, 255, 255)
    black = (0, 0, 0, 255)

    # Body (yellow ellipse)
    draw_bird.ellipse([2, 2, bird_w - 6, bird_h - 2], fill=yellow, outline=black, width=2)
    # Underbelly shading
    draw_bird.chord([4, 12, bird_w - 8, bird_h - 4], start=0, end=180, fill=dark_yellow)

    # Wing (white/yellowish shape)
    draw_bird.ellipse([6, 8, 18, 18], fill=white, outline=black, width=2)

    # Eye (white circle)
    draw_bird.ellipse([22, 5, 30, 13], fill=white, outline=black, width=2)
    # Pupil (black circle)
    draw_bird.ellipse([26, 7, 29, 11], fill=black)

    # Beak (orange polygon pointing right)
    beak_points = [
        (bird_w - 8, 10),
        (bird_w - 1, 14),
        (bird_w - 8, 18)
    ]
    draw_bird.polygon(beak_points, fill=orange, outline=black)
    draw_bird.line([(bird_w - 8, 14), (bird_w - 3, 14)], fill=black, width=1)

    bird.save(os.path.join(assets_dir, "bird.png"))
    print("Saved bird.png")

    # 3. Generate pipe.png (80 x 600) - Retro cylindrical green pipe
    # We will generate a texture for the pipe. Pygame can load this and use it.
    # The image will contain a shaded green pipe.
    pipe_w, pipe_h = 80, 600
    pipe = Image.new("RGBA", (pipe_w, pipe_h), (0, 0, 0, 0))
    draw_pipe = ImageDraw.Draw(pipe)

    # Green shades for cylindrical look
    g_main = (115, 191, 46, 255)
    g_dark = (85, 141, 34, 255)
    g_light = (165, 230, 80, 255)
    g_darkest = (55, 95, 22, 255)

    # Draw vertical cylinder bands to give a 3D effect
    # The pipe consists of body and lip. But since this is a generic pipe image,
    # let's make it a shaded pipe body from x=6 to x=74, and the borders at x=6 and x=74.
    # Then we will draw the pipe lip programmatically in pygame using the same style,
    # or we can draw the whole pipe including lip!
    # Wait, if we generate a 80x600 texture, how does Pygame render it?
    # Pygame can draw the pipe by taking a slice of the pipe image.
    # If the pipe image has a lip at the end, say the bottom 30 pixels or top 30 pixels,
    # it gets tricky because a bottom pipe has a lip at the top, and a top pipe has a lip at the bottom.
    # A cleaner way: The `pipe.png` represents the pipe *body*. We tile or stretch it.
    # What about the lip? The lip is also just a wider piece of pipe (e.g. 84 wide, 30 tall).
    # We can draw the lip programmatically using Pygame rects shaded beautifully, OR
    # We can make `pipe.png` just a beautifully shaded tileable pipe texture of 80x600,
    # and in Pygame, we draw the pipe body by blitting the texture, and draw the lip by blitting
    # a slightly wider version.
    # Let's make `pipe.png` a complete shaded pipe texture:
    # 0 to 8: border
    # 8 to 20: highlight
    # 20 to 50: middle green
    # 50 to 72: shadow green
    # 72 to 80: border
    
    # Let's draw the vertical bands for the pipe body
    for x in range(pipe_w):
        if x < 4 or x >= pipe_w - 4:
            c = g_darkest
        elif x < 12:
            # Transition highlight to light
            c = g_dark
        elif x < 24:
            c = g_light
        elif x < 50:
            c = g_main
        else:
            c = g_dark
        
        draw_pipe.line([(x, 0), (x, pipe_h)], fill=c)

    # Draw some thin black lines to simulate details/joints or retro texture
    # A few horizontal lines across the pipe
    for y in range(100, pipe_h, 150):
        draw_pipe.line([(4, y), (pipe_w - 5, y)], fill=g_darkest, width=2)
        draw_pipe.line([(4, y + 2), (pipe_w - 5, y + 2)], fill=g_light, width=1)

    pipe.save(os.path.join(assets_dir, "pipe.png"))
    print("Saved pipe.png")

if __name__ == "__main__":
    create_assets()

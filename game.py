import os
import random
import pygame
from settings import *

class State:
    START = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3

class Bird:
    def __init__(self, image):
        self.original_image = image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = BIRD_START_X
        self.rect.y = BIRD_START_Y
        self.y_float = float(self.rect.y)
        self.velocity = 0.0
        self.mask = pygame.mask.from_surface(self.image)
        
    def flap(self):
        self.velocity = FLAP_STRENGTH
        
    def update(self):
        # Apply gravity
        self.velocity += GRAVITY
        if self.velocity > MAX_FALL_SPEED:
            self.velocity = MAX_FALL_SPEED
            
        self.y_float += self.velocity
        self.rect.y = int(self.y_float)
        
        # Rotate image based on velocity
        angle = -self.velocity * BIRD_ROTATION_FACTOR
        angle = max(-90.0, min(25.0, angle))  # Clamp rotation
        self.image = pygame.transform.rotate(self.original_image, angle)
        
        # Keep centered during rotation
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        
        # Recreate mask for rotated image
        self.mask = pygame.mask.from_surface(self.image)
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class PipePair:
    def __init__(self, x, speed, gap_size, pipe_image):
        self.x = float(x)
        self.speed = speed
        self.gap_size = gap_size
        self.scored = False
        
        # Random heights for top and bottom pipes
        self.top_height = random.randint(PIPE_MIN_HEIGHT, PIPE_MAX_HEIGHT)
        self.bottom_y = self.top_height + self.gap_size
        self.bottom_height = SCREEN_HEIGHT - self.bottom_y - FLOOR_HEIGHT
        
        # Draw and bake top pipe onto its own surface
        self.top_surf = pygame.Surface((PIPE_WIDTH, self.top_height), pygame.SRCALPHA)
        body_w = 72
        body_x = (PIPE_WIDTH - body_w) // 2
        
        # Draw top pipe body (scaled segment)
        body_h_top = self.top_height - 24
        if body_h_top > 0:
            scaled_body = pygame.transform.scale(pipe_image, (body_w, body_h_top))
            self.top_surf.blit(scaled_body, (body_x, 0))
            
        # Draw top pipe lip (at the bottom of top pipe)
        lip_surf = pygame.Surface((PIPE_WIDTH, 24), pygame.SRCALPHA)
        scaled_lip = pygame.transform.scale(pipe_image, (PIPE_WIDTH, 24))
        lip_surf.blit(scaled_lip, (0, 0))
        pygame.draw.rect(lip_surf, COLOR_BLACK, (0, 0, PIPE_WIDTH, 24), 2)
        pygame.draw.line(lip_surf, (165, 230, 80), (3, 2), (3, 21), 1)
        pygame.draw.line(lip_surf, (55, 95, 22), (PIPE_WIDTH - 4, 2), (PIPE_WIDTH - 4, 21), 1)
        self.top_surf.blit(lip_surf, (0, self.top_height - 24))
        
        # Draw and bake bottom pipe onto its own surface
        self.bottom_surf = pygame.Surface((PIPE_WIDTH, self.bottom_height), pygame.SRCALPHA)
        
        # Draw bottom pipe body (scaled segment)
        body_h_bottom = self.bottom_height - 24
        if body_h_bottom > 0:
            scaled_body = pygame.transform.scale(pipe_image, (body_w, body_h_bottom))
            self.bottom_surf.blit(scaled_body, (body_x, 24))
            
        # Draw bottom pipe lip (at the top of bottom pipe)
        self.bottom_surf.blit(lip_surf, (0, 0))
        
        # Build collision masks
        self.top_mask = pygame.mask.from_surface(self.top_surf)
        self.bottom_mask = pygame.mask.from_surface(self.bottom_surf)
        
        # Bounding boxes for position references
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.top_height)
        self.bottom_rect = pygame.Rect(self.x, self.bottom_y, PIPE_WIDTH, self.bottom_height)
        
    def update(self):
        self.x -= self.speed
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)
        
    def draw(self, screen):
        screen.blit(self.top_surf, (int(self.x), 0))
        screen.blit(self.bottom_surf, (int(self.x), self.bottom_y))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        
        # State & data initialization
        self.state = State.START
        self.score = 0
        self.highscore = 0
        self.pipe_speed = BASE_PIPE_SPEED
        self.pipe_gap = BASE_PIPE_GAP
        self.pipes = []
        self.bg_scroll_x = 0.0
        self.floor_scroll_x = 0.0
        self.last_pipe_spawn_time = 0
        
        self.initialize_game()

    def initialize_game(self):
        # Load high score
        self.load_highscore()
        
        # Load fonts
        try:
            self.title_font = pygame.font.SysFont("Impact", 48)
            self.ui_font = pygame.font.SysFont("Arial", 22, bold=True)
            self.score_font = pygame.font.SysFont("Arial", 36, bold=True)
        except Exception:
            self.title_font = pygame.font.Font(None, 48)
            self.ui_font = pygame.font.Font(None, 22)
            self.score_font = pygame.font.Font(None, 36)
            
        # Verify asset files and load them
        try:
            self.bg_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert_alpha()
            self.bird_image = pygame.image.load(BIRD_IMAGE_PATH).convert_alpha()
            self.pipe_image = pygame.image.load(PIPE_IMAGE_PATH).convert_alpha()
        except pygame.error as e:
            print(f"Error loading assets: {e}")
            print("Please make sure you have generated the assets using generate_assets.py")
            raise SystemExit(e)
            
        # Instantiate bird
        self.bird = Bird(self.bird_image)
        
    def load_highscore(self):
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, "r") as f:
                    self.highscore = int(f.read().strip())
            except Exception:
                self.highscore = 0
        else:
            self.highscore = 0
            self.save_highscore()

    def save_highscore(self):
        try:
            with open(HIGHSCORE_FILE, "w") as f:
                f.write(str(self.highscore))
        except Exception as e:
            print(f"Failed to save highscore: {e}")

    def reset_game(self):
        self.bird = Bird(self.bird_image)
        self.pipes = []
        self.score = 0
        self.pipe_speed = BASE_PIPE_SPEED
        self.pipe_gap = BASE_PIPE_GAP
        self.last_pipe_spawn_time = pygame.time.get_ticks()
        self.state = State.PLAYING

    def handle_input(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.save_highscore()
                return False
                
            if event.type == pygame.KEYDOWN:
                if self.state == State.START:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        
                elif self.state == State.PLAYING:
                    if event.key == pygame.K_SPACE:
                        self.bird.flap()
                    elif event.key == pygame.K_p:
                        self.state = State.PAUSED
                        
                elif self.state == State.PAUSED:
                    if event.key == pygame.K_p:
                        self.state = State.PLAYING
                        
                elif self.state == State.GAME_OVER:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.save_highscore()
                        return False
        return True

    def update_bird(self):
        self.bird.update()

    def spawn_pipe(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pipe_spawn_time >= PIPE_SPAWN_INTERVAL:
            # Spawn a pipe pair at the right edge
            self.pipes.append(PipePair(SCREEN_WIDTH, self.pipe_speed, self.pipe_gap, self.pipe_image))
            self.last_pipe_spawn_time = current_time

    def move_pipes(self):
        for pipe in self.pipes:
            pipe.update()
        # Remove offscreen pipes
        self.pipes = [p for p in self.pipes if p.x + PIPE_WIDTH > 0]

    def check_collisions(self):
        # Ceiling or ground collision
        if self.bird.rect.top <= 0 or self.bird.rect.bottom >= FLOOR_Y:
            return True
            
        # Pipe collision using pixel-perfect masks
        for pipe in self.pipes:
            offset_top = (pipe.top_rect.x - self.bird.rect.x, pipe.top_rect.y - self.bird.rect.y)
            offset_bottom = (pipe.bottom_rect.x - self.bird.rect.x, pipe.bottom_rect.y - self.bird.rect.y)
            
            collision_top = self.bird.mask.overlap(pipe.top_mask, offset_top)
            collision_bottom = self.bird.mask.overlap(pipe.bottom_mask, offset_bottom)
            
            if collision_top or collision_bottom:
                return True
                
        return False

    def update_score(self):
        for pipe in self.pipes:
            # Check if bird passed the pipe's center
            if pipe.x + PIPE_WIDTH < self.bird.rect.centerx and not pipe.scored:
                pipe.scored = True
                self.score += 1
                
                # Check for high score
                if self.score > self.highscore:
                    self.highscore = self.score
                    self.save_highscore()
                
                # Difficulty scaling: every 10 points increase speed and shrink gap
                if self.score > 0 and self.score % 10 == 0:
                    self.pipe_speed = BASE_PIPE_SPEED + (self.score // 10) * PIPE_SPEED_INCREMENT
                    new_gap = BASE_PIPE_GAP - (self.score // 10) * PIPE_GAP_DECREMENT
                    self.pipe_gap = max(MIN_PIPE_GAP, new_gap)
                    
                    # Align existing pipe speeds
                    for p in self.pipes:
                        p.speed = self.pipe_speed

    def draw_background(self):
        # Update scroll x coordinates (only when playing)
        if self.state == State.PLAYING:
            self.bg_scroll_x = (self.bg_scroll_x - self.pipe_speed * 0.2) % SCREEN_WIDTH
            self.floor_scroll_x = (self.floor_scroll_x - self.pipe_speed) % SCREEN_WIDTH
            
        # Draw sky gradient/background
        self.screen.blit(self.bg_image, (int(self.bg_scroll_x), 0))
        if self.bg_scroll_x > 0:
            self.screen.blit(self.bg_image, (int(self.bg_scroll_x) - SCREEN_WIDTH, 0))
        else:
            self.screen.blit(self.bg_image, (int(self.bg_scroll_x) + SCREEN_WIDTH, 0))
            
        # Draw floor
        pygame.draw.rect(self.screen, (222, 216, 149), (0, FLOOR_Y, SCREEN_WIDTH, FLOOR_HEIGHT))
        pygame.draw.rect(self.screen, (115, 191, 46), (0, FLOOR_Y, SCREEN_WIDTH, 12))
        pygame.draw.line(self.screen, (85, 141, 34), (0, FLOOR_Y + 12), (SCREEN_WIDTH, FLOOR_Y + 12), 2)
        pygame.draw.line(self.screen, COLOR_BLACK, (0, FLOOR_Y), (SCREEN_WIDTH, FLOOR_Y), 3)
        
        # Draw scrolling floor texture stripes
        stripe_w = 8
        spacing = 24
        start_x = int(self.floor_scroll_x) - spacing
        while start_x < SCREEN_WIDTH:
            pygame.draw.rect(self.screen, (200, 190, 120), (start_x, FLOOR_Y + 18, stripe_w, FLOOR_HEIGHT - 24))
            start_x += spacing

    def draw_bird(self):
        self.bird.draw(self.screen)

    def draw_pipes(self):
        for pipe in self.pipes:
            pipe.draw(self.screen)

    def draw_ui(self):
        # Text shadows
        def draw_shadowed_text(text, font, color, center_pos):
            text_surf = font.render(text, True, color)
            shadow_surf = font.render(text, True, COLOR_SHADOW)
            
            rect = text_surf.get_rect(center=center_pos)
            shadow_rect = shadow_surf.get_rect(center=(center_pos[0] + 2, center_pos[1] + 2))
            
            self.screen.blit(shadow_surf, shadow_rect)
            self.screen.blit(text_surf, rect)

        if self.state == State.START:
            # Title
            draw_shadowed_text(GAME_TITLE, self.title_font, COLOR_YELLOW, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            # Start prompts
            draw_shadowed_text("Press SPACE to Start", self.ui_font, COLOR_WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            # Highscore
            draw_shadowed_text(f"High Score: {self.highscore}", self.ui_font, COLOR_ORANGE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            
        elif self.state == State.PLAYING or self.state == State.PAUSED:
            # Running Score in top-center
            draw_shadowed_text(str(self.score), self.score_font, COLOR_WHITE, (SCREEN_WIDTH // 2, 40))
            
            if self.state == State.PAUSED:
                # Semi-transparent overlay
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill(COLOR_OVERLAY)
                self.screen.blit(overlay, (0, 0))
                # Pause text
                draw_shadowed_text("GAME PAUSED", self.title_font, COLOR_WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
                draw_shadowed_text("Press P to Resume", self.ui_font, COLOR_WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
                
        elif self.state == State.GAME_OVER:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill(COLOR_OVERLAY)
            self.screen.blit(overlay, (0, 0))
            
            draw_shadowed_text("GAME OVER", self.title_font, COLOR_ORANGE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            draw_shadowed_text(f"Score: {self.score}", self.score_font, COLOR_WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            draw_shadowed_text(f"Best Score: {self.highscore}", self.ui_font, COLOR_YELLOW, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
            draw_shadowed_text("Press R to Restart", self.ui_font, COLOR_WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90))
            draw_shadowed_text("Press ESC to Quit", self.ui_font, COLOR_WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130))

    def main_loop(self):
        running = True
        while running:
            # 1. Handle user inputs
            running = self.handle_input()
            if not running:
                break
                
            # 2. Logic updates based on state
            if self.state == State.PLAYING:
                self.update_bird()
                self.spawn_pipe()
                self.move_pipes()
                self.update_score()
                
                # Check for death collision
                if self.check_collisions():
                    self.state = State.GAME_OVER
                    self.save_highscore()
            
            # 3. Draw screen layers
            self.draw_background()
            self.draw_pipes()
            self.draw_bird()
            self.draw_ui()
            
            # 4. Update display and limit frames
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()

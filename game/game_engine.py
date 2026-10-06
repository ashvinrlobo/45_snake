import pygame
from .snake import Snake
from .food import Food
from .sound import SoundManager

# Game Engine

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (220, 60, 60)

GOLD = (255, 215, 0)
CYAN = (100, 220, 255)
GRAY = (180, 180, 180)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell_size = 20
        self.grid_width = width // self.cell_size
        self.grid_height = height // self.cell_size

        self.snake = Snake(self.grid_width // 2, self.grid_height // 2, self.cell_size)
        self.food = Food(self.grid_width, self.grid_height, self.cell_size)
        self.sound_manager = SoundManager()

        self.score = 0
        self.high_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.font_large = pygame.font.SysFont("Arial", 50, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 20)

        self.moves_per_second = 8
        self._frame_counter = 0

        self.game_over = False
        self.should_quit = False

    def restart(self, moves_per_second=None):
        if moves_per_second is not None:
            self.moves_per_second = moves_per_second
        self.snake = Snake(self.grid_width // 2, self.grid_height // 2, self.cell_size)
        self.food = Food(self.grid_width, self.grid_height, self.cell_size)
        self.score = 0
        self._frame_counter = 0
        self.game_over = False
        self.should_quit = False

    def handle_keydown(self, key):
        if self.game_over:
            # Replay options on Game Over
            if key in (pygame.K_1, pygame.K_KP1, pygame.K_e):
                self.restart(moves_per_second=6)  # Easy
            elif key in (pygame.K_2, pygame.K_KP2, pygame.K_m):
                self.restart(moves_per_second=10) # Medium
            elif key in (pygame.K_3, pygame.K_KP3, pygame.K_h):
                self.restart(moves_per_second=16) # Hard
            elif key in (pygame.K_SPACE, pygame.K_r):
                self.restart()                    # Restart with current difficulty
            elif key in (pygame.K_ESCAPE, pygame.K_q):
                self.should_quit = True
            return

        # Direction changes are applied immediately on key press.
        if key in (pygame.K_UP, pygame.K_w):
            self.snake.set_direction(0, -1)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.snake.set_direction(0, 1)
        elif key in (pygame.K_LEFT, pygame.K_a):
            self.snake.set_direction(-1, 0)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.snake.set_direction(1, 0)

    def handle_input(self):
        # Reserved for continuously-held-key input (not used for a
        # grid-based snake, but kept here to mirror the engine's shape).
        pass

    def update(self):
        if self.game_over:
            return

        self._frame_counter += 1
        frames_per_move = max(1, 60 // self.moves_per_second)
        if self._frame_counter < frames_per_move:
            return
        self._frame_counter = 0

        self.snake.move()

        if self.snake.collides_with_wall(self.grid_width, self.grid_height) or self.snake.collides_with_self():
            if not self.game_over:
                self.game_over = True
                self.sound_manager.play_game_over()
                if self.score > self.high_score:
                    self.high_score = self.score
            return

        if self.snake.head_rect().colliderect(self.food.rect()):
            self.snake.grow()
            self.score += 1
            self.sound_manager.play_eat()
            if self.score > self.high_score:
                self.high_score = self.score
            self.food.respawn(self.snake.body)

    def render(self, screen):
        # Draw food
        pygame.draw.rect(screen, RED, self.food.rect())

        # Draw snake
        for rect in self.snake.segment_rects():
            pygame.draw.rect(screen, GREEN, rect)

        # Draw current score and session high score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        high_score_text = self.font.render(f"High Score: {self.high_score}", True, GOLD)
        screen.blit(high_score_text, (self.width - high_score_text.get_width() - 10, 10))

        if self.game_over:
            # Semi-transparent dark overlay over the game screen
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 215))
            screen.blit(overlay, (0, 0))

            # Game Over Title
            title_text = self.font_large.render("GAME OVER", True, RED)
            title_rect = title_text.get_rect(center=(self.width // 2, self.height // 2 - 130))
            screen.blit(title_text, title_rect)

            # Final Score Display
            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            score_rect = final_score_text.get_rect(center=(self.width // 2, self.height // 2 - 70))
            screen.blit(final_score_text, score_rect)

            # Session High Score Display
            high_text = self.font.render(f"Session High Score: {self.high_score}", True, GOLD)
            high_rect = high_text.get_rect(center=(self.width // 2, self.height // 2 - 25))
            screen.blit(high_text, high_rect)

            # Replay options prompt 1: SPACE to restart
            restart_text = self.font_small.render("[ SPACE ] : Play Again (Current Speed)", True, CYAN)
            restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 35))
            screen.blit(restart_text, restart_rect)

            # Replay options prompt 2: Select difficulty
            diff_text = self.font_small.render("[ 1 ] Easy   |   [ 2 ] Medium   |   [ 3 ] Hard", True, WHITE)
            diff_rect = diff_text.get_rect(center=(self.width // 2, self.height // 2 + 70))
            screen.blit(diff_text, diff_rect)

            # Exit prompt
            quit_text = self.font_small.render("[ ESC / Q ] : Quit Game", True, GRAY)
            quit_rect = quit_text.get_rect(center=(self.width // 2, self.height // 2 + 115))
            screen.blit(quit_text, quit_rect)

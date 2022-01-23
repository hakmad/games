"""Main program."""

import pygame
import random


from gui import *
from settings import *
from sprites import *


class States:
    """Class to represent a state.

    Methods are meant to be overridden.

    Attributes:
    share (dict) - a dictionary that is shared across all instances of 
    the States class.
    running (bool) - flag to check if the state is running.
    next (str) - name of the next state to transition to.
    """
    share = {}
    def __init__(self):
        """Initialise the new state."""
        self.running = True
        self.next = None

    def setup(self):
        """Setup the state."""
        pass
    
    def cleanup(self):
        """Cleanup after the state."""
        pass

    def handle_events(self, event):
        """Handle input and events for the state.

        Arguments:
        event (pygame.event.Event) - input/event to handle.
        """
        pass

    def update(self):
        """Update the state."""
        pass

    def draw(self, screen):
        """Draw state to the screen.

        Arguments:
        screen (pygame.Surface) - screen to draw to.
        """
        pass


class MainMenu(States):
    """Main menu state."""
    def __init__(self):
        """Initialise the new main menu state."""
        States.__init__(self)

    def setup(self):
        """Setup the main menu state."""
        self.running = True

        self.title = Text("Pong", screen_width // 2, 40, font_size=32)

        self.start_game = Button("Start Game", self.switch_to_game, screen_width // 2 - 75, 100, 150, 20)
        self.exit_game = Button("Exit Game", self.exit, screen_width // 2 - 75, 150, 150, 20)

    def switch_to_game(self):
        """Switch the current state to the game state."""
        self.next = "game"
        self.running = False

    def exit(self):
        """Exit the game."""
        self.next = None
        self.running = False
    
    def handle_events(self, event):
        """Handle input and events for the main menu state.

        Arguments:
        event (pygame.event.Event) - input/event to handle.
        """
        self.start_game.check_clicked(event)
        self.exit_game.check_clicked(event)

    def update(self):
        """Update the main menu state."""
        self.start_game.check_hover()
        self.exit_game.check_hover()

    def draw(self, screen):
        """Draw the main menu state to the screen.

        Arguments:
        screen (pygame.Surface) - screen to draw to.
        """
        screen.fill(black)

        self.title.draw(screen)

        self.start_game.draw(screen)
        self.exit_game.draw(screen)

        pygame.display.flip()


class GameOver(States):
    """Game over state."""
    def __init__(self):
        """Initialise the new game over state."""
        States.__init__(self)

    def setup(self):
        """Setup the game over state."""
        self.running = True

        # Check who won.
        if States.share["paddle_1_score"] > States.share["paddle_2_score"]:
            self.winner_text = "Player 1 Won!"
            self.winner_colour = "red"
        else:
            self.winner_text = "Player 2 Won!"
            self.winner_colour = "blue"

        self.title = Text("Game Over!", screen_width // 2, 40, font_size=32)
        self.winner = Text(self.winner_text, screen_width // 2, screen_height // 2, font_colour=self.winner_colour)

        self.main_menu = Button("Main Menu", self.switch_to_main_menu, screen_width // 2 - 75, screen_height - 100, 150, 20)
        self.restart = Button("Restart Game", self.switch_to_game, screen_width // 2 - 75, screen_height - 50, 150, 20)

    def switch_to_main_menu(self):
        """Switch the current state to the main menu state."""
        self.next = "main menu"
        self.running = False

    def switch_to_game(self):
        """Switch the current state to the game state."""
        self.next = "game"
        self.running = False

    def cleanup(self):
        """Cleanup after the game over state."""
        del self.title, self.winner

    def handle_events(self, event):
        """Handle input and events for the game over state.

        Arguments:
        event (pygame.event.Event) - input/event to handle.
        """
        self.main_menu.check_clicked(event)
        self.restart.check_clicked(event)
    
    def update(self):
        """Update the game over state."""
        self.main_menu.check_hover()
        self.restart.check_hover()

    def draw(self, screen):
        """Draw the game over state to the screen.

        Arguments:
        screen (pygame.Surface) - screen to draw to.
        """
        screen.fill(black)

        self.title.draw(screen)
        self.winner.draw(screen)

        self.main_menu.draw(screen)
        self.restart.draw(screen)

        pygame.display.flip()


class Game(States):
    def __init__(self):
        States.__init__(self)

    def setup(self):
        self.running = True
        self.next = "game over"

        self.paddle_1 = Paddle(30, pygame.K_w, pygame.K_s, red)
        self.paddle_2 = Paddle(screen_width - 40, pygame.K_UP, pygame.K_DOWN, blue)
        
        self.paddle_1_score = Text(str(self.paddle_1.score), (screen_width // 2) - 20, screen_height // 2, font_colour=red)
        self.paddle_2_score = Text(str(self.paddle_1.score), (screen_width // 2) + 20, screen_height // 2, font_colour=blue)

        self.paddles = [self.paddle_1, self.paddle_2]

        self.ball = Ball()
        self.ball.dx = random.choice((-5, -6, -7, 5, 6, 7))
        self.ball.dy = random.choice((-5, -6, -7, 5, 6, 7))
        
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.paddle_1)
        self.sprites.add(self.paddle_2)
        self.sprites.add(self.ball)

        self.paddle_hit = False
        self.paddle_hit_count = 0

    def cleanup(self):
        del self.paddle_1, self.paddle_2, self.ball
        del self.sprites, self.paddles
        del self.paddle_1_score, self.paddle_2_score

    def reset_sprites(self):
        self.paddle_hit_count = 0
        self.ball.reset()
        for paddle in self.paddles:
            paddle.reset()

    def update(self):
        self.sprites.update()
    
        for paddle in self.paddles:
            if self.ball.rect.colliderect(paddle.rect):
                self.paddle_hit = True
                if abs(paddle.rect.left - self.ball.rect.right) < collision_tolerance and self.ball.dx > 0:
                    self.ball.dx *= -1
                if abs(paddle.rect.right - self.ball.rect.left) < collision_tolerance and self.ball.dx < 0:
                    self.ball.dx *= -1
                if abs(paddle.rect.top - self.ball.rect.bottom) < collision_tolerance and self.ball.dy > 0:
                    self.ball.dy *= -1
                if abs(paddle.rect.bottom - self.ball.rect.top) < collision_tolerance and self.ball.dy < 0:
                    self.ball.dy *= -1
    
            if not(self.ball.rect.colliderect(paddle.rect)) and self.paddle_hit:
                if (self.paddle_hit_count % 3) == 0:
                    if self.ball.dx > 0:
                        self.ball.dx += random.randint(0, 3)
                    else:
                        self.ball.dx -= random.randint(0, 3)
    
                    if self.ball.dy > 0:
                        self.ball.dy += random.randint(0, 3)
                    else:
                        self.ball.dy -= random.randint(0, 3)
    
                self.paddle_hit = False
                self.paddle_hit_count += 1
    
        if self.ball.rect.x >= screen_width - self.ball.size:
            self.paddle_1.score += 1
            self.paddle_1_score.update_text(str(self.paddle_1.score))
            self.reset_sprites()
            self.ball.dx = random.choice((-5, -6, -7))
            self.ball.dy = random.choice((-5, -6, -7, 5, 6, 7))
    
        if self.ball.rect.x <= 0:
            self.paddle_2.score += 1
            self.paddle_2_score.update_text(str(self.paddle_2.score))
            self.reset_sprites()
            self.ball.dx = random.choice((5, 6, 7))
            self.ball.dy = random.choice((-5, -6, -7, 5, 6, 7))

        if self.paddle_1.score >= 11 or self.paddle_2.score >= 11:
            States.share["paddle_1_score"] = self.paddle_1.score
            States.share["paddle_2_score"] = self.paddle_2.score

            self.running = False

    def draw(self, screen):
        screen.fill(black)
    
        pygame.draw.line(screen, white, (screen_width // 2, 0), (screen_width // 2, screen_height), 5)
        
        self.paddle_1_score.draw(screen)
        self.paddle_2_score.draw(screen)
    
        self.sprites.draw(screen)
    
        pygame.display.flip()


class Control:
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state_dict = None
        self.current_state = None

    def setup(self, state_dict, start_state):
        self.state_dict = state_dict
        self.current_state = self.state_dict[start_state]
        self.current_state.setup()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.current_state.handle_events(event)

        if not(self.current_state.running):
            self.change_state()

    def change_state(self):
        try:
            new_state = self.current_state.next
            self.current_state.cleanup()
            self.current_state = self.state_dict[new_state]
            self.current_state.setup()
        except KeyError:
            self.running = False
    
    def main_loop(self):
        while self.running:
            self.clock.tick(fps)
            self.handle_events()
            self.current_state.update()
            self.current_state.draw(self.screen)
            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    
    state_dict = {
            "main menu": MainMenu(),
            "game": Game(),
            "game over": GameOver()
            }
    
    app = Control()
    app.setup(state_dict, "main menu")
    app.main_loop()
    
    pygame.quit()

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

        # Create title textbox.
        self.title = Text("Pong", screen_width // 2, 40, font_size=32)

        # Create navigation buttons.
        self.start_game = Button("Start Game", self.switch_to_game, screen_width // 2 - 75, 100, 150, 20)
        self.exit_game = Button("Exit Game", self.exit, screen_width // 2 - 75, 150, 150, 20)
   
    def handle_events(self, event):
        """Handle input and events for the main menu state.

        Arguments:
        event (pygame.event.Event) - input/event to handle.
        """
        # Check if buttons have been clicked.
        self.start_game.check_clicked(event)
        self.exit_game.check_clicked(event)

    def update(self):
        """Update the main menu state."""
        # Check if buttons have been hovered over.
        self.start_game.check_hover()
        self.exit_game.check_hover()

    def draw(self, screen):
        """Draw the main menu state to the screen.

        Arguments:
        screen (pygame.Surface) - screen to draw to.
        """
        # Fill the screen with black.
        screen.fill(black)

        # Draw the title textbox to the screen.
        self.title.draw(screen)

        # Draw the navigation buttons to the screen.
        self.start_game.draw(screen)
        self.exit_game.draw(screen)

        # Update the display.
        pygame.display.flip()

    def switch_to_game(self):
        """Switch the current state to the game state."""
        self.next = "game"
        self.running = False

    def exit(self):
        """Exit the game."""
        self.next = None
        self.running = False
 

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
            # Player 1 (red paddle) won.
            self.winner_text = "Player 1 Won!"
            self.winner_colour = "red"
        else:
            # Player 2 (blue paddle) won.
            self.winner_text = "Player 2 Won!"
            self.winner_colour = "blue"

        # Create title and winner textboxes.
        self.title = Text("Game Over!", screen_width // 2, 40, font_size=32)
        self.winner = Text(self.winner_text, screen_width // 2, screen_height // 2, font_colour=self.winner_colour)

        # Create navigation buttons.
        self.main_menu = Button("Main Menu", self.switch_to_main_menu, screen_width // 2 - 75, screen_height - 100, 150, 20)
        self.restart = Button("Restart Game", self.switch_to_game, screen_width // 2 - 75, screen_height - 50, 150, 20)

    def cleanup(self):
        """Cleanup after the game over state."""
        del self.title, self.winner

    def handle_events(self, event):
        """Handle input and events for the game over state.

        Arguments:
        event (pygame.event.Event) - input/event to handle.
        """
        # Check if buttons have been clicked.
        self.main_menu.check_clicked(event)
        self.restart.check_clicked(event)
    
    def update(self):
        """Update the game over state."""
        # Check if buttons have been hovered over.
        self.main_menu.check_hover()
        self.restart.check_hover()

    def draw(self, screen):
        """Draw the game over state to the screen.

        Arguments:
        screen (pygame.Surface) - screen to draw to.
        """
        # Fill the screen with black.
        screen.fill(black)

        # Draw the title and winner textboxes to the screen.
        self.title.draw(screen)
        self.winner.draw(screen)

        # Draw the navigation buttons to the screen.
        self.main_menu.draw(screen)
        self.restart.draw(screen)

        # Update the display.
        pygame.display.flip()

    def switch_to_main_menu(self):
        """Switch the current state to the main menu state."""
        self.next = "main menu"
        self.running = False

    def switch_to_game(self):
        """Switch the current state to the game state."""
        self.next = "game"
        self.running = False


class Game(States):
    """Game state."""
    def __init__(self):
        """Initialise the new game state."""
        States.__init__(self)

    def setup(self):
        """Setup the game state."""
        self.running = True
        self.next = "game over"

        # Create paddle sprites.
        self.paddle_1 = Paddle(30, pygame.K_w, pygame.K_s, red)
        self.paddle_2 = Paddle(screen_width - 40, pygame.K_UP, pygame.K_DOWN, blue)

        # Create paddle score textboxes.
        self.paddle_1_score = Text(str(self.paddle_1.score), (screen_width // 2) - 20, screen_height // 2, font_colour=red)
        self.paddle_2_score = Text(str(self.paddle_1.score), (screen_width // 2) + 20, screen_height // 2, font_colour=blue)

        # Create list to contain paddles.
        self.paddles = [self.paddle_1, self.paddle_2]

        # Create ball sprite.
        self.ball = Ball()
        self.ball.dx = random.choice((-5, -6, -7, 5, 6, 7))
        self.ball.dy = random.choice((-5, -6, -7, 5, 6, 7))

        # Create sprite group for all sprites.
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.paddle_1)
        self.sprites.add(self.paddle_2)
        self.sprites.add(self.ball)

        # Set flags and counters.
        self.paddle_hit = False
        self.paddle_hit_count = 0

    def cleanup(self):
        """Cleanup after the game state."""
        del self.paddle_1, self.paddle_2, self.ball
        del self.sprites, self.paddles
        del self.paddle_1_score, self.paddle_2_score

    def update(self):
        """Update the game state."""
        # Update all the sprites.
        self.sprites.update()

        # Move ball around the screen.
        for paddle in self.paddles:
            # Check if ball has collided with either of the paddles.
            if self.ball.rect.colliderect(paddle.rect):
                self.paddle_hit = True
                # Move the ball depending on the side of the paddle it collided with.
                if abs(paddle.rect.left - self.ball.rect.right) < collision_tolerance and self.ball.dx > 0:
                    self.ball.dx *= -1
                if abs(paddle.rect.right - self.ball.rect.left) < collision_tolerance and self.ball.dx < 0:
                    self.ball.dx *= -1
                if abs(paddle.rect.top - self.ball.rect.bottom) < collision_tolerance and self.ball.dy > 0:
                    self.ball.dy *= -1
                if abs(paddle.rect.bottom - self.ball.rect.top) < collision_tolerance and self.ball.dy < 0:
                    self.ball.dy *= -1

            # Move the ball in the opposite direction and randomly change its vectors.
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
   
        # Check if the ball has gone past the end of the screen on the right side.
        if self.ball.rect.x >= screen_width - self.ball.size:
            # Increase paddle 1s score.
            self.paddle_1.score += 1
            self.paddle_1_score.update_text(str(self.paddle_1.score))

            # Reset sprites.
            self.reset_sprites()
            
            # Change ball vectors.
            self.ball.dx = random.choice((-5, -6, -7))
            self.ball.dy = random.choice((-5, -6, -7, 5, 6, 7))
    
        # Check if the ball has gone past the end of the screen on the left side.
        if self.ball.rect.x <= 0:
            # Increase paddle 2s score.
            self.paddle_2.score += 1
            self.paddle_2_score.update_text(str(self.paddle_2.score))

            # Reset sprites.
            self.reset_sprites()

            # Change ball vectors.
            self.ball.dx = random.choice((5, 6, 7))
            self.ball.dy = random.choice((-5, -6, -7, 5, 6, 7))

        if self.paddle_1.score >= 11 or self.paddle_2.score >= 11:
            States.share["paddle_1_score"] = self.paddle_1.score
            States.share["paddle_2_score"] = self.paddle_2.score

            self.running = False

    def draw(self, screen):
        """Draw the game state to the screen.

        Arguments:
        screen (pygame.Surface) - screen to draw to.
        """
        # Fill the screen with black.
        screen.fill(black)
    
        # Draw a white line in the middle of the screen.
        pygame.draw.line(screen, white, (screen_width // 2, 0), (screen_width // 2, screen_height), 5)
        
        # Draw the paddle score textboxes to the screen.
        self.paddle_1_score.draw(screen)
        self.paddle_2_score.draw(screen)
    
        # Draw the sprites to the screen.
        self.sprites.draw(screen)
    
        # Update the display.
        pygame.display.flip()

    def reset_sprites(self):
        """Reset the paddle and ball sprites."""
        # Reset the paddles and balls.
        self.paddle_hit_count = 0
        self.ball.reset()
        for paddle in self.paddles:
            paddle.reset()


class Control:
    """Class used to control program and manage states.

    Attributes:
    screen (pygame.Surface) - screen to draw to.
    clock (pygame.time.Clock - clock to track time.
    running (bool) - flag to check if program is running.
    state_dict (dict) - dictionary containing states and their names.
    current_state (str) - name of current state.
    """
    def __init__(self):
        """Initialise the new control object."""
        # Create screen and clock.
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        # Set flags.
        self.running = True

        # Set state dictionary and current state.
        self.state_dict = None
        self.current_state = None

    def setup(self, state_dict, start_state):
        """Setup the control object."""
        # Add state dictionary and start state to control object.
        self.state_dict = state_dict
        self.current_state = self.state_dict[start_state]

        # Setup the current state.
        self.current_state.setup()

    def handle_events(self):
        """Handle events for the control object and the current state."""
        # Get events from PyGame.
        for event in pygame.event.get():
            # Check if program has been closed.
            if event.type == pygame.QUIT:
                self.running = False
            # Pass event to current state.
            self.current_state.handle_events(event)

        # Change the state when current state stops running.
        if not(self.current_state.running):
            self.change_state()

    def change_state(self):
        """Change the state to the next state."""
        try:
            # Get next state.
            new_state = self.current_state.next
            
            # Cleanup current state.
            self.current_state.cleanup()

            # Get and setup next state.
            self.current_state = self.state_dict[new_state]
            self.current_state.setup()
        except KeyError:
            # State could not be found, exit program.
            self.running = False
    
    def main_loop(self):
        """Perform main loop."""
        while self.running:
            # Update clock.
            self.clock.tick(fps)

            # Handle events.
            self.handle_events()

            # Update the current state.
            self.current_state.update()

            # Draw the current state to the screen.
            self.current_state.draw(self.screen)

            # Update the screen.
            pygame.display.flip()


# Main program.
if __name__ == "__main__":
    # Setup PyGame.
    pygame.init()
    
    # Create state dictionary.
    state_dict = {
            "main menu": MainMenu(),
            "game": Game(),
            "game over": GameOver()
            }
    
    # Setup and start control object.
    app = Control()
    app.setup(state_dict, "main menu")
    app.main_loop()
    
    # Exit program.
    pygame.quit()

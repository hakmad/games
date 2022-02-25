"""Main program."""

import pygame


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
        """Initialise the main menu state."""
        States.__init__(self)

    def setup(self):
        """Setup the main menu state."""
        self.running = True

        # Create the title textbox.
        self.title = Text("Shoot 'Em Up", screen_width // 2, 40, font_size=32)

        # Create navigation buttons.
        self.start_game = Button("Start", self.switch_to_game, screen_width // 2 - 75, 100, 150, 20)
        self.exit_game = Button("Exit", self.exit, screen_width // 2 - 75, 150, 150, 20)

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


class Game(States):
    """Game state."""
    def __init__(self):
        """Initialise the game state."""
        States.__init__(self)

    def setup(self):
        """Setup the main menu state."""
        self.running = True

        # Create the main sprite groups.
        self.sprites = pygame.sprite.Group()
        self.hostiles = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        # Create the player and hostiles.
        self.player = Player()
        self.sprites.add(self.player)

        for i in range(8):
            hostile = Hostile()
            self.sprites.add(hostile)
            self.hostiles.add(hostile)

    def handle_events(self, event):
        """Handle input and events for the game state.

        Arguments:
        event (pygame.event.Event) - input/event to handle.
        """
        # Check if spacebar has been pressed.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet = self.player.shoot()
            self.sprites.add(bullet)
            self.bullets.add(bullet)

    def update(self):
        """Update the game state."""
        # Update the sprites positions.
        self.sprites.update()

        # Check to see if a bullet hit a hostile.
        collisions = pygame.sprite.groupcollide(self.bullets, self.hostiles, True, True)
        for collision in collisions:
            # Increase player score.
            self.player.score += collision.width

            # Create new hostile.
            hostile = Hostile()
            self.sprites.add(hostile)
            self.hostiles.add(hostile)

        # Check to see if a hostile hit the player.
        collisions = pygame.sprite.spritecollide(self.player, self.hostiles, True)
        for collision in collisions:
            # Decrease player health.
            self.player.health -= collision.width

            # Create new hostile.
            hostile = Hostile()
            self.sprites.add(hostile)
            self.hostiles.add(hostile)

        # Check if player is still alive.
        if self.player.health < 0:
            self.running = False

    def draw(self, screen):
        """Draw the game state to the screen.

        Arguments:
        screen (pygame.Surface) - screen to draw to.
        """
        # Fill the screen with black.
        screen.fill(black)

        # Draw the sprites to the screen.
        self.sprites.draw(screen)

        # Update the display.
        pygame.display.flip()


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
            }

    # Setup and start control object.
    app = Control()
    app.setup(state_dict, "main menu")
    app.main_loop()

    # Exit program.
    pygame.quit()

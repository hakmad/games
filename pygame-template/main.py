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

    """
    # Create state dictionary.
    state_dict = {
        # Add states here.
    }

    # Setup and start control object.
    app = Control()
    app.setup(state_dict, ) # Add starting state here.
    app.main_loop()
    """

    # Exit program.
    pygame.quit()

"""Sprites."""

import pygame
import random


from settings import *


class Hostile(pygame.sprite.Sprite):
    """Hostile sprite. Inherits from pygame.sprite.Sprite."""
    def __init__(self):
        """Initialise the new hostile."""
        # Setup the underlying PyGame sprite.
        pygame.sprite.Sprite.__init__(self)

        # Set width, height and colour.
        self.width = random.randrange(20, 40, 5)
        self.height = random.randrange(20, 40, 5)
        self.colour = red

        # Create surface to display hostile.
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.colour)

        # Create rectangle to store hostile and move it to the top of screen.
        self.rect = self.image.get_rect()

        # Set initial vector.
        self.dx = random.randint(-4, 4)
        self.dy = random.randint(2, 10)

    def reset(self):
        """Reset the hostile to the top of the screen."""
        self.rect.x = random.randint(0, screen_width - self.width)
        self.rect.y = -1 * self.height

    def update(self):
        """Update the hostiles position."""
        # Move the hostile according to the vectors.
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Check if hostile has gone beyond the boundaries of the screen.
        if (self.rect.y > screen_height or 
                self.rect.x >= screen_width - self.width or self.rect.x <= 0):
            self.reset()

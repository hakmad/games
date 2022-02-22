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


class Player(pygame.sprite.Sprite):
    """Player sprite. Inherits from pygame.sprite.Sprite."""
    def __init__(self):
        """Initialise the new player."""
        # Setup the underlying PyGame sprite.
        pygame.sprite.Sprite.__init__(self)

        # Set health.
        self.health = 100

        # Set width, height and colour.
        self.width = 80
        self.height = 40
        self.colour = green

        # Create surface to display player.
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.colour)

        # Create rectangle to store the player.
        self.rect = self.image.get_rect()
        self.rect.x = (screen_width // 2) - (self.width // 2)
        self.rect.y = screen_height - self.height - 10

    def update(self):
        """Update the players position."""
        # Set vectors and get pressed keys.
        self.dx = 0

        keystates = pygame.key.get_pressed()

        # Check the pressed keys and adjust vectors.
        if keystates[pygame.K_RIGHT]:
            self.dx = 10
        elif keystates[pygame.K_LEFT]:
            self.dx = -10

        # Move the player according to the vector.
        self.rect.x += self.dx

        # Check if the player has contacted the right of the screen.
        if self.rect.x >= screen_width - self.width:
            self.rect.x = screen_width - self.width

        # Check if the player has contacted the left of the screen.
        if self.rect.x <= 0:
            self.rect.x = 0


class Bullet(pygame.sprite.Sprite):
    """Bullet sprite. Inherits from pygame.sprite.Sprite."""
    def __init__(self, x, y):
        """Initialise the new bullet."""
        # Setup the underlying PyGame sprite.
        pygame.sprite.Sprite.__init__(self)

        # Set width, height and colour.
        self.width = 10
        self.height = 20
        self.colour = blue

        # Create surface to display bullet.
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.colour)

        # Create rectangle to store the bullet.
        self.rect = self.image.get_rect()
        self.rect.x = x - (self.width // 2)
        self.rect.y = y - self.height

        # Set vector.
        self.dy = -10

    def update(self):
        """Update the bullets position."""
        self.rect.y += self.dy

        # Check if the bullet has gone beyond the edge of the screen.
        if self.rect.y - self.height < 0:
            self.kill()

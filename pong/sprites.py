"""Sprites."""

import pygame


from settings import *


class Ball(pygame.sprite.Sprite):
    """Ball sprite. Inherits from pygame.sprite.Sprite."""
    def __init__(self):
        """Initialise the new ball."""
        # Setup the underlying PyGame sprite.
        pygame.sprite.Sprite.__init__(self)
        
        # Set size and colour.
        self.size = 20
        self.colour = white

        # Create surface to display ball.
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.colour)

        # Create rectangle to store the ball.
        self.rect = self.image.get_rect()
        self.reset()

        # Set initial vector.
        self.dx = 0
        self.dy = 0

    def reset(self):
        """Reset ball to center of the screen."""
        self.rect.x = int(screen_width / 2) - int(self.size / 2)
        self.rect.y = int(screen_height / 2) - int(self.size / 2)

    def update(self):
        """Update the balls position."""
        # Move the ball according to the vectors.
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Check if ball has contacted the left or right walls of the screen.
        if self.rect.x >= screen_width - self.size or self.rect.x <= 0:
            self.dx *= -1

        # Check if ball has contacted the top or bottom of the screen.
        if self.rect.y >= screen_height - self.size or self.rect.y <= 0:
            self.dy *= -1


class Paddle(pygame.sprite.Sprite):
    """Paddle sprite. Inherits from pygame.sprite.Sprite."""
    def __init__(self, start_x, up_key, down_key, colour):
        """Initialise the new paddle.

        Arguments:
        start_x (int) - start X position.
        up_key (int) - integer code for key to move paddle up.
        down_key (int) - integer code for key to move paddle down.
        colour (tuple) - colour of the paddle.
        """
        # Setup the underlying 
        pygame.sprite.Sprite.__init__(self)

        # Set score to 0.
        self.score = 0

        # Set keys.
        self.up_key = up_key
        self.down_key = down_key

        # Set size and colour.
        self.size = (10, 100)
        self.colour = colour

        # Create surface to display paddle.
        self.image = pygame.Surface(self.size)
        self.image.fill(self.colour)

        # Create rectangle to store the paddle.
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.reset()

    def reset(self):
        """Reset the paddle to the center of the screen."""
        self.rect.y = int(screen_height / 2) - int(self.size[1] / 2)

    def update(self):
        """Update the paddles position."""
        # Set vector and get pressed keys.
        self.dy = 0
        keystates = pygame.key.get_pressed()

        # Check the pressed keys and change the vector.
        if keystates[self.up_key]:
            self.dy = -10
        if keystates[self.down_key]:
            self.dy = 10

        # Move the paddle according to the vector.
        self.rect.y += self.dy

        # Check if the paddle has contacted the top of the screen.
        if self.rect.y >= screen_height - self.size[1]:
            self.rect.y = screen_height - self.size[1]

        # Check if the paddle has contacted the bottom of the screen.
        if self.rect.y <= 0:
            self.rect.y = 0

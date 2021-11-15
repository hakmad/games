import pygame


from settings import *


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.size = 20
        self.colour = white

        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.colour)

        self.rect = self.image.get_rect()
        self.reset()

        self.dx = 0
        self.dy = 0

    def reset(self):
        self.rect.x = int(screen_width / 2) - int(self.size / 2)
        self.rect.y = int(screen_height / 2) - int(self.size / 2)

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.x >= screen_width - self.size or self.rect.x <= 0:
            self.dx *= -1

        if self.rect.y >= screen_height - self.size or self.rect.y <= 0:
            self.dy *= -1


class Paddle(pygame.sprite.Sprite):
    def __init__(self, start_x, up_key, down_key, colour):
        pygame.sprite.Sprite.__init__(self)

        self.score = 0

        self.up_key = up_key
        self.down_key = down_key

        self.size = (10, 100)
        self.colour = colour

        self.image = pygame.Surface(self.size)
        self.image.fill(self.colour)

        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.reset()

    def reset(self):
        self.rect.y = int(screen_height / 2) - int(self.size[1] / 2)

    def update(self):
        self.dy = 0
        keystates = pygame.key.get_pressed()

        if keystates[self.up_key]:
            self.dy = -10
        if keystates[self.down_key]:
            self.dy = 10

        self.rect.y += self.dy

        if self.rect.y >= screen_height - self.size[1]:
            self.rect.y = screen_height - self.size[1]

        if self.rect.y <= 0:
            self.rect.y = 0

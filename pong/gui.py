import pygame


from settings import *


class Text:
    def __init__(self, text, x_pos, y_pos, font_name=pygame.font.get_default_font(), font_size=18, font_colour=white):
        self.rect = pygame.Rect(x_pos, y_pos, 0, 0)

        self.text = text

        self.font = pygame.font.Font(font_name, font_size)
        self.font_colour = font_colour

    def update_text(self, text):
        self.text = text

    def draw(self, surface):
        rendered_text = self.font.render(self.text, True, self.font_colour)
        location = rendered_text.get_rect(center=self.rect.center)
        surface.blit(rendered_text, location)


class Button(Text):
    def __init__(self, text, function, x_pos, y_pos, width, height, background_colour=black, border_colour=white, font_name=pygame.font.get_default_font(), font_size=18, font_colour=white):
        Text.__init__(self, text, x_pos, y_pos, font_name, font_size, font_colour)

        self.hovered = False
        self.clicked = False

        self.function = function

        self.rect = pygame.Rect(x_pos, y_pos, width, height)

        self.background_colour = background_colour
        self.border_colour = border_colour

    def check_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.hovered == True:
            self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP and self.hovered == True:
            if self.clicked:
                self.function()
            self.clicked = False

    def check_hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
        else:
            self.hovered = False

    def draw(self, surface):
        self.check_hover()
        
        colour = self.background_colour
        font_colour = self.font_colour

        if self.clicked:
            colour = self.border_colour
            font_colour = self.background_colour
        elif self.hovered:
            surface.fill(self.border_colour, self.rect.inflate(4, 4))
        surface.fill(colour, self.rect)

        rendered_text = self.font.render(self.text, True, font_colour)
        location = rendered_text.get_rect(center=self.rect.center)

        surface.blit(rendered_text, location)

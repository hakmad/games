"""GUI elements."""

import pygame


from settings import *


class Text:
    """Class for textboxes."""
    def __init__(self, text, x_pos, y_pos, font_name=pygame.font.get_default_font(), font_size=18, font_colour=white):
        """Initialise a new textbox.

        Arguments:
        text (str) - text to display.
        x_pos (int) - X position of textbox.
        y_pox (int) - Y position of textbox.
        font_name (str) - name of font to use.
        font_size (int) - size of the font.
        font_colour (tuple) - colour of the font.
        """
        # Create a new rectangle to store the textbox.
        self.rect = pygame.Rect(x_pos, y_pos, 0, 0)

        # Set the text of the textbox.
        self.text = text

        # Set font and colour.
        self.font = pygame.font.Font(font_name, font_size)
        self.font_colour = font_colour

    def update_text(self, text):
        """Update the text of a textbox.

        Arguments:
        text (str) - text to update to.
        """
        self.text = text

    def draw(self, surface):
        """Draw the textbox to a surface.

        Arguments:
        surface (pygame.Surface) - surface to draw to.
        """
        # Draw text to surface.
        rendered_text = self.font.render(self.text, True, self.font_colour)
        location = rendered_text.get_rect(center=self.rect.center)
        surface.blit(rendered_text, location)


class Button(Text):
    """Class for buttons. Inherits from Text."""
    def __init__(self, text, function, x_pos, y_pos, width, height, background_colour=black, border_colour=white, font_name=pygame.font.get_default_font(), font_size=18, font_colour=white):
        """Initialise the new button.

        Arguments:
        text (str) - text to display.
        function (function) - function to call when clicked.
        x_pos (int) - X position of button.
        y_pox (int) - Y position of button.
        width (int) - width of the button.
        height (int) - height of the button.
        background_colour (tuple) - colour of the background of the button.
        border_colour (tuple) - colour of the border of the button.
        font_name (str) - name of font to use.
        font_size (int) - size of the font.
        font_colour (tuple) - colour of the font.
        """
        # Setup the underlying textbox.
        Text.__init__(self, text, x_pos, y_pos, font_name, font_size, font_colour)

        # Set flags for button.
        self.hovered = False
        self.clicked = False
        
        # Set callback function.
        self.function = function

        # Create a new rectangle to store the button.
        self.rect = pygame.Rect(x_pos, y_pos, width, height)

        # Set background and border colour.
        self.background_colour = background_colour
        self.border_colour = border_colour

    def check_clicked(self, event):
        """Check if the button has been clicked on.

        Arguments:
        event (pygame.event.Event) - event to check.
        """
        # Check if mouse has been clicked and is over button.
        if event.type == pygame.MOUSEBUTTONDOWN and self.hovered == True:
            # Set flag.
            self.clicked = True
        # Check if button has been released and is over button.
        elif event.type == pygame.MOUSEBUTTONUP and self.hovered == True:
            # Check flag.
            if self.clicked:
                # Call function.
                self.function()
            # Unset flag.
            self.clicked = False

    def check_hover(self):
        """Check if the mouse is hovering over the button."""
        # Check posiiton of mouse.
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # Check flag.
            if not self.hovered:
                # Set flag.
                self.hovered = True
        else:
            # Unset flag.
            self.hovered = False

    def draw(self, surface):
        """Draw the button to a surface.

        Arguments:
        surface (pygame.Surface) - surface to draw to.
        """
        # Check if mouse is hovering over button.
        self.check_hover()
        
        # Set colours for background and font.
        colour = self.background_colour
        font_colour = self.font_colour
        
        # Check flag.
        if self.clicked:
            # Set colours for background and font.
            colour = self.border_colour
            font_colour = self.background_colour
        elif self.hovered:
            # Draw border of button.
            surface.fill(self.border_colour, self.rect.inflate(4, 4))

        # Draw button to surface.
        surface.fill(colour, self.rect)

        # Draw text to surface.
        rendered_text = self.font.render(self.text, True, font_colour)
        location = rendered_text.get_rect(center=self.rect.center)

        surface.blit(rendered_text, location)

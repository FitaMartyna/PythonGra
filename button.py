import pygame

class Button:
    def __init__(self, rectangle, action, label):
        self.rectangle = rectangle
        self.action = action
        self.label = label
        self.clicked = False

    def draw(self, window, draw_text_fn, text_color):
        pygame.draw.rect(window, (255, 255, 255), self.rectangle)
        pygame.draw.rect(window, (0, 0, 0), self.rectangle, 2)
        draw_text_fn(
            self.label,
            text_color,
            self.rectangle.x + 13,
            self.rectangle.y + 8
        )

    def handle_click(self, position):
        if self.rectangle.collidepoint(position) and not self.clicked:
            self.clicked = True
            self.action()

    def reset_click(self):
        self.clicked = False

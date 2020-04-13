import pygame

from game.draw.ui.ui_element import UIElement

pygame.font.init()
LABEL_FONT = pygame.font.SysFont('freesanbold', 15)
LABEL_FONT_COLOR = pygame.Color(0, 0, 0)


class StatBar(UIElement):

    def __init__(self, min_value: int, max_value: int, border_color: pygame.Color, back_color: pygame.Color, bar_color: pygame.Color):
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value
        self.border_color = border_color
        self.back_color = back_color
        self.bar_color = bar_color
        self.value = max_value

    def set_value(self, value: int) -> None:
        self.value = value

    def draw(self, surface, left: int, top: int) -> None:
        self.draw_border(surface, left, top)
        self.draw_background(surface, left, top)
        self.draw_bar(surface, left, top)
        self.draw_labels(surface, left, top)

    def draw_border(self, surface, left: int, top: int) -> None:
        border_rect = pygame.Rect(left, top, 190, 15)
        pygame.draw.rect(surface, self.border_color, border_rect)

    def draw_background(self, surface, left: int, top: int) -> None:
        background_rect = pygame.Rect(left + 1, top + 1, 188, 13)
        pygame.draw.rect(surface, self.back_color, background_rect)

    def draw_bar(self, surface, left: int, top: int) -> None:
        ratio = (self.value - self.min_value) / (self.max_value - self.min_value)
        width = int(188 * ratio)

        bar_rect = pygame.Rect(left + 1, top + 1, width, 13)
        pygame.draw.rect(surface, self.bar_color, bar_rect)

    def draw_labels(self, surface, left: int, top: int) -> None:
        min_label = LABEL_FONT.render(str(self.min_value), True, LABEL_FONT_COLOR)
        min_rect = pygame.Rect(left, top + 15, 0, 0)
        surface.blit(min_label, min_rect)

        max_label = LABEL_FONT.render(str(self.max_value), True, LABEL_FONT_COLOR)
        max_rect = pygame.Rect(left + 175, top + 15, 0, 0)
        surface.blit(max_label, max_rect)

    def update_mouse(self, mouse_position, mouse_clicked) -> None:
        pass

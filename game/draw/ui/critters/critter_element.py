import pygame

from critter.critter import Critter
from game.draw.ui.ui_element import UIElement
from game.draw.ui.util import load_sprite
from game.state import get_state

SLOWED_INDICATOR_COLOR = pygame.Color(175, 250, 255)
SELECTED_INDICATOR_COLOR = pygame.Color(0, 0, 0)


class CritterElement(UIElement):

    def __init__(self, critter: Critter):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.critter = critter
        self.critter_sprite = load_sprite(f"critter_{critter.type}")
        self.critter_sprite_rect = self.critter_sprite.get_rect()

        self.critter_invisible_sprite = None

        if critter.can_go_invisible():
            self.critter_invisible_sprite = load_sprite(f"critter_{critter.type}_invisible")

    def draw(self, surface, left: int, top: int) -> None:
        rectangle = pygame.Rect(left + self.critter.current_x, top + self.critter.current_y, 0, 0)

        if not self.critter.is_invisible():
            surface.blit(self.critter_sprite, rectangle)
        elif self.critter_invisible_sprite is not None:
            surface.blit(self.critter_invisible_sprite, rectangle)

        self.maybe_draw_slowed_indicator(surface, left, top)
        self.rect = pygame.Rect(rectangle.left, rectangle.top, self.critter_sprite_rect.height, self.critter_sprite_rect.width)

        self.maybe_draw_selected_indicator(surface)

    def maybe_draw_slowed_indicator(self, surface, left: int, top: int) -> None:
        if self.critter.is_slow():
            center_x = int(self.critter.current_x + left + (self.critter_sprite_rect.width / 2))
            center_y = int(self.critter.current_y + top + (self.critter_sprite_rect.height / 2))

            circle_center = center_x, center_y
            circle_radius = int((self.critter_sprite_rect.width / 2) + 2)
            pygame.draw.circle(surface, SLOWED_INDICATOR_COLOR, circle_center, circle_radius, 1)

    def maybe_draw_selected_indicator(self, surface) -> None:
        if get_state().get_selected_critter() == self.critter:
            pygame.draw.rect(surface, SELECTED_INDICATOR_COLOR, self.rect, 1)

    def set_clock_tick(self, clock_tick: int) -> None:
        self.critter.add_clock_tick(clock_tick)

    def update_mouse(self, mouse_position, mouse_clicked) -> None:
        state = get_state()
        if self.rect.collidepoint(mouse_position):
            state.set_hover(self, True)

            if mouse_clicked:
                state.set_selected_critter(self.critter)

        else:
            state.set_hover(self, False)

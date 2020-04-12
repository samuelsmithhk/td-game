from typing import Optional

import pygame

from critter.critter import Critter
from game.draw.ui.sim_entity_viewer.critter_viewer.stat_bar import StatBar
from game.draw.ui.ui_element import UIElement
from game.state import get_state

pygame.font.init()

BAR_BORDER_COLOR = pygame.Color(0, 0, 0)

HEALTH_BAR_BACKGROUND_COLOR = pygame.Color(255, 0, 0)
HEALTH_BAR_COLOR = pygame.Color(0, 255, 0)

DISTANCE_BAR_BACKGROUND_COLOR = pygame.Color(195, 220, 220)
DISTANCE_BAR_COLOR = pygame.Color(100, 140, 175)

HEADER_FONT = pygame.font.SysFont('Verdana', 21)
SUB_HEADER_FONT = pygame.font.SysFont('Verdana', 18)
STAT_FONT = pygame.font.SysFont('Verdana', 15)

HEADER_FONT_COLOR = pygame.Color(0, 0, 0)
SUB_HEADER_FONT_COLOR = pygame.Color(0, 0, 0)
STAT_FONT_COLOR = pygame.Color(0, 0, 0)

CLOSE_BUTTON_BORDER_COLOR = pygame.Color(255, 255, 255)
CLOSE_BUTTON_COLOR = pygame.Color(255, 100, 100)
CLOSE_BUTTON_HOVER_COLOR = pygame.Color(255, 50, 50)
CLOSE_BUTTON_FONT = pygame.font.SysFont('Verdana', 60)
CLOSE_BUTTON_FONT_COLOR = pygame.Color(255, 255, 255)




CRITTER_TYPE_DISPLAY_NAMES = {
    'base': 'Critter',
    'base_boss': 'Boss Critter',
    'invisible': 'Stealthy Critter',
    'invisible_boss': 'Stealthy Boss Critter',
    'resistant': 'Resistant Critter',
    'resistant_boss': 'Resistant Critter Boss',
    'speeder': 'Speedy Critter',
    'speeder_boss': 'Speedy Critter Boss'
}


class CritterViewer(UIElement):

    def __init__(self):
        super().__init__()
        self._critter: Optional[Critter] = None
        self.close_button_rect = pygame.Rect(0, 0, 0, 0)

    def set_critter(self, critter: Critter) -> None:
        self._critter = critter

    def draw(self, surface, left: int, top: int) -> None:
        self.draw_header(surface, left, top)
        self.draw_health_bar(surface, left, top)
        self.draw_distance_travelled(surface, left, top)
        self.draw_close_button(surface, left, top)

    def draw_header(self, surface, left: int, top: int) -> None:
        header_message = CRITTER_TYPE_DISPLAY_NAMES[self._critter.type]
        header_label = HEADER_FONT.render(header_message, True, HEADER_FONT_COLOR)
        header_rectangle = pygame.Rect(left + 5, top + 5, 0, 0)
        surface.blit(header_label, header_rectangle)

    def draw_health_bar(self, surface, left: int, top: int) -> None:
        health_label = SUB_HEADER_FONT.render("Health", True, SUB_HEADER_FONT_COLOR)
        health_rectangle = pygame.Rect(left + 5, top + 25, 0, 0)
        surface.blit(health_label, health_rectangle)

        health_bar = StatBar(0, self._critter.starting_health, BAR_BORDER_COLOR, HEALTH_BAR_BACKGROUND_COLOR, HEALTH_BAR_COLOR)
        health_bar.set_value(self._critter.health)
        health_bar.draw(surface, left + 5, top + 40)

    def draw_distance_travelled(self, surface, left: int, top: int) -> None:
        distance_message = f"Distance Travelled"
        distance_label = SUB_HEADER_FONT.render(distance_message, True, SUB_HEADER_FONT_COLOR)
        distance_rectangle = pygame.Rect(left + 5, top + 70, 0, 0)
        surface.blit(distance_label, distance_rectangle)

        distance_bar = StatBar(0, self._critter.total_distance, BAR_BORDER_COLOR, DISTANCE_BAR_BACKGROUND_COLOR, DISTANCE_BAR_COLOR)
        distance_bar.set_value(self._critter.distance_travelled)
        distance_bar.draw(surface, left + 5, top + 85)

    def draw_close_button(self, surface, left: int, top: int) -> None:
        border_rectangle = pygame.Rect(left + 65, top + 105, 60, 40)
        pygame.draw.rect(surface, CLOSE_BUTTON_BORDER_COLOR, border_rectangle)

        self.close_button_rect = border_rectangle

        background_rectangle = pygame.Rect(left + 66, top + 106, 58, 38)
        color_to_draw = CLOSE_BUTTON_HOVER_COLOR if get_state().get_hover(self) else CLOSE_BUTTON_COLOR
        pygame.draw.rect(surface, color_to_draw, background_rectangle)

        x_label = CLOSE_BUTTON_FONT.render("X", True, CLOSE_BUTTON_FONT_COLOR)
        x_rectangle = pygame.Rect(left + 80, top + 108, 0, 0)
        surface.blit(x_label, x_rectangle)

    def update_mouse(self, mouse_position, mouse_clicked) -> None:
        state = get_state()

        if self.close_button_rect.collidepoint(mouse_position):
            state.set_hover(self, True)

            if mouse_clicked:
                state.set_selected_critter(None)
        else:
            state.set_hover(self, False)

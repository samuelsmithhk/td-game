from typing import Optional

import pygame

from game.draw.ui.ui_element import UIElement
from game.state import get_state

BACKGROUND_COLOR_UNPAUSED = pygame.Color(185, 185, 185)
BACKGROUND_COLOR_PAUSED = pygame.Color(0, 0, 0)

BORDER_COLOR = pygame.Color(0, 0, 0)

RESUME_ICON_COLOR = pygame.Color(255, 255, 255)
PAUSE_ICON_COLOR = pygame.Color(255, 255, 255)

LIME = pygame.Color(128, 255, 0)


class SimToggle(UIElement):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.clock_tick = 0
        self.last_interacted_clock_tick = 0

    def draw(self, surface, left: int, top: int) -> None:
        # width = 60
        # height = 50
        #
        # rectangle = pygame.Rect(left, top, width, height)
        # pygame.draw.rect(surface, LIME, rectangle)

        is_paused = get_state().is_paused()

        self.draw_border(surface, left, top, is_paused)
        self.draw_background(surface, left, top, is_paused)

        if is_paused:
            self.draw_resume_icon(surface, left, top)
        else:
            self.draw_pause_icon(surface, left, top)

    def draw_border(self, surface, left: int, top: int, is_paused: bool) -> None:
        width = 60
        height = 50
        rectangle = pygame.Rect(left, top, width, height)
        self.rect = rectangle

        pygame.draw.rect(surface, BORDER_COLOR, rectangle)

    @staticmethod
    def draw_background(surface, left: int, top: int, is_paused: bool) -> None:
        width = 58
        height = 48
        rectangle = pygame.Rect(left + 1, top + 1, width, height)

        color_to_draw = (
            BACKGROUND_COLOR_PAUSED if is_paused else BACKGROUND_COLOR_UNPAUSED
        )

        pygame.draw.rect(surface, color_to_draw, rectangle)

    @staticmethod
    def draw_resume_icon(surface, left: int, top: int) -> None:
        top_left_point = (left + 15, top + 10)
        bottom_left_point = (left + 15, top + 40)
        right_point = (left + 45, top + 25)

        points = (top_left_point, bottom_left_point, right_point)

        pygame.draw.polygon(surface, RESUME_ICON_COLOR, points)

    @staticmethod
    def draw_pause_icon(surface, left: int, top: int) -> None:
        left_bar_border_rectangle = pygame.Rect(left + 16, top + 10, 11, 33)
        right_bar_border_rectangle = pygame.Rect(left + 31, top + 10, 11, 33)

        pygame.draw.rect(surface, BORDER_COLOR, left_bar_border_rectangle)
        pygame.draw.rect(surface, BORDER_COLOR, right_bar_border_rectangle)

        left_bar_rectangle = pygame.Rect(left + 17, top + 11, 9, 31)
        right_bar_rectangle = pygame.Rect(left + 32, top + 11, 9, 31)

        pygame.draw.rect(surface, PAUSE_ICON_COLOR, left_bar_rectangle)
        pygame.draw.rect(surface, PAUSE_ICON_COLOR, right_bar_rectangle)

    def add_clock_tick(self, clock_tick: int) -> None:
        self.clock_tick += clock_tick

    def update_mouse(self, mouse_position, mouse_clicked) -> None:
        state = get_state()

        if self.rect.collidepoint(mouse_position):
            state.set_hover(self, True)

            if mouse_clicked:
                if self.clock_tick - self.last_interacted_clock_tick > 250:
                    state.set_paused(not state.is_paused())
                    self.last_interacted_clock_tick = self.clock_tick
        else:
            state.set_hover(self, False)

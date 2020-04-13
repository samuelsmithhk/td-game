from abc import ABC, abstractmethod

import pygame

from game.draw.ui.ui_element import UIElement
from game.draw.ui.util import load_sprite
from game.state import get_state


class Cursor(UIElement):
    def __init__(self):
        super().__init__()
        self.mouse_position = 0, 0
        self.cursor_bank = self.load_cursor_bank()

    @staticmethod
    def load_cursor_bank():
        return {
            "default": load_sprite("cursor_default"),
            "hover": load_sprite("cursor_hover"),
            "basic": load_sprite("tower_basic"),
            "basic_no": load_sprite("tower_basic_no"),
            "machine_gun": load_sprite("tower_machine_gun"),
            "machine_gun_no": load_sprite("tower_machine_gun_no"),
            "sniper": load_sprite("tower_sniper"),
            "sniper_no": load_sprite("tower_sniper_no"),
            "glue": load_sprite("tower_glue"),
            "glue_no": load_sprite("tower_glue_no"),
        }

    def update_mouse(self, mouse_position, mouse_clicked) -> None:
        self.mouse_position = mouse_position

    def draw(self, surface, left: int, top: int) -> None:
        cursor_to_draw = self.determine_cursor()
        ctd_rect = cursor_to_draw.get_rect()

        rectangle = pygame.Rect(
            self.mouse_position[0],
            self.mouse_position[1],
            ctd_rect.width,
            ctd_rect.height,
        )
        get_state().set_cursor_rect(rectangle)

        surface.blit(cursor_to_draw, rectangle)

    def determine_cursor(self):
        state = get_state()

        if state.is_cursor_in_playable_space():
            selected_tower_definition = state.get_selected_tower_definition()

            if selected_tower_definition:
                if state.is_cursor_in_buildable_space():
                    return self.cursor_bank[selected_tower_definition.tower_name]
                else:
                    return self.cursor_bank[
                        f"{selected_tower_definition.tower_name}_no"
                    ]

        if state.get_any_hover():
            return self.cursor_bank["hover"]

        return self.cursor_bank["default"]

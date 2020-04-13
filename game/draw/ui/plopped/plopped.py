import pygame

from critter.critter import Critter
from game.draw.ui.ui_element import UIElement
from game.draw.ui.util import load_sprite
from game.state import get_state
from tower.ploppable import Ploppable

HOVER_BORDER_COLOR = pygame.Color(100, 100, 100)
SELECTED_BORDER_COLOR = pygame.Color(0, 0, 0)
RANGE_CIRCLE_COLOR = pygame.Color(255, 255, 255)


class Plopped(UIElement):
    def __init__(self, ploppable: Ploppable, left: int, top: int):
        super().__init__()
        self.ploppable = ploppable
        tower_definition = ploppable.get_tower_definition()
        self.tower_sprites = self.load_tower_sprites(tower_definition.tower_name)
        self.ts_rect = self.tower_sprites[0].get_rect()
        self.left = left
        self.top = top
        self.rect = pygame.Rect(
            self.left, self.top, self.ts_rect.width, self.ts_rect.height
        )
        self._ready_to_shoot = False

    @staticmethod
    def load_tower_sprites(tower_name: str):
        return [load_sprite(f"tower_{tower_name}_{level}") for level in range(1, 6)]

    def get_plop_id(self) -> str:
        return self.ploppable.get_plop_id()

    def draw(self, surface, left: int, top: int) -> None:
        state = get_state()

        is_selected = state.get_selected_ploppable() == self.ploppable

        if is_selected:
            self.draw_range_circle(surface)

        rectangle = pygame.Rect(self.left, self.top, 0, 0)
        surface.blit(
            self.tower_sprites[self.ploppable.get_current_level() - 1], rectangle
        )

        if state.get_hover(self):
            pygame.draw.rect(surface, HOVER_BORDER_COLOR, self.rect, 1)

        if is_selected:
            pygame.draw.rect(surface, SELECTED_BORDER_COLOR, self.rect, 1)

    def draw_range_circle(self, surface):
        tower_range = self.ploppable.get_tower_stats()["range"]
        tower_rectangle = self.rect
        center_x = int(tower_rectangle.left + (tower_rectangle.width / 2))
        center_y = int(tower_rectangle.top + (tower_rectangle.height / 2))

        pygame.draw.circle(
            surface, RANGE_CIRCLE_COLOR, (center_x, center_y), tower_range, 2
        )

    def update_mouse(self, mouse_position, mouse_clicked) -> None:
        state = get_state()
        if self.rect.colliderect(get_state().get_cursor_rect()):
            state.set_hover(self, True)
            state.set_cursor_in_buildable_space(False)

            if mouse_clicked:
                selected_tower_definition = state.get_selected_tower_definition()

                if selected_tower_definition is None:
                    state.set_selected_ploppable(self.ploppable)
        else:
            state.set_hover(self, False)

    def shoot(self, critter: Critter) -> int:
        self.ploppable.shoot(critter)
        self._ready_to_shoot = False
        return self.ploppable.get_tower_stats()["damage"]

    def reload(self) -> None:
        self._ready_to_shoot = True

    def is_reloaded(self) -> bool:
        return self._ready_to_shoot

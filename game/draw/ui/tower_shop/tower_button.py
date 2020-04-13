import pygame

from game.draw.ui.ui_element import UIElement
from game.draw.ui.util import load_sprite
from game.state import get_state
from tower.tower_definitions import TowerDefinition

BACKGROUND_COLOR = pygame.Color(185, 185, 185)
BACKGROUND_COLOR_HOVER = pygame.Color(125, 125, 125)
BACKGROUND_COLOR_CLICKED = pygame.Color(75, 75, 75)
BACKGROUND_COLOR_SELECTED = pygame.Color(0, 0, 0)
BACKGROUND_COLOR_DISABLED = pygame.Color(225, 225, 225)

BORDER_COLOR = pygame.Color(0, 0, 0)

pygame.font.init()
TEXT_FONT = pygame.font.SysFont("freesanbold", 21)

TOWER_NAME_FONT_COLOR = pygame.Color(0, 0, 0)
TOWER_NAME_FONT_COLOR_SELECTED = pygame.Color(255, 255, 255)
TOWER_NAME_FONT_COLOR_DISABLED = pygame.Color(175, 175, 175)
PRICE_FONT_COLOR = pygame.Color(34, 171, 7)
PRICE_FONT_COLOR_DISABLED = pygame.Color(255, 0, 0)


class TowerButton(UIElement):
    def __init__(self, tower_definition: TowerDefinition):
        super().__init__()
        self.tower_definition = tower_definition
        self.tower_sprite = load_sprite(f"tower_{tower_definition.tower_name}")
        self.rect = pygame.Rect(0, 0, 0, 0)

    def draw(self, surface, left: int, top: int) -> None:
        is_selected = self.is_tower_selected()
        is_enabled = (
            get_state().get_current_money() >= self.tower_definition.level_one_price
        )

        self.draw_border(surface, left, top)
        self.draw_background(
            surface, left, top, is_selected=is_selected, is_enabled=is_enabled
        )
        self.draw_tower_sprite(surface, left, top)
        self.draw_tower_name(
            surface, left, top, is_selected=is_selected, is_enabled=is_enabled
        )
        self.draw_price(surface, left, top, is_enabled=is_enabled)

    @staticmethod
    def draw_border(surface, left: int, top: int) -> None:
        width = 150
        height = 50

        rectangle = pygame.Rect(left, top, width, height)
        pygame.draw.rect(surface, BORDER_COLOR, rectangle)

    def draw_background(
        self,
        surface,
        left: int,
        top: int,
        is_selected: bool = False,
        is_enabled: bool = True,
    ) -> None:
        width = 148
        height = 48

        rectangle = pygame.Rect(left + 1, top + 1, width, height)
        self.rect = rectangle

        color_to_draw = BACKGROUND_COLOR

        if is_selected:
            color_to_draw = BACKGROUND_COLOR_SELECTED
        elif get_state().get_hover(self):
            color_to_draw = BACKGROUND_COLOR_HOVER

        if self.clicked:
            color_to_draw = BACKGROUND_COLOR_CLICKED

        if not is_enabled:
            color_to_draw = BACKGROUND_COLOR_DISABLED

        pygame.draw.rect(surface, color_to_draw, rectangle)

    def draw_tower_sprite(self, surface, left: int, top: int) -> None:
        rectangle = pygame.Rect(left + 5, top + 12, 0, 0)
        surface.blit(self.tower_sprite, rectangle)

    def draw_tower_name(
        self,
        surface,
        left: int,
        top: int,
        is_selected: bool = False,
        is_enabled: bool = True,
    ) -> None:

        color_to_draw = (
            TOWER_NAME_FONT_COLOR_SELECTED if is_selected else TOWER_NAME_FONT_COLOR
        )
        color_to_draw = color_to_draw if is_enabled else TOWER_NAME_FONT_COLOR_DISABLED

        tower_name_label = TEXT_FONT.render(
            self.tower_definition.tower_human_readable_name, True, color_to_draw
        )

        rectangle = pygame.Rect(left + 35, top + 18, 0, 0)
        surface.blit(tower_name_label, rectangle)

    def draw_price(self, surface, left: int, top: int, is_enabled: bool = True) -> None:

        color_to_draw = PRICE_FONT_COLOR if is_enabled else PRICE_FONT_COLOR_DISABLED

        price_label = TEXT_FONT.render(
            f"${self.tower_definition.level_one_price}", True, color_to_draw
        )

        rectangle = pygame.Rect(left + 120, top + 18, 0, 0)
        surface.blit(price_label, rectangle)

    def update_mouse(self, mouse_position, mouse_clicked) -> None:
        state = get_state()
        is_enabled = (
            get_state().get_current_money() >= self.tower_definition.level_one_price
        )

        if self.rect.collidepoint(mouse_position) and is_enabled:
            state.set_hover(self, True)

            if mouse_clicked:
                state.set_selected_tower_definition(self.tower_definition)
                state.set_selected_ploppable(None)
                self.clicked = True
            else:
                self.clicked = False
        else:
            state.set_hover(self, False)

    def is_tower_selected(self) -> bool:
        return get_state().get_selected_tower_definition() == self.tower_definition

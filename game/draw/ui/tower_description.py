from typing import Optional, List

import pygame

from game.draw.ui.ui_element import UIElement
from game.draw.ui.util import load_sprite
from game.state import get_state
from tower.tower_definitions import TowerDefinition
from tower.util import get_tower_names_ui_order

BORDER_COLOR = pygame.Color(0, 0, 0)
BACKGROUND_COLOR = pygame.Color(185, 185, 185)
PRICES_BACKGROUND_COLOR = pygame.Color(205, 205, 205)
DESELECT_COLOR_ONE = pygame.Color(255, 100, 100)
DESELECT_COLOR_ONE_HOVER = pygame.Color(255, 50, 50)
DESELECT_COLOR_TWO = pygame.Color(255, 255, 255)

pygame.font.init()
HEADER_FONT = pygame.font.SysFont('freesanbold', 30)
DESCRIPTION_FONT = pygame.font.SysFont('freesanbold', 20)
UPGRADE_FONT = pygame.font.SysFont('freesanbold', 15)
DESELECT_FONT = pygame.font.SysFont('freesanbold', 60)

HEADER_FONT_COLOR = pygame.Color(0, 0, 0)
DESCRIPTION_FONT_COLOR = pygame.Color(0, 0, 0)
UPGRADE_FONT_COLOR = pygame.Color(0, 0, 0)
UPGRADE_PRICE_FONT_COLOR = pygame.Color(34, 171, 7)
DESELECT_FONT_COLOR = pygame.Color(255, 255, 255)


class TowerDescription(UIElement):

    def __init__(self):
        super().__init__()
        self.deselect_rect = pygame.Rect(0, 0, 0, 0)
        self.tower_sprites = self.load_tower_sprites()

    @staticmethod
    def load_tower_sprites():
        tower_names = get_tower_names_ui_order()

        tower_sprites = {}
        for tower_name in tower_names:
            tower_sprite = load_sprite(f"tower_{tower_name}_large")
            tower_sprites[tower_name] = tower_sprite

        return tower_sprites

    def draw(self, surface, left: int, top: int) -> None:
        self.draw_border(surface, left, top)
        self.draw_background(surface, left, top)

        selected_tower_definition = self.get_selected_tower_definition()

        if selected_tower_definition:
            self.draw_tower_sprite(surface, left, top, selected_tower_definition)
            self.draw_tower_name(surface, left, top, selected_tower_definition)
            self.draw_tower_description(surface, left, top, selected_tower_definition)
            self.draw_tower_upgrade_prices(surface, left, top, selected_tower_definition)
            self.draw_tower_deselect_button(surface, left, top)

    @staticmethod
    def draw_border(surface, left: int, top: int) -> None:
        width = 600
        height = 100

        rectangle = pygame.Rect(left, top, width, height)
        pygame.draw.rect(surface, BORDER_COLOR, rectangle)

    @staticmethod
    def draw_background(surface, left: int, top: int) -> None:
        width = 598
        height = 98

        rectangle = pygame.Rect(left + 1, top + 1, width, height)
        pygame.draw.rect(surface, BACKGROUND_COLOR, rectangle)

    def draw_tower_sprite(self, surface, left: int, top: int, tower_definition: TowerDefinition) -> None:
        rectangle = pygame.Rect(left + 10, top + 12, 0, 0)
        sprite_to_draw = self.tower_sprites[tower_definition.tower_name]
        surface.blit(sprite_to_draw, rectangle)

    @staticmethod
    def draw_tower_name(surface, left: int, top: int, tower_definition: TowerDefinition) -> None:
        tower_name_label = HEADER_FONT.render(tower_definition.tower_human_readable_name, True, HEADER_FONT_COLOR)

        rectangle = pygame.Rect(left + 100, top + 12, 0, 0)
        surface.blit(tower_name_label, rectangle)

    @staticmethod
    def draw_tower_description(surface, left: int, top: int, tower_definition: TowerDefinition) -> None:
        description_one_label = DESCRIPTION_FONT.render(tower_definition.description_line_1, True,
                                                        DESCRIPTION_FONT_COLOR)
        description_two_label = DESCRIPTION_FONT.render(tower_definition.description_line_2, True,
                                                        DESCRIPTION_FONT_COLOR)
        description_three_label = DESCRIPTION_FONT.render(tower_definition.description_line_3, True,
                                                          DESCRIPTION_FONT_COLOR)

        description_one_rectangle = pygame.Rect(left + 115, top + 40, 0, 0)
        description_two_rectangle = pygame.Rect(left + 115, top + 60, 0, 0)
        description_three_rectangle = pygame.Rect(left + 115, top + 80, 0, 0)

        surface.blit(description_one_label, description_one_rectangle)
        surface.blit(description_two_label, description_two_rectangle)
        surface.blit(description_three_label, description_three_rectangle)

    def draw_tower_upgrade_prices(self, surface, left: int, top: int, tower_definition: TowerDefinition) -> None:
        width = 180

        upgrade_prices = self.get_upgrade_prices(tower_definition)

        height = 19
        top_offset = 0
        for upgrade_level, upgrade_price in enumerate(upgrade_prices):
            border_rectangle = pygame.Rect(left + 330, top + 12 + top_offset, width, height + 1)
            pygame.draw.rect(surface, BORDER_COLOR, border_rectangle)

            background_rectangle = pygame.Rect(left + 331, top + 13 + top_offset, width - 2, height - 1)
            pygame.draw.rect(surface, PRICES_BACKGROUND_COLOR, background_rectangle)

            upgrade_description_message = f"Upgrade to level {upgrade_level + 2} costs:"
            upgrade_description_label = UPGRADE_FONT.render(upgrade_description_message, True, DESCRIPTION_FONT_COLOR)
            upgrade_description_rectangle = pygame.Rect(left + 333, top + 17 + top_offset, 0, 0)
            surface.blit(upgrade_description_label, upgrade_description_rectangle)

            upgrade_price_message = f"${upgrade_price}"
            upgrade_price_label = UPGRADE_FONT.render(upgrade_price_message, True, UPGRADE_PRICE_FONT_COLOR)
            upgrade_price_rectangle = pygame.Rect(left + 330 + width - 25, top + 17 + top_offset, 0, 0)
            surface.blit(upgrade_price_label, upgrade_price_rectangle)

            top_offset += 19

    @staticmethod
    def get_upgrade_prices(tower_definition: TowerDefinition) -> List[int]:
        return [
            tower_definition.level_two_price,
            tower_definition.level_three_price,
            tower_definition.level_four_price,
            tower_definition.level_five_price
        ]

    def draw_tower_deselect_button(self, surface, left: int, top: int) -> None:
        width = 50
        height = 50

        border_rectangle = pygame.Rect(left + 530, top + 25, width, height)
        self.deselect_rect = border_rectangle
        pygame.draw.rect(surface, DESELECT_COLOR_TWO, border_rectangle)

        background_rectangle = pygame.Rect(left + 532, top + 27, width - 4, height - 4)

        hover = get_state().get_hover(self)

        background_color = DESELECT_COLOR_ONE if not hover else DESELECT_COLOR_ONE_HOVER
        pygame.draw.rect(surface, background_color, background_rectangle)

        deselect_label = DESELECT_FONT.render("X", True, DESELECT_FONT_COLOR)
        deselect_label_rectangle = pygame.Rect(left + 541, top + 33, 0, 0)
        surface.blit(deselect_label, deselect_label_rectangle)

    @staticmethod
    def get_selected_tower_definition() -> Optional[TowerDefinition]:
        return get_state().get_selected_tower_definition()

    def update_mouse(self, mouse_position, mouse_clicked) -> None:
        state = get_state()

        if self.deselect_rect.collidepoint(mouse_position):
            state.set_hover(self, True)

            if mouse_clicked:
                get_state().set_selected_tower_definition(None)
        else:
            state.set_hover(self, False)

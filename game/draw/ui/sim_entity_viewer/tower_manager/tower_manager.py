import pygame

from game.draw.ui.sim_entity_viewer.tower_manager.buttons.close_button import CloseButton
from game.draw.ui.sim_entity_viewer.tower_manager.buttons.sell_button import SellButton
from game.draw.ui.sim_entity_viewer.tower_manager.buttons.upgrade_button import UpgradeButton
from game.draw.ui.ui_element import UIElement
from tower.ploppable import Ploppable

BORDER_COLOR = pygame.Color(0, 0, 0)
BACKGROUND_COLOR = pygame.Color(185, 185, 185)
STATS_BACKGROUND_COLOR = pygame.Color(205, 205, 205)

pygame.font.init()
HEADER_FONT = pygame.font.SysFont('Verdana', 21)
STAT_FONT = pygame.font.SysFont('Verdana', 15)

HEADER_FONT_COLOR = pygame.Color(0, 0, 0)
STAT_FONT_COLOR = pygame.Color(0, 0, 0)

STATS_DISPLAY_ORDER = [
    ('damage', 'Damage'),
    ('reload_time', 'Reload Time'),
    ('range', 'Range'),
    ('special', 'Spec')
]

CREDITS_DISPLAY_ORDER = [
    ('rounds', 'Rounds'),
    ('shots', 'Shots'),
    ('damage', 'Damage'),
    ('kills', 'Kills')
]


class TowerManager(UIElement):

    def __init__(self):
        super().__init__()
        self.tower = None

        self.upgrade_button = UpgradeButton()
        self.sell_button = SellButton()
        self.close_button = CloseButton()

    def set_tower(self, tower: Ploppable) -> None:
        self.upgrade_button.set_tower(tower)
        self.sell_button.set_tower(tower)
        self.close_button.set_tower(tower)
        self.tower = tower

    def draw(self, surface, left: int, top: int) -> None:
        self.draw_tower_name(surface, left, top)
        self.draw_tower_stats(surface, left, top)
        self.draw_tower_credits(surface, left, top)

        self.upgrade_button.draw(surface, left + 5, top + 105)
        self.sell_button.draw(surface, left + 68, top + 105)
        self.close_button.draw(surface, left + 131, top + 105)

    def draw_tower_name(self, surface, left: int, top: int) -> None:
        tower_definition = self.tower.get_tower_definition()
        tower_name_message = f"{tower_definition.tower_human_readable_name} Tower Level {self.tower.get_current_level()}"
        tower_name_label = HEADER_FONT.render(tower_name_message, True, HEADER_FONT_COLOR)

        rectangle = pygame.Rect(left + 5, top + 5, 0, 0)
        surface.blit(tower_name_label, rectangle)

    def draw_tower_stats(self, surface, left: int, top: int) -> None:
        tower_stats = self.tower.get_tower_stats()

        width = 105
        height = 19
        top_offset = 0
        for stat_name, stat_display in STATS_DISPLAY_ORDER:
            border_rectangle = pygame.Rect(left + 5, top + 25 + top_offset, width, height + 1)
            pygame.draw.rect(surface, BORDER_COLOR, border_rectangle)

            background_rectangle = pygame.Rect(left + 6, top + 26 + top_offset, width - 2, height - 1)
            pygame.draw.rect(surface, STATS_BACKGROUND_COLOR, background_rectangle)

            stat_message = f"{stat_display}: {tower_stats[stat_name]}"
            stat_label = STAT_FONT.render(stat_message, True, STAT_FONT_COLOR)
            stat_rectangle = pygame.Rect(left + 8, top + 29 + top_offset, 0, 0)
            surface.blit(stat_label, stat_rectangle)

            top_offset += 19

    def draw_tower_credits(self, surface, left: int, top: int) -> None:
        tower_credits = self.tower.get_credits()
        width = 85
        height = 19
        top_offset = top + 25
        left_offset = left + 111

        for credit_name, credit_display in CREDITS_DISPLAY_ORDER:
            border_rectangle = pygame.Rect(left_offset, top_offset, width, height + 1)
            pygame.draw.rect(surface, BORDER_COLOR, border_rectangle)

            background_rectangle = pygame.Rect(left_offset + 1, top_offset + 1, width - 2, height - 1)
            pygame.draw.rect(surface, STATS_BACKGROUND_COLOR, background_rectangle)

            credit_message = f"{credit_display}: {tower_credits[credit_name]}"
            credit_label = STAT_FONT.render(credit_message, True, STAT_FONT_COLOR)
            credit_rectangle = pygame.Rect(left_offset + 3, top_offset + 4, 0, 0)
            surface.blit(credit_label, credit_rectangle)

            top_offset += 19

    def update_mouse(self, mouse_position, mouse_clicked) -> None:
        self.upgrade_button.update_mouse(mouse_position, mouse_clicked)
        self.sell_button.update_mouse(mouse_position, mouse_clicked)
        self.close_button.update_mouse(mouse_position, mouse_clicked)

    def add_clock_tick(self, clock_tick: int) -> None:
        self.upgrade_button.add_clock_tick(clock_tick)
        self.sell_button.add_clock_tick(clock_tick)
        self.close_button.add_clock_tick(clock_tick)

import pygame

from game.draw.ui.sim_entity_viewer.tower_manager.buttons.button import TowerManagerButton
from game.state import get_state

pygame.font.init()

LABEL_FONT = pygame.font.SysFont('freesanbold', 15)
PRICE_FONT = pygame.font.SysFont('freesanbold', 20)

LABEL_FONT_COLOR = pygame.Color(0, 0, 0)
PRICE_FONT_COLOR = pygame.Color(10, 175, 0)
CANT_AFFORD_FONT_COLOR = pygame.Color(255, 0, 0)

BORDER_COLOR = pygame.Color(0, 0, 0)

BUTTON_COLOR = pygame.Color(255, 255, 0)
BUTTON_COLOR_HOVER = pygame.Color(200, 220, 0)
BUTTON_COLOR_DISABLED = pygame.Color(255, 255, 230)


class UpgradeButton(TowerManagerButton):

    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)

    def draw(self, surface, left: int, top: int) -> None:
        self.draw_border(surface, left, top)

        if not self.tower.is_upgradeable():
            self.draw_tower_max_level_button(surface, left, top)
        elif self.tower.get_upgrade_price() > get_state().get_current_money():
            self.draw_upgrade_unaffordable_button(surface, left, top)
        else:
            self.draw_upgrade_button(surface, left, top)

    def draw_upgrade_button(self, surface, left: int, top: int) -> None:
        self.draw_upgrade_background(surface, left, top)
        self.draw_upgrade_label(surface, left, top)

    def draw_tower_max_level_button(self, surface, left: int, top: int) -> None:
        self.draw_disabled_background(surface, left, top)
        self.draw_tower_max_level_label(surface, left, top)

    def draw_upgrade_unaffordable_button(self, surface, left: int, top: int) -> None:
        self.draw_disabled_background(surface, left, top)
        self.draw_upgrade_unaffordable_label(surface, left, top)

    def draw_border(self, surface, left: int, top: int) -> None:
        border_rectangle = pygame.Rect(left, top, 60, 40)
        pygame.draw.rect(surface, BORDER_COLOR, border_rectangle)
        self.rect = border_rectangle

    def draw_upgrade_background(self, surface, left: int, top: int) -> None:
        background_rectangle = pygame.Rect(left + 1, top + 1, 58, 38)

        color_to_draw = BUTTON_COLOR_HOVER if get_state().get_hover(self) else BUTTON_COLOR
        pygame.draw.rect(surface, color_to_draw, background_rectangle)

    @staticmethod
    def draw_disabled_background(surface, left: int, top: int) -> None:
        background_rectangle = pygame.Rect(left + 1, top + 1, 58, 38)
        pygame.draw.rect(surface, BUTTON_COLOR_DISABLED, background_rectangle)

    def draw_upgrade_label(self, surface, left: int, top: int):
        upgrade_label = LABEL_FONT.render("UPGRADE", True, LABEL_FONT_COLOR)
        label_rectangle = pygame.Rect(left + 5, top + 10, 0, 0)
        surface.blit(upgrade_label, label_rectangle)

        price_message = f"${self.tower.get_upgrade_price()}"
        price_label = PRICE_FONT.render(price_message, True, PRICE_FONT_COLOR)
        price_rectangle = pygame.Rect(left + 20, top + 20, 0, 0)
        surface.blit(price_label, price_rectangle)

    @staticmethod
    def draw_tower_max_level_label(surface, left: int, top: int) -> None:
        max_label = LABEL_FONT.render("MAX", True, LABEL_FONT_COLOR)
        max_rectangle = pygame.Rect(left + 18, top + 10, 0, 0)
        surface.blit(max_label, max_rectangle)

        level_label = LABEL_FONT.render("LEVEL", True, LABEL_FONT_COLOR)
        level_rectangle = pygame.Rect(left + 13, top + 20, 0, 0)
        surface.blit(level_label, level_rectangle)

    def draw_upgrade_unaffordable_label(self, surface, left: int, top: int) -> None:
        cant_afford_label = LABEL_FONT.render("SAVE UP", True, LABEL_FONT_COLOR)
        cant_afford_rectangle = pygame.Rect(left + 5, top + 10, 0, 0)
        surface.blit(cant_afford_label, cant_afford_rectangle)

        price_message = f"${self.tower.get_upgrade_price()}"
        price_label = PRICE_FONT.render(price_message, True, CANT_AFFORD_FONT_COLOR)
        price_rectangle = pygame.Rect(left + 20, top + 20, 0, 0)
        surface.blit(price_label, price_rectangle)

    def get_collision_rect(self):
        return self.rect

    def button_functionality(self):
        cost = self.tower.upgrade()
        get_state().spend_money(cost)

    def is_button_enabled(self) -> bool:
        return self.tower.is_upgradeable() and self.tower.get_upgrade_price() <= get_state().get_current_money()

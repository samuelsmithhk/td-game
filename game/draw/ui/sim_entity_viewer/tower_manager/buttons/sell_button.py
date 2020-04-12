import pygame

from game.draw.ui.plopped.plopped_master import delete_plop
from game.draw.ui.sim_entity_viewer.tower_manager.buttons.button import TowerManagerButton
from game.state import get_state

pygame.font.init()

LABEL_FONT = pygame.font.SysFont('Verdana', 15)
VALUE_FONT = pygame.font.SysFont('Verdana', 20)

LABEL_FONT_COLOR = pygame.Color(0, 0, 0)
VALUE_FONT_COLOR = pygame.Color(10, 150, 20)

BORDER_COLOR = pygame.Color(0, 0, 0)
BACKGROUND_COLOR = pygame.Color(250, 220, 200)
BACKGROUND_COLOR_HOVER = pygame.Color(225, 200, 180)


class SellButton(TowerManagerButton):

    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)

    def get_collision_rect(self):
        return self.rect

    def button_functionality(self) -> None:
        sell_value = self.tower.get_sell_value()
        plop_id = self.tower.get_plop_id()
        delete_plop(plop_id)
        get_state().credit_money(sell_value)

    def is_button_enabled(self) -> bool:
        return True

    def draw(self, surface, left: int, top: int) -> None:
        self.draw_border(surface, left, top)
        self.draw_background(surface, left, top)
        self.draw_label(surface, left, top)

    def draw_border(self, surface, left: int, top: int) -> None:
        border_rectangle = pygame.Rect(left, top, 60, 40)
        pygame.draw.rect(surface, BORDER_COLOR, border_rectangle)
        self.rect = border_rectangle

    def draw_background(self, surface, left: int, top: int) -> None:
        background_rectangle = pygame.Rect(left + 1, top + 1, 58, 38)
        color_to_draw = BACKGROUND_COLOR_HOVER if get_state().get_hover(self) else BACKGROUND_COLOR
        pygame.draw.rect(surface, color_to_draw, background_rectangle)

    def draw_label(self, surface, left: int, top: int) -> None:
        sell_label = LABEL_FONT.render("SELL", True, LABEL_FONT_COLOR)
        sell_rectangle = pygame.Rect(left + 17, top + 10, 0, 0)
        surface.blit(sell_label, sell_rectangle)

        value_message = f"${self.tower.get_sell_value()}"
        value_label = VALUE_FONT.render(value_message, True, VALUE_FONT_COLOR)
        value_rectangle = pygame.Rect(left + 20, top + 20, 0, 0)
        surface.blit(value_label, value_rectangle)

import pygame

from game.draw.ui.sim_entity_viewer.tower_manager.buttons.button import (
    TowerManagerButton,
)
from game.state import get_state

pygame.font.init()

X_FONT = pygame.font.SysFont("freesanbold", 60)
X_FONT_COLOR = pygame.Color(255, 255, 255)

BORDER_COLOR = pygame.Color(255, 255, 255)
BACKGROUND_COLOR = pygame.Color(255, 100, 100)
BACKGROUND_COLOR_HOVER = pygame.Color(255, 50, 50)


class CloseButton(TowerManagerButton):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)

    def get_collision_rect(self):
        return self.rect

    def button_functionality(self) -> None:
        get_state().set_selected_ploppable(None)

    def is_button_enabled(self) -> bool:
        return True

    def draw(self, surface, left: int, top: int) -> None:
        self.draw_border(surface, left, top)
        self.draw_background(surface, left, top)
        self.draw_x(surface, left, top)

    def draw_border(self, surface, left: int, top: int) -> None:
        border_rectangle = pygame.Rect(left, top, 60, 40)
        pygame.draw.rect(surface, BORDER_COLOR, border_rectangle)
        self.rect = border_rectangle

    def draw_background(self, surface, left: int, top: int) -> None:
        background_rectangle = pygame.Rect(left + 1, top + 1, 58, 38)
        color_to_draw = (
            BACKGROUND_COLOR_HOVER if get_state().get_hover(self) else BACKGROUND_COLOR
        )
        pygame.draw.rect(surface, color_to_draw, background_rectangle)

    @staticmethod
    def draw_x(surface, left: int, top: int) -> None:
        x_label = X_FONT.render("X", True, X_FONT_COLOR)
        x_rectangle = pygame.Rect(left + 15, top + 3, 0, 0)
        surface.blit(x_label, x_rectangle)

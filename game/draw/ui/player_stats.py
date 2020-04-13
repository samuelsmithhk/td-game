import pygame

from game.draw.ui.ui_element import UIElement
from game.draw.ui.util import load_sprite
from game.state import get_state

BORDER_COLOR = pygame.Color(0, 0, 0)
BACKGROUND_COLOR = pygame.Color(185, 185, 185)

pygame.font.init()

LABEL_FONT = pygame.font.SysFont("freesanbold", 25)
LABEL_FONT_COLOR = pygame.Color(0, 0, 0)


class PlayerStats(UIElement):
    def __init__(self):
        super().__init__()
        self.coins_sprite = load_sprite("coins")
        self.lives_sprite = load_sprite("lives")

    def draw(self, surface, left: int, top: int) -> None:
        self.draw_border(surface, left, top)
        self.draw_background(surface, left, top)

        self.draw_cash(surface, left, top)
        self.draw_lives(surface, left, top)

    @staticmethod
    def draw_border(surface, left: int, top: int) -> None:
        border_rectangle = pygame.Rect(left, top, 200, 50)
        pygame.draw.rect(surface, BORDER_COLOR, border_rectangle)

    @staticmethod
    def draw_background(surface, left: int, top: int) -> None:
        background_rectangle = pygame.Rect(left + 1, top + 1, 198, 48)
        pygame.draw.rect(surface, BACKGROUND_COLOR, background_rectangle)

    def draw_cash(self, surface, left: int, top: int) -> None:
        coins_rect = pygame.Rect(left + 10, top + 15, 0, 0)
        surface.blit(self.coins_sprite, coins_rect)

        cash_text = f"${get_state().get_current_money()}"
        cash_label = LABEL_FONT.render(cash_text, True, LABEL_FONT_COLOR)
        cash_rect = pygame.Rect(left + 45, top + 18, 0, 0)
        surface.blit(cash_label, cash_rect)

    def draw_lives(self, surface, left: int, top: int) -> None:
        lives_rect = pygame.Rect(left + 100, top + 15, 0, 0)
        surface.blit(self.lives_sprite, lives_rect)

        lives_label = LABEL_FONT.render(
            str(get_state().get_lives()), True, LABEL_FONT_COLOR
        )
        lives_label_rect = pygame.Rect(left + 135, top + 18, 0, 0)
        surface.blit(lives_label, lives_label_rect)

    def update_mouse(self, mouse_position, mouse_clicked) -> None:
        pass

import pygame

from game.draw.ui.game_map.tile.tile import Tile
from game.state import get_state

PATH_COLOR = pygame.Color(240, 240, 10)
PATH_COLOR_HOVER = pygame.Color(150, 0, 0)


class PathTile(Tile):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)

    def draw(self, surface, left: int, top: int) -> None:
        width = 40
        height = 40

        rectangle = pygame.Rect(left, top, width, height)
        self.rect = rectangle

        color_to_draw = PATH_COLOR_HOVER if get_state().get_hover(self) else PATH_COLOR

        pygame.draw.rect(surface, color_to_draw, rectangle)

    def update_mouse(self, mouse_position, mouse_clicked) -> None:
        state = get_state()

        if self.rect.colliderect(state.get_cursor_rect()):
            if state.get_selected_tower_definition():
                state.set_hover(self, True)

            state.set_cursor_in_buildable_space(False)
        else:
            state.set_hover(self, False)

    def update_mouse_clicked(self, moue_position, mouse_clicked) -> None:
        pass

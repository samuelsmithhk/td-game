import pygame

from game.draw.ui.game_map.tile.tile import Tile
from game.draw.ui.plopped.plopped_master import try_to_plop
from game.state import get_state

LAND_COLOR = pygame.Color(140, 200, 0)
LAND_COLOR_HOVER = pygame.Color(200, 240, 0)


class LandTile(Tile):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)

    def draw(self, surface, left: int, top: int) -> None:
        width = 40
        height = 40

        rectangle = pygame.Rect(left, top, width, height)
        self.rect = rectangle

        color_to_draw = LAND_COLOR_HOVER if get_state().get_hover(self) else LAND_COLOR

        pygame.draw.rect(surface, color_to_draw, rectangle)

    def update_mouse(self, mouse_position, mouse_clicked) -> None:
        state = get_state()

        if self.rect.colliderect(state.get_cursor_rect()):
            if state.get_selected_tower_definition():
                state.set_hover(self, True)
        else:
            state.set_hover(self, False)

    def update_mouse_clicked(self, mouse_position, mouse_clicked) -> None:
        state = get_state()
        if get_state().is_cursor_in_buildable_space():
            if self.rect.colliderect(get_state().get_cursor_rect()):
                if mouse_clicked:
                    selected_tower_definition = state.get_selected_tower_definition()
                    price = (
                        selected_tower_definition.level_one_price
                        if selected_tower_definition
                        else 0
                    )

                    plop_success = try_to_plop(mouse_position)

                    if plop_success and price > 0:
                        state.spend_money(price)

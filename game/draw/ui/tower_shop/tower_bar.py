from typing import List

from game.draw.ui.tower_shop.tower_button import TowerButton
from game.draw.ui.ui_element import UIElement
from tower.util import get_tower_names_ui_order, get_tower_definition


class TowerBar(UIElement):
    def __init__(self):
        super().__init__()
        self.tower_buttons = self.load_tower_buttons()

    def draw(self, surface, left: int, top: int) -> None:
        left_offset = 0

        for tower_button in self.tower_buttons:
            tower_button.draw(surface, left + left_offset, top)
            left_offset += 150

    def update_mouse(self, mouse_position, mouse_clicked) -> None:
        for tower_button in self.tower_buttons:
            tower_button.update_mouse(mouse_position, mouse_clicked)

    @staticmethod
    def load_tower_buttons() -> List[TowerButton]:
        tower_names = get_tower_names_ui_order()
        return [
            TowerButton(get_tower_definition(tower_name)) for tower_name in tower_names
        ]

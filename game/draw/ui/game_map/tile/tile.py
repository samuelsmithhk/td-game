from abc import ABC, abstractmethod

from game.draw.ui.ui_element import UIElement


class Tile(UIElement, ABC):

    @abstractmethod
    def update_mouse(self, mouse_position, mouse_clicked) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_mouse_clicked(self, moue_position, mouse_clicked) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw(self, surface, left: int, top: int) -> None:
        raise NotImplementedError

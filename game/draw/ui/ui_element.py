from abc import ABC, abstractmethod


class UIElement(ABC):
    def __init__(self):
        self.enabled = True
        self.clicked = False

    def set_enabled(self, enabled: bool) -> None:
        self.enabled = enabled

    @abstractmethod
    def update_mouse(self, mouse_position, mouse_clicked) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw(self, surface, left: int, top: int) -> None:
        raise NotImplementedError

from abc import ABC, abstractmethod

from game.draw.ui.ui_element import UIElement
from game.state import get_state
from tower.ploppable import Ploppable


class TowerManagerButton(UIElement, ABC):

    def __init__(self):
        super().__init__()
        self.tower = None
        self.clock_tick = 0
        self.last_interacted_clock_tick = 0

    @abstractmethod
    def get_collision_rect(self):
        raise NotImplementedError

    @abstractmethod
    def button_functionality(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_button_enabled(self) -> bool:
        raise NotImplementedError

    def set_tower(self, tower: Ploppable) -> None:
        self.tower = tower

    def add_clock_tick(self, clock_tick: int) -> None:
        self.clock_tick += clock_tick

    def update_mouse(self, mouse_position, mouse_clicked) -> None:
        state = get_state()
        if self.get_collision_rect().collidepoint(mouse_position):
            if self.is_button_enabled():
                state.set_hover(self, True)

                if mouse_clicked:
                    if self.clock_tick - self.last_interacted_clock_tick > 250:
                        self.button_functionality()
                        self.last_interacted_clock_tick = self.clock_tick
            else:
                state.set_hover(self, False)
        else:
            state.set_hover(self, False)
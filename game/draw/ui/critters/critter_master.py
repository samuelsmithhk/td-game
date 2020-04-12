from typing import Dict

from game.draw.ui.critters.critter_element import CritterElement
from game.draw.ui.ui_element import UIElement
from game.state import get_state


class CritterMaster(UIElement):

    def __init__(self):
        super().__init__()
        self.critter_elements: Dict[str, CritterElement] = {}
        self.current_clock_tick = 0

    def draw(self, surface, left: int, top: int) -> None:
        self.check_current_critters()

        for critter_element in self.critter_elements.values():
            critter_element.set_clock_tick(self.current_clock_tick)
            critter_element.draw(surface, left, top)

    def check_current_critters(self):
        state = get_state()
        expected_critter_ids = set(self.critter_elements.keys())
        actual_critter_ids = set(state.get_critter_ids())

        new_critter_ids = actual_critter_ids - expected_critter_ids
        dead_critter_ids = expected_critter_ids - actual_critter_ids

        for new_critter_id in new_critter_ids:
            self.critter_elements[new_critter_id] = CritterElement(state.get_critter(new_critter_id))

        for dead_critter_id in dead_critter_ids:
            del self.critter_elements[dead_critter_id]

    def update_mouse(self, mouse_position, mouse_clicked) -> None:
        for critter_element in self.critter_elements.values():
            critter_element.update_mouse(mouse_position, mouse_clicked)

    def set_clock_tick(self, clock_tick: int) -> None:
        self.current_clock_tick = clock_tick
import logging
from math import sqrt

from typing import Dict, Tuple

import pygame

from game.draw.ui.plopped.plopped import Plopped
from game.draw.ui.ui_element import UIElement
from game.state import get_state
from tower.ploppable import Ploppable

RAY_COLOR = pygame.Color(0, 0, 0)


def get_plopped_master():
    return _plopped_master


def try_to_plop(mouse_position: Tuple[int, int]) -> bool:
    logging.info("Trying to plop")
    state = get_state()

    if state.is_cursor_in_buildable_space():
        logging.debug("Cursor is in buildable space")
        tower_definition = state.get_selected_tower_definition()

        if tower_definition:
            logging.debug(
                f"Tower definition {tower_definition.tower_name} has been selected"
            )
            ploppable = Ploppable(tower_definition)
            plopped = Plopped(ploppable, mouse_position[0], mouse_position[1])
            _plopped_master.add_plopped(plopped)
            logging.info(f"Successfully plopped - {plopped.get_plop_id()}")
            state.set_selected_tower_definition(None)
            return True

        return False


def delete_plop(plop_id: str) -> None:
    logging.info(f"Deleting plop - {plop_id}")
    state = get_state()

    if state.get_selected_ploppable().get_plop_id() == plop_id:
        state.set_selected_ploppable(None)

    plopped_master = get_plopped_master()
    plopped_master.remove_plopped(plop_id)
    logging.info(f"{plop_id} removed")


class _PloppedMaster(UIElement):
    def __init__(self):
        super().__init__()
        self.plops: Dict[str, Plopped] = {}

    def add_plopped(self, plopped: Plopped) -> None:
        self.plops[plopped.get_plop_id()] = plopped

    def remove_plopped(self, plop_id: str) -> None:
        if plop_id in self.plops:
            del self.plops[plop_id]

    def draw(self, surface, left: int, top: int) -> None:
        self.calculate_rays(surface, left, top)

        for plop_id, plop in self.plops.items():
            plop.draw(surface, 0, 0)

        get_state().set_plopped_towers(self.plops)

    def calculate_rays(self, surface, left, top):
        critters = get_state().get_critters()

        for tower in self.plops.values():
            if tower.is_reloaded():
                tower_range = tower.ploppable.get_tower_stats()["range"]
                tower_can_see_invisible = (
                    tower.ploppable.get_tower_stats()["special"] == "sees invisible"
                )
                tower_slows_enemy = (
                    tower.ploppable.get_tower_stats()["special"] == "slows enemy"
                )

                tower_rectangle = tower.rect
                tower_x = int(tower_rectangle.left + (tower_rectangle.width / 2))
                tower_y = int(tower_rectangle.top + (tower_rectangle.height / 2))
                tower_pos = tower_x, tower_y

                for critter in critters:
                    visibility_test = (
                        not critter.is_invisible()
                    ) or tower_can_see_invisible
                    slow_test = not (tower_slows_enemy and critter.is_slow())

                    if visibility_test and slow_test:
                        critter_x = critter.current_x + left + 5
                        critter_y = critter.current_y + top + 5
                        critter_pos = critter_x, critter_y

                        line_length = self.calculate_line_length(tower_pos, critter_pos)

                        if line_length <= tower_range:
                            pygame.draw.aaline(
                                surface, RAY_COLOR, tower_pos, critter_pos, 5
                            )
                            damage = tower.shoot(critter)
                            critter.hit(damage)

                            if tower_slows_enemy:
                                critter.maybe_slow()
                            break

    @staticmethod
    def calculate_line_length(tower_pos, critter_pos):
        tower_x, tower_y = tower_pos
        critter_x, critter_y = critter_pos

        diff_x = tower_x - critter_x
        diff_y = tower_y - critter_y

        return sqrt(abs((diff_x * diff_x) + (diff_y * diff_y)))

    def update_mouse(self, mouse_position, mouse_clicked) -> None:
        for plop_id, plop in self.plops.items():
            plop.update_mouse(mouse_position, mouse_clicked)


_plopped_master = _PloppedMaster()

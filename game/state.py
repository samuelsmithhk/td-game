import logging
from typing import Optional, List

import pygame

from game.draw.ui.ui_element import UIElement
from tower.ploppable import Ploppable
from tower.tower_definitions import TowerDefinition


def get_state():
    return _state


class _State:
    def __init__(self):
        self._selected_tower_definition: Optional[TowerDefinition] = None
        self._current_hover: Optional[UIElement] = None
        self._in_playable_space = False
        self._in_buildable_space = False
        self._cursor_rect = pygame.Rect(0, 0, 0, 0)
        self._selected_ploppable: Optional[Ploppable] = None
        self._critters = {}
        self._critters_to_despawn: List[str] = []
        self._plopped_towers = {}
        self._is_paused = False
        self._current_money = 100
        self._selected_critter = None
        self._round_finished = True
        self._round_number = 0
        self._lives = 50

    def set_selected_tower_definition(
        self, tower_definition: Optional[TowerDefinition]
    ) -> None:
        self._selected_tower_definition = tower_definition

        if tower_definition:
            self.set_selected_critter(None)
            self.set_selected_ploppable(None)

    def get_selected_tower_definition(self) -> Optional[TowerDefinition]:
        return self._selected_tower_definition

    def set_hover(self, object_hovering: UIElement, is_hovering: bool) -> None:
        if is_hovering:
            self._current_hover = object_hovering
        elif self._current_hover == object_hovering:
            self._current_hover = None

    def get_any_hover(self) -> bool:
        return self._current_hover is not None

    def get_hover(self, object_hovering: UIElement) -> bool:
        return self._current_hover == object_hovering

    def set_cursor_in_playable_space(self, in_playable_space: bool) -> None:
        self._in_playable_space = in_playable_space

    def is_cursor_in_playable_space(self) -> bool:
        return self._in_playable_space

    def set_cursor_in_buildable_space(self, in_buildable_space: bool) -> None:
        self._in_buildable_space = in_buildable_space

    def is_cursor_in_buildable_space(self) -> bool:
        return self._in_buildable_space

    def set_cursor_rect(self, cursor_rect) -> None:
        self._cursor_rect = cursor_rect

    def get_cursor_rect(self):
        return self._cursor_rect

    def set_selected_ploppable(self, ploppable: Optional[Ploppable]) -> None:
        self._selected_ploppable = ploppable

        if ploppable:
            self.set_selected_critter(None)
            self.set_selected_tower_definition(None)

    def get_selected_ploppable(self) -> Optional[Ploppable]:
        return self._selected_ploppable

    def add_critter(self, critter) -> None:
        critter_id = critter.critter_id
        self._critters[critter_id] = critter

    def get_critters(self):
        return list(self._critters.values())

    def get_critter_ids(self) -> List[str]:
        return list(self._critters.keys())

    def get_critter(self, critter_id: str):
        return self._critters[critter_id]

    def mark_critter_for_despawn(self, critter) -> None:
        logging.info(f"{critter.critter_id} marked for despawn")
        self._critters_to_despawn.append(critter.critter_id)

    def despawn_marked_critters(self) -> None:

        if len(self._critters_to_despawn) > 0:
            logging.info(f"despawning {len(self._critters_to_despawn)} critters")

        selected_critter = self.get_selected_critter()

        if selected_critter:
            if selected_critter.critter_id in self._critters_to_despawn:
                self.set_selected_critter(None)

        for critter_to_despawn_id in self._critters_to_despawn:
            if critter_to_despawn_id in self._critters:
                del self._critters[critter_to_despawn_id]

        self._critters_to_despawn = []

    def get_all_plopped_towers(self):
        return list(self._plopped_towers.values())

    def get_plopped_tower(self, tower_plop_id):
        return self._plopped_towers.get(tower_plop_id)

    def set_plopped_towers(self, plopped_towers):
        self._plopped_towers = plopped_towers

    def set_paused(self, is_paused: bool) -> None:
        if is_paused:
            logging.info("Pausing simulation")
        else:
            logging.info("Resuming simulation")
        self._is_paused = is_paused

    def is_paused(self) -> bool:
        return self._is_paused

    def set_round_number(self, round_number: int) -> None:
        self._round_number = round_number

    def get_round_number(self) -> int:
        return self._round_number

    def set_round_finished(self, round_finished: bool) -> None:
        self._round_finished = round_finished

        if round_finished:
            for plopped in self._plopped_towers.values():
                plopped.ploppable.increment_rounds()

    def is_round_finished(self) -> bool:
        return self._round_finished

    def get_current_money(self) -> int:
        return self._current_money

    def spend_money(self, amount: int) -> int:
        self._current_money -= amount
        logging.info(f"${amount} spent, current balance = ${self._current_money}")
        return self._current_money

    def credit_money(self, amount: int) -> int:
        self._current_money += amount
        logging.info(f"${amount} credited, current balance = ${self._current_money}")
        return self._current_money

    def get_selected_critter(self):
        return self._selected_critter

    def set_selected_critter(self, critter):
        self._selected_critter = critter

        if critter:
            self.set_selected_ploppable(None)
            self.set_selected_tower_definition(None)

    def get_lives(self) -> int:
        return self._lives

    def subtract_life(self) -> None:
        self._lives -= 1

        if self._lives < 0:
            exit()


_state = _State()

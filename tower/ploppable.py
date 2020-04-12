import logging
import uuid
from typing import Any, Dict

from tower.tower_definitions import TowerDefinition


class Ploppable:

    def __init__(self, tower_definition: TowerDefinition, current_level: int = 1):
        self._plop_id = str(uuid.uuid4())
        self._tower_definition = tower_definition
        self._current_level = current_level
        self._kills = 0
        self._rounds = 0
        self._shots = 0
        self._damage = 0
        self._amount_spent = tower_definition.level_one_price

    def get_plop_id(self) -> str:
        return self._plop_id

    def get_tower_definition(self) -> TowerDefinition:
        return self._tower_definition

    def get_current_level(self) -> int:
        return self._current_level

    def is_upgradeable(self):
        return self._current_level < 5

    def get_upgrade_price(self) -> int:
        return self._tower_definition.get_upgrade_price(self._current_level)

    def increment_rounds(self) -> None:
        self._rounds += 1

    def upgrade(self):
        upgrade_price = self.get_upgrade_price()
        self._amount_spent += upgrade_price

        if self._current_level < 5:
            self._current_level += 1
            logging.info(f"{self.get_plop_id()} upgraded to level {self.get_current_level()}")

        return upgrade_price

    def get_tower_stats(self) -> Dict[str, Any]:
        return self.get_stats_for_level(self._current_level)

    def shoot(self, critter):
        self._shots += 1
        self._damage += self.get_tower_stats()['damage']

        if critter.health <= self.get_tower_stats()['damage']:
            self._kills += 1

    def get_sell_value(self):
        return int(self._amount_spent / 2)

    def get_credits(self) -> Dict[str, Any]:
        return {
            'rounds': self._rounds,
            'shots': self._shots,
            'damage': self._damage,
            'kills': self._kills
        }

    def get_stats_for_level(self, level: int) -> Dict[str, Any]:
        level_definition = self._tower_definition.get_level_definition(level)

        stats = {
            'damage': level_definition.damage_per_shot,
            'reload_time': level_definition.reload_time_milliseconds,
            'range': level_definition.range_radius,
            'special': 'N/A'
        }

        if level_definition.sees_invisible:
            stats['special'] = 'sees invisible'

        if level_definition.slows_enemy:
            stats['special'] = 'slows enemy'

        return stats

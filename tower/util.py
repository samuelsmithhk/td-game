from typing import List

from tower.tower_definitions import basic_tower, machine_gun_tower, sniper_tower, glue_tower, TowerDefinition

TOWER_DEFINITION_FACTORY = {
    'basic': basic_tower,
    'machine_gun': machine_gun_tower,
    'sniper': sniper_tower,
    'glue': glue_tower
}


def get_tower_names_ui_order() -> List[str]:
    return ['basic', 'machine_gun', 'sniper', 'glue']


def get_tower_definition(tower_name: str) -> TowerDefinition:
    return TOWER_DEFINITION_FACTORY[tower_name]

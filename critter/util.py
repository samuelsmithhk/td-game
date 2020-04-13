from functools import partial
from typing import List

from critter.critter import Critter
from critter.critter_base import Base
from critter.critter_base_boss import BaseBoss
from critter.critter_invisible import Invisible
from critter.critter_invisible_boss import InvisibleBoss
from critter.critter_resistant import Resistant
from critter.critter_resistant_boss import ResistantBoss
from critter.critter_speeder import Speeder
from critter.critter_speeder_boss import SpeederBoss

CRITTER_FACTORY = {
    "base": Base,
    "base-boss": BaseBoss,
    "speeder": Speeder,
    "speeder-boss": SpeederBoss,
    "invisible": Invisible,
    "invisible-boss": InvisibleBoss,
    "resistant": Resistant,
    "resistant-boss": ResistantBoss,
}


def get_critter_type_names() -> List[str]:
    return list(CRITTER_FACTORY.keys())


def get_critter(critter_type: str, critter_health: int, critter_speed: int) -> partial:
    critter_class = CRITTER_FACTORY[critter_type]

    return partial(critter_class, health=critter_health, speed=critter_speed)

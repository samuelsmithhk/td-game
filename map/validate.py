import logging

from typing import Any, Callable, Dict, List, NamedTuple, Optional

from critter.util import get_critter_type_names


class Validator(NamedTuple):
    name: str
    func: Callable[[Dict[str, Any]], Optional[str]]


def run_map_definition_validators(map_definition: Dict[str, Any]) -> None:
    for validator in VALIDATORS:
        logging.debug(f"Running validator {validator.name}")
        validation_error = validator.func(map_definition)

        if validation_error is not None:
            raise ValueError(validation_error)


########################
# Validation Functions #
########################


def root_schema_validator(map_definition: Dict[str, Any]) -> Optional[str]:
    root_keys = ["board", "rounds"]

    for root_key in root_keys:
        if root_key not in map_definition:
            return f"Missing key in root of map schema - {root_key}"


def board_size_validator(map_definition: Dict[str, Any]) -> Optional[str]:
    board_size = map_definition["board"].get("size")

    if board_size is None:
        return "board config missing size key"

    board_width = board_size.get("width")
    board_height = board_size.get("height")

    if board_width is None:
        return "board size config is missing width key"

    if board_height is None:
        return "board size config is missing height key"

    if 0 > board_width >= 40:
        return "board width must be greater than 0 and less than 41"

    if 0 > board_height >= 10:
        return "board height must be greater than 0 and less than 11"


def board_spawn_validator(map_definition: Dict[str, Any]) -> Optional[str]:
    board_spawn = map_definition["board"].get("spawn")

    if board_spawn is None:
        return "board config is missing spawn key"

    spawn_x = board_spawn.get("x")
    spawn_y = board_spawn.get("y")

    if spawn_x is None:
        return "board spawn config missing x key"

    if spawn_y is None:
        return "board spawn config missing y key"

    if 0 >= spawn_x >= map_definition["board"]["size"]["width"]:
        return "board spawn x must be between 0 and width of board"

    if 0 >= spawn_y >= map_definition["board"]["size"]["height"]:
        return "board spawn y must be between 0 and height of board"


def board_goal_validator(map_definition: Dict[str, Any]) -> Optional[str]:
    board_goal = map_definition["board"].get("goal")

    if board_goal is None:
        return "board config is missing goal key"

    goal_x = board_goal.get("x")
    goal_y = board_goal.get("y")

    if goal_x is None:
        return "board goal config missing x key"

    if goal_y is None:
        return "board goal config missing y key"

    if 0 >= goal_x >= map_definition["board"]["size"]["width"]:
        return "board goal x must be between 0 and width of board"

    if 0 >= goal_y >= map_definition["board"]["size"]["height"]:
        return "board goal y must be between 0 and height of board"

    spawn_x = map_definition["board"]["spawn"]["x"]
    spawn_y = map_definition["board"]["spawn"]["y"]

    if spawn_x == goal_x and spawn_y == goal_y:
        return "board spawn and goal cannot be in same location"


def board_path_validator(map_definition: Dict[str, Any]) -> Optional[str]:
    board_path = map_definition["board"].get("path")

    if board_path is None:
        return "board config is missing path key"

    if not isinstance(board_path, list):
        return "board path config must be a list"

    defined_blocks = {}

    spawn_x = map_definition["board"]["spawn"]["x"]
    spawn_y = map_definition["board"]["spawn"]["y"]
    spawn_in_path = False

    goal_x = map_definition["board"]["goal"]["x"]
    goal_y = map_definition["board"]["goal"]["y"]
    goal_in_path = False

    for block_index, block in enumerate(board_path):
        block_x = block.get("x")
        block_y = block.get("y")

        if block_x is None:
            return f"board path index {block_index} config missing x key"

        if block_y is None:
            return f"board path index {block_index} config missing y key"

        duplicate_key = f"{block_x}~{block_y}"
        duplicate_index = defined_blocks.get(duplicate_key, -1)

        if duplicate_index > -1:
            return (
                f"board path index {block_index} is duplicated with {duplicate_index}"
            )

        defined_blocks[duplicate_key] = block_index

        if not spawn_in_path:
            if spawn_x == block_x and spawn_y == block_y:
                spawn_in_path = True

        if not goal_in_path:
            if goal_x == block_x and goal_y == block_y:
                goal_in_path = True

    if not spawn_in_path:
        return "spawn is not in path"

    if not goal_in_path:
        return "goal is not in path"

    # TODO: Build map and ensure there is a valid path from spawn to goal


def rounds_critters_validator(map_definition: Dict[str, Any]) -> Optional[str]:
    rounds = map_definition["rounds"]

    if not isinstance(rounds, list):
        return "rounds config must be a list"

    valid_critter_types = get_critter_type_names()

    for round_index, round_definition in enumerate(rounds):
        critters = round_definition.get("critters")

        if critters is None:
            return f"round {round_index} config is missing critter key"

        if not isinstance(critters, list):
            return f"round {round_index} critter config must be a list"

        for critter_index, critter in enumerate(critters):
            if not isinstance(critter, dict):
                return f"round {round_index} critter {critter_index} must be a dict"

            critter_type = critter.get("type")

            if critter_type is None:
                return f"round {round_index} critter {critter_index} config is missing key type"

            if critter_type not in valid_critter_types:
                return f"round {round_index} critter {critter_index} type [{critter_type}] is invalid - must be one of {valid_critter_types}"

            critter_health = critter.get("health")

            if critter_health is None:
                return f"round {round_index} critter {critter_index} config is missing health key"

            if not isinstance(critter_health, int):
                return f"round {round_index} critter {critter_index} health must be int"

            if critter_health <= 0:
                return f"round {round_index} critter {critter_index} health must be greater than 0"

            critter_speed = critter.get("speed")

            if critter_speed is None:
                return f"round {round_index} critter {critter_index} config is missing speed key"

            if not isinstance(critter_speed, int):
                return f"round {round_index} critter {critter_index} speed must be int"

            if critter_speed <= 0:
                return f"round {round_index} critter {critter_index} speed must be greater than 0"

            critter_count = critter.get("count")

            if critter_count is None:
                return f"round {round_index} critter {critter_index} config is missing count key"

            if not isinstance(critter_count, int):
                return f"round {round_index} critter {critter_index} count must be int"

            if critter_count <= 0:
                return f"round {round_index} critter {critter_index} count must be greater than 0"


VALIDATORS: List[Validator] = [
    Validator(name="Base Schema Validation", func=root_schema_validator),
    Validator(name="Board Size Validation", func=board_size_validator),
    Validator(name="Board Spawn Validation", func=board_spawn_validator),
    Validator(name="Board Goal Validation", func=board_goal_validator),
    Validator(name="Board Path Validation", func=board_path_validator),
    Validator(name="Round Critters Validation", func=rounds_critters_validator),
]

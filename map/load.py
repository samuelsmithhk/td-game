import logging
import os

import yaml

from critter.util import get_critter
from map.map import Map, Board, Round
from typing import Any, Dict, List

from map.validate import run_map_definition_validators

DIR_NAME = os.path.dirname(os.path.realpath(__file__))


def load_game_map(map_name: str) -> Map:
    logging.info(f"Loading map {map_name}")

    map_path = get_map_path(map_name=map_name)
    logging.debug(f"Map path: {map_path}")

    map_definition = load_map_definition(map_path=map_path)
    logging.debug("Map definition file loaded, validating")

    validate_map_definition(map_definition=map_definition)
    logging.debug("Map definition file validated, parsing")

    game_map = parse_map_definition(map_definition=map_definition)

    logging.info(f"{map_name} loaded")
    return game_map


def get_map_path(map_name: str) -> str:
    return os.path.join(DIR_NAME, "..", "resources", "maps", f"{map_name}.yml")


def load_map_definition(map_path: str) -> Dict[str, Any]:
    try:
        with open(map_path) as map_file:
            map_definition = yaml.safe_load(map_file)
            return map_definition
    except OSError as e:
        logging.critical("Unable to load map, are you sure the name is right?")
        exit(1)


def validate_map_definition(map_definition: Dict[str, Any]) -> None:
    try:
        run_map_definition_validators(map_definition=map_definition)
    except ValueError as e:
        logging.critical("Map definition failed validation")
        logging.critical(e)
        exit(1)


def parse_map_definition(map_definition: Dict[str, Any]) -> Map:
    board: Board = parse_board_definition(board_definition=map_definition["board"])
    rounds: List[Round] = parse_rounds_definition(
        rounds_definition=map_definition["rounds"]
    )

    return Map(board=board, rounds=rounds)


def parse_board_definition(board_definition: Dict[str, Any]) -> Board:
    logging.debug("Parsing board definition")

    board_builder = (
        Board.BoardBuilder()
        .set_width(board_definition["size"]["width"])
        .set_height(board_definition["size"]["height"])
        .set_spawn(board_definition["spawn"]["x"], board_definition["spawn"]["y"])
        .set_goal(board_definition["goal"]["x"], board_definition["goal"]["y"])
    )

    for path_block in board_definition["path"]:
        board_builder.add_block_to_path(path_block["x"], path_block["y"])

    return board_builder.build()


def parse_rounds_definition(rounds_definition: List[Dict[str, Any]]) -> List[Round]:

    rounds: List[Round] = []
    for round_definition in rounds_definition:
        game_round = Round()
        critter_definitions = round_definition["critters"]

        for critter_definition in critter_definitions:
            critter_type = critter_definition["type"]
            critter_health = critter_definition["health"]
            critter_speed = critter_definition["speed"]
            critter_count = critter_definition["count"]

            critter = get_critter(critter_type, critter_health, critter_speed)

            game_round.add_wave(critter, critter_count)

        rounds.append(game_round)

    return rounds

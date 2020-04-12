import logging
import random
from functools import partial

from typing import List, Tuple, Optional, Dict, Set

class Board:

    def __init__(self, width: int, height: int, spawn_x: int, spawn_y: int, goal_x: int, goal_y: int,
                 path: List[Tuple[int, int]]):
        self.size = width, height
        self.spawn = spawn_x, spawn_y
        self.goal = goal_x, goal_y
        self.path = path
        self.path_tile_coordinates = self._calculate_path_tile_coordinates()
        self.tile_paths = []
        self.pixel_paths = []

        self._bake_paths()

    def get_random_pixel_path(self) -> List[Tuple[int, int]]:
        return random.choice(self.pixel_paths).copy()

    def _calculate_path_tile_coordinates(self) -> Set[str]:
        return {f"{x}~{y}" for x, y in self.path}

    def _bake_paths(self):
        logging.info("Calculating paths for critters")
        visited_keys = {}
        spawn_key = f"{self.spawn[0]}~{self.spawn[1]}"
        goal_key = f"{self.goal[0]}~{self.goal[1]}"
        path_buffer = []

        self._bake_all_tile_paths(spawn_key, goal_key, visited_keys, path_buffer)
        self._bake_all_pixel_paths()

    def _bake_all_tile_paths(self, current_key: str, goal_key: str, visited_keys: Dict[str, bool], path_buffer) -> None:
        visited_keys[current_key] = True
        path_buffer.append(current_key)

        if current_key == goal_key:
            logging.debug("Tile path calculated")
            logging.debug(path_buffer)
            self.tile_paths.append(path_buffer.copy())
        else:
            for path_key in self._get_adjacent_path_keys(current_key):
                if not visited_keys.get(path_key, False):
                    self._bake_all_tile_paths(path_key, goal_key, visited_keys, path_buffer)

        path_buffer.pop()
        visited_keys[current_key] = False

    def _bake_all_pixel_paths(self) -> None:
        logging.debug("Generating pixel paths")
        pixel_paths_per_tile_path = int(50 / len(self.tile_paths))

        pixel_paths = []
        for tile_path in self.tile_paths:
            for _ in range(0, pixel_paths_per_tile_path):
                spawn_pixel = self._get_random_pixel_in_tile(tile_path[0], spawn=True)
                pixel_path = [spawn_pixel]

                for tile_coordinates in tile_path:
                    pixel_path.append(self._get_random_pixel_in_tile(tile_coordinates))

                goal_pixel = self._get_random_pixel_in_tile(tile_path[-1], goal=True)
                pixel_path.append(goal_pixel)

                logging.debug(pixel_path)

                pixel_paths.append(pixel_path)

        self.pixel_paths = pixel_paths

    @staticmethod
    def _get_random_pixel_in_tile(tile_coordinates: str, spawn: bool = False, goal: bool = False) -> Tuple[int, int]:
        tile_x = int(tile_coordinates.split('~')[0])
        tile_y = int(tile_coordinates.split('~')[1])

        left_bound = tile_x * 40
        top_bound = tile_y * 40
        right_bound = left_bound + 30
        bottom_bound = top_bound + 30

        pixel_x = random.randint(left_bound, right_bound)
        pixel_y = random.randint(top_bound, bottom_bound)

        if spawn:
            pixel_x -= 40

        if goal:
            pixel_x += 40

        return pixel_x, pixel_y

    def _get_adjacent_path_keys(self, current_key: str) -> List[str]:
        current_x = int(current_key.split('~')[0])
        current_y = int(current_key.split('~')[1])

        left_key = f'{current_x - 1}~{current_y}'
        top_key = f'{current_x}~{current_y - 1}'
        right_key = f'{current_x + 1}~{current_y}'
        bottom_key = f'{current_x}~{current_y + 1}'

        adjacent_path_keys = []

        if left_key in self.path_tile_coordinates:
            adjacent_path_keys.append(left_key)

        if top_key in self.path_tile_coordinates:
            adjacent_path_keys.append(top_key)

        if right_key in self.path_tile_coordinates:
            adjacent_path_keys.append(right_key)

        if bottom_key in self.path_tile_coordinates:
            adjacent_path_keys.append(bottom_key)

        return adjacent_path_keys

    class BoardBuilder:

        def __init__(self):
            self.width: Optional[int] = None
            self.height: Optional[int] = None
            self.spawn_x: Optional[int] = None
            self.spawn_y: Optional[int] = None
            self.goal_x: Optional[int] = None
            self.goal_y: Optional[int] = None
            self.path: List[Tuple[int, int]] = []

        def set_width(self, width: int) -> "Board.BoardBuilder":
            self.width = width
            return self

        def set_height(self, height: int) -> "Board.BoardBuilder":
            self.height = height
            return self

        def set_spawn(self, x: int, y: int) -> "Board.BoardBuilder":
            self.spawn_x = x
            self.spawn_y = y
            return self

        def set_goal(self, x: int, y: int) -> "Board.BoardBuilder":
            self.goal_x = x
            self.goal_y = y
            return self

        def add_block_to_path(self, x: int, y: int) -> "Board.BoardBuilder":
            self.path.append((x, y))
            return self

        def build(self) -> "Board":
            return Board(width=self.width, height=self.height, spawn_x=self.spawn_x, spawn_y=self.spawn_y,
                         goal_x=self.goal_x, goal_y=self.goal_y, path=self.path)


class Round:

    def __init__(self):
        self.waves: List[Tuple[partial, int]] = []

    def add_wave(self, critter: partial, count: int):
        self.waves.append((critter, count))


class Map:

    def __init__(self, board: Board, rounds: List[Round]):
        self.board: Board = board
        self.rounds: List[Round] = rounds

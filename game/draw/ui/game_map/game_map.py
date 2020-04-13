from typing import Dict, Tuple, List

import pygame

from game.draw.ui.game_map.tile.land_tile import LandTile
from game.draw.ui.game_map.tile.path_tile import PathTile
from game.draw.ui.game_map.tile.tile import Tile
from game.draw.ui.game_map.tile.water_tile import WaterTile
from game.draw.ui.ui_element import UIElement
from game.state import get_state
from map.map import Map, Board


class GameMap(UIElement):
    def __init__(self, game_map: Map):
        super().__init__()
        self.left_offset = 0
        self.top_offset = 0
        self.tiles: Dict[str, Tile] = self.init_tiles(game_map.board)
        self.rect = pygame.Rect(0, 0, 800, 400)

    def init_tiles(self, board: Board) -> Dict[str, Tile]:
        tiles: Dict[str, Tile] = {}

        playable_boundaries = self.calculate_playable_boundaries(board)
        self.left_offset = playable_boundaries[0]
        self.top_offset = playable_boundaries[1]

        for column in range(0, 20):
            for row in range(0, 20):
                tile_coordinates = column, row

                tile_key = f"{column}~{row}"
                tile = WaterTile()

                if self.is_tile_in_playable_boundary(
                    tile_coordinates, playable_boundaries
                ):
                    if self.is_tile_on_critter_path(
                        playable_boundaries, tile_coordinates, board.path
                    ):
                        tile = PathTile()
                    else:
                        tile = LandTile()

                tiles[tile_key] = tile

        return tiles

    @staticmethod
    def is_tile_in_playable_boundary(
        tile_coordinates: Tuple[int, int],
        playable_boundaries: Tuple[int, int, int, int],
    ) -> bool:
        tile_column, tile_row = tile_coordinates
        (
            left_boundary,
            top_boundary,
            right_boundary,
            bottom_boundary,
        ) = playable_boundaries

        if (left_boundary <= tile_column <= right_boundary) and (
            top_boundary <= tile_row <= bottom_boundary
        ):
            return True

        return False

    @staticmethod
    def is_tile_on_critter_path(
        playable_boundaries: Tuple[int, int, int, int],
        tile_coordinates: Tuple[int, int],
        critter_path: List[Tuple[int, int]],
    ):
        left_boundary, top_boundary, _, _ = playable_boundaries
        tile_column, tile_row = tile_coordinates

        left_offset = tile_column - left_boundary
        top_offset = tile_row - top_boundary

        for path_block in critter_path:
            path_x, path_y = path_block
            if left_offset == path_x and top_offset == path_y:
                return True

        return False

    @staticmethod
    def calculate_playable_boundaries(board: Board) -> Tuple[int, int, int, int]:
        board_width, board_height = board.size

        dead_zone_width = 20 - board_width
        dead_zone_height = 10 - board_height

        left_boundary = dead_zone_width // 2
        top_boundary = dead_zone_height // 2
        right_boundary = left_boundary + board_width
        bottom_boundary = top_boundary + board_height

        if board_width % 2 != 0:
            right_boundary -= 1

        if board_height % 2 != 0:
            bottom_boundary -= 1

        return left_boundary, top_boundary, right_boundary, bottom_boundary

    def draw(self, surface, left: int, top: int) -> None:
        for column in range(0, 20):
            for row in range(0, 20):
                self.tiles[f"{column}~{row}"].draw(surface, column * 40, row * 40)

    def update_mouse(self, mouse_position, mouse_clicked) -> None:

        state = get_state()

        if self.rect.collidepoint(mouse_position):
            state.set_cursor_in_playable_space(True)
            state.set_cursor_in_buildable_space(True)

            for column in range(0, 20):
                for row in range(0, 20):
                    self.tiles[f"{column}~{row}"].update_mouse(
                        mouse_position, mouse_clicked
                    )

        else:
            state.set_cursor_in_playable_space(False)

    def update_mouse_clicked(self, mouse_position, mouse_clicked):
        for column in range(0, 20):
            for row in range(0, 20):
                self.tiles[f"{column}~{row}"].update_mouse_clicked(
                    mouse_position, mouse_clicked
                )

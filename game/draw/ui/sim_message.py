from typing import Tuple, Optional, List, Dict

import pygame

from game.draw.ui.ui_element import UIElement
from game.draw.ui.util import load_sprite
from game.state import get_state
from map.map import Round

pygame.font.init()

MESSAGE_FONT = pygame.font.SysFont('freesanbold', 20)
MESSAGE_FONT_COLOR = pygame.Color(0, 0, 0)
STAT_FONT = pygame.font.SysFont('freesanbold', 20)
STAT_FONT_COLOR = pygame.Color(0, 0, 0)

BORDER_COLOR = pygame.Color(0, 0, 0)
BACKGROUND_COLOR = pygame.Color(185, 185, 185)

CRITTER_DISPLAY_ORDER = [
    'base',
    'speeder',
    'invisible',
    'resistant',
    'base_boss',
    'speeder_boss',
    'invisible_boss',
    'resistant_boss'
]


class SimMessage(UIElement):

    def __init__(self, rounds: List[Round]):
        super().__init__()
        self.critter_counts = self.calculate_critter_counts(rounds)
        self.round_count = len(self.critter_counts)
        self.critter_sprites = self.load_critter_sprites()

    @staticmethod
    def calculate_critter_counts(rounds: List[Round]) -> List[Dict[str, int]]:

        round_messages = []

        for game_round in rounds:
            round_message = {}
            waves = game_round.waves

            for wave in waves:
                critter, count = wave
                critter_type = critter().type

                if critter_type not in round_message:
                    round_message[critter_type] = 0

                round_message[critter_type] += count

            round_messages.append(round_message)

        return round_messages

    @staticmethod
    def load_critter_sprites() -> Dict:
        return {
            'base': load_sprite("critter_base"),
            'base_boss': load_sprite("critter_base_boss"),
            'speeder': load_sprite('critter_speeder'),
            'speeder_boss': load_sprite('critter_speeder_boss'),
            'invisible': load_sprite("critter_invisible"),
            'invisible_boss': load_sprite('critter_invisible_boss'),
            'resistant': load_sprite('critter_resistant'),
            'resistant_boss': load_sprite('critter_resistant_boss')
        }

    def draw(self, surface, left: int, top: int) -> None:
        self.draw_border(surface, left, top)
        self.draw_background(surface, left, top)
        self.draw_round_message(surface, left, top)
        self.draw_critter_counts(surface, left, top)

    @staticmethod
    def draw_border(surface, left: int, top: int) -> None:
        border_rect = pygame.Rect(left, top, 540, 50)
        pygame.draw.rect(surface, BORDER_COLOR, border_rect)

    @staticmethod
    def draw_background(surface, left: int, top: int) -> None:
        background_rect = pygame.Rect(left + 1, top + 1, 538, 48)
        pygame.draw.rect(surface, BACKGROUND_COLOR, background_rect)

    def draw_round_message(self, surface, left: int, top: int):
        state = get_state()

        this_or_next = "NEXT" if state.is_round_finished() else "THIS"
        round_number = state.get_round_number()
        round_count = self.round_count

        message = f"{this_or_next} ROUND ({round_number} of {round_count})"
        message_label = MESSAGE_FONT.render(message, True, MESSAGE_FONT_COLOR)
        message_rect = pygame.Rect(left + 5, top + 5, 0, 0)
        surface.blit(message_label, message_rect)

    def draw_critter_counts(self, surface, left, top):
        round_number = get_state().get_round_number()
        critter_counts = self.critter_counts[round_number - 1]

        left_offset = left + 15
        for critter_type in CRITTER_DISPLAY_ORDER:
            top_offset = top + 20 if critter_type.find('boss') != -1 else top + 27

            critter_rect = pygame.Rect(left_offset, top_offset, 0, 0)
            surface.blit(self.critter_sprites[critter_type], critter_rect)

            label_left_offset = left_offset + 25 if critter_type.find('boss') != -1 else left_offset + 15

            stat_label = STAT_FONT.render(str(critter_counts.get(critter_type, 0)), True, STAT_FONT_COLOR)
            stat_rect = pygame.Rect(label_left_offset, top + 25, 0, 0)
            surface.blit(stat_label, stat_rect)

            left_offset += 60


    def update_mouse(self, mouse_position, mouse_clicked) -> None:
        pass

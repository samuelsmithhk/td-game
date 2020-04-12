import logging
import uuid
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

from game.state import get_state


class Critter(ABC):
    type = None

    def __init__(self, health: int, speed: int):
        self.critter_id = str(uuid.uuid4())
        self.starting_health = health
        self.health = health
        self.speed = speed
        self.pixel_path = None
        self.total_distance = -1
        self.distance_travelled = 0
        self.current_x = -1
        self.current_y = -1
        self.clock_tick_acc = 0
        self.slow_since = -1

    def set_pixel_path(self, pixel_path: List[Tuple[int, int]]) -> None:
        self.pixel_path = pixel_path

        first_position = self.pixel_path[0]
        self.current_x, self.current_y = first_position
        self.pixel_path.pop(0)

        self.calculate_total_distance()

    def calculate_total_distance(self):
        total_x, total_y = 0, 0
        prev_x, prev_y, = 0, 0

        for current_x, current_y in self.pixel_path:
            x_delta = abs(current_x - prev_x)
            y_delta = abs(current_y - prev_y)

            total_x += x_delta
            total_y += y_delta

            prev_x, prev_y = current_x, current_y

        self.total_distance = total_x + total_y

    def set_position(self, new_x: int, new_y: int) -> None:
        x_delta = abs(new_x - self.current_x)
        y_delta = abs(new_y - self.current_y)
        self.distance_travelled += x_delta + y_delta

        self.current_x = new_x
        self.current_y = new_y

    def get_current_milestone(self) -> Optional[Tuple[int, int]]:
        if len(self.pixel_path) > 0:
            return self.pixel_path[0]

    def milestone_reached(self) -> None:
        self.pixel_path.pop(0)

    def hit(self, damage):
        self.health -= damage

    @abstractmethod
    def is_resistant(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def can_go_invisible(self) -> bool:
        raise NotImplementedError

    def add_clock_tick(self, clock_tick: int) -> None:
        if not get_state().is_paused():
            self.clock_tick_acc += clock_tick

            if self.slow_since > -1 and self.clock_tick_acc - self.slow_since >= 1000:
                logging.debug(f"Speeding up {self.critter_id} - {self.slow_since}")
                self.slow_since = -1

    def is_invisible(self) -> bool:
        if self.can_go_invisible():
            clock_tick_acc_seconds = self.clock_tick_acc // 1000
            return clock_tick_acc_seconds % 2 != 0

        return False

    def maybe_slow(self) -> None:
        if not self.is_resistant() and self.slow_since <= -1:
            logging.debug(f"Slowing {self.critter_id} - {self.clock_tick_acc}")
            self.slow_since = self.clock_tick_acc

    def is_slow(self) -> bool:
        return self.slow_since > -1

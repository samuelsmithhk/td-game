import logging
from functools import partial

from typing import List, Tuple

from game.state import get_state
from map.map import Round, Board


class Sim:

    def __init__(self, game_board: Board, game_round: Round, round_number: int):
        logging.info(f"Starting round {round_number}")
        self.sim_time = 0
        self.board = game_board
        self.spawn_timers = self.generate_spawn_timers(game_round, round_number)
        self.reload_timers = {}
        get_state().set_paused(True)
        get_state().set_round_number(round_number)

    @staticmethod
    def generate_spawn_timers(game_round: Round, round_number: int) -> List[Tuple[int, partial]]:
        spawn_timers: List[Tuple[int, partial]] = []
        spawn_time_delta = 1500 - (round_number * 60)
        spawn_time_delta = 150 if spawn_time_delta < 150 else spawn_time_delta

        trigger_time = 1000
        for wave in game_round.waves:
            critter_type, count = wave
            for i in range(0, count):
                spawn_timers.append((trigger_time, critter_type))
                trigger_time += spawn_time_delta

        return spawn_timers

    def next_frame(self, clock_tick) -> bool:
        """
        Calculates the next frame of simulation of the game round.
        Returning True if the game round has a next frame
        Returns False if the game round has finished
        :param clock_tick:
        :return:
        """

        state = get_state()

        if not get_state().is_paused():
            state.set_round_finished(False)
            self.sim_time += clock_tick

            self.move_existing_critters(clock_tick)
            self.maybe_spawn_new_critter()
            self.maybe_kill_critters()
            self.reload_towers()

        all_critters_killed = self.all_critters_killed()

        if all_critters_killed:
            state.credit_money(state.get_round_number() * 3)
            state.set_round_finished(True)

        return not all_critters_killed

    @staticmethod
    def move_existing_critters(clock_tick):
        state = get_state()
        critters = state.get_critters()

        for critter in critters:
            current_milestone = critter.get_current_milestone()

            if current_milestone is None:
                continue

            milestone_x, milestone_y = current_milestone

            move_left = False
            move_up = False

            x_distance = milestone_x - critter.current_x
            y_distance = milestone_y - critter.current_y

            if x_distance == y_distance == 0:
                critter.milestone_reached()

                if critter.get_current_milestone() is None:
                    state.subtract_life()
                    state.mark_critter_for_despawn(critter)

                continue

            if x_distance < 0:
                x_distance *= -1
                move_left = True

            if y_distance < 0:
                y_distance *= -1
                move_up = True

            slow_multiplier = 0.3 if critter.is_slow() else 1
            pixels_to_move = clock_tick * critter.speed * 0.05 * slow_multiplier

            if pixels_to_move >= x_distance + y_distance:
                critter.set_position(milestone_x, milestone_y)
                continue

            x_y_ratio = pixels_to_move / (x_distance + y_distance)

            x_delta = int(x_distance * x_y_ratio)
            y_delta = pixels_to_move - x_delta

            if y_delta > y_distance:
                y_delta = y_distance

            if move_left:
                x_delta *= -1

            if move_up:
                y_delta *= -1

            new_x = critter.current_x + x_delta
            new_y = critter.current_y + y_delta

            critter.set_position(new_x, new_y)

        state.despawn_marked_critters()

    def maybe_spawn_new_critter(self):

        if len(self.spawn_timers) <= 0:
            return

        next_spawn_time, next_critter_partial = self.spawn_timers[0]

        if self.sim_time >= next_spawn_time:
            next_critter = next_critter_partial()
            logging.debug(f"Spawning new critter: {next_critter.critter_id}")
            next_critter.set_pixel_path(self.board.get_random_pixel_path())
            get_state().add_critter(next_critter)
            self.spawn_timers.pop(0)

    @staticmethod
    def maybe_kill_critters():
        state = get_state()
        critters = state.get_critters()

        for critter in critters:
            if critter.health <= 0:
                state.mark_critter_for_despawn(critter)
                state.credit_money(int(critter.starting_health * 0.01))

    def reload_towers(self):
        state = get_state()
        self.create_new_reload_timers()

        mark_reloaded = []
        for tower_id, reload_time in self.reload_timers.items():
            if self.sim_time >= reload_time:
                plopped_tower = state.get_plopped_tower(tower_id)

                if plopped_tower:
                    plopped_tower.reload()

                mark_reloaded.append(tower_id)

        for tower_id in mark_reloaded:
            if tower_id in self.reload_timers:
                del self.reload_timers[tower_id]

    def create_new_reload_timers(self):
        state = get_state()

        for tower in state.get_all_plopped_towers():
            if not tower.is_reloaded() and tower.get_plop_id() not in self.reload_timers:
                reload_time = tower.ploppable.get_tower_stats()['reload_time']
                self.reload_timers[tower.get_plop_id()] = self.sim_time + reload_time

    def all_critters_killed(self) -> bool:
        state = get_state()

        alive_critters = len(state.get_critters())
        critters_left_to_spawn = len(self.spawn_timers)

        return alive_critters <= 0 and critters_left_to_spawn <= 0

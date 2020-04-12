import argparse
import logging

from game.game import start_game
from map.load import load_game_map
from map.map import Map


def main(args: argparse.Namespace) -> None:
    game_map: Map = load_game_map(args.map)
    start_game(game_map)


def load_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument('--map', '-m', help='Map name to load', type=str, default='1', choices=['1'])
    ap.add_argument('--difficulty', '-d', help='Difficulty mode, 1=easy, 2=medium, 3=hard', type=int, default=1,
                    choices=[1, 2, 3])
    ap.add_argument('--log_level', '-l', default='info', choices=['debug', 'info', 'warning', 'error', 'critical'])

    args = ap.parse_args()
    return args


def configure_logging(args: argparse.Namespace) -> None:
    log_levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    logger = logging.getLogger()
    logger.setLevel(log_levels[args.log_level])

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_levels[args.log_level])

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)


if __name__ == '__main__':
    _args = load_args()
    configure_logging(_args)
    main(_args)

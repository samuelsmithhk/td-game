import pygame

from game.draw.ui.critters.critter_master import CritterMaster
from game.draw.ui.cursor import Cursor
from game.draw.ui.game_map.game_map import GameMap
from game.draw.ui.player_stats import PlayerStats
from game.draw.ui.plopped.plopped_master import get_plopped_master
from game.draw.ui.sim_entity_viewer.sim_entity_viewer import SimEntityViewer
from game.draw.ui.sim_message import SimMessage
from game.draw.ui.sim_toggle import SimToggle
from game.draw.ui.tower_description import TowerDescription
from game.draw.ui.tower_shop.tower_bar import TowerBar
from game.draw.ui.util import load_sprite
from game.sim import Sim
from map.map import Map


CLOCK = pygame.time.Clock()


def start_game(game_map: Map) -> None:
    game_screen = init_pygame()

    cursor = Cursor()
    game_map_ui = GameMap(game_map)
    sim_toggle = SimToggle()
    sim_message = SimMessage(game_map.rounds)
    player_stats = PlayerStats()
    plopped_master = get_plopped_master()
    tower_bar = TowerBar()
    tower_description = TowerDescription()
    sim_entity_viewer = SimEntityViewer()
    critter_master = CritterMaster()

    round_number = 0
    clock_tick = update_fps()
    sim = Sim(game_map.board, game_map.rounds[round_number], 1)

    game_finished = False
    while not game_finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        mouse_position = pygame.mouse.get_pos()
        mouse_clicked, _, _ = pygame.mouse.get_pressed()

        game_map_ui.update_mouse(mouse_position, mouse_clicked)
        game_map_ui.draw(game_screen, 0, 0)
        plopped_master.update_mouse(mouse_position, mouse_clicked)
        plopped_master.draw(game_screen, game_map_ui.left_offset * 40, game_map_ui.top_offset * 40)
        game_map_ui.update_mouse_clicked(mouse_position, mouse_clicked)
        tower_bar.update_mouse(mouse_position, mouse_clicked)
        tower_bar.draw(game_screen, 0, 400)
        tower_description.update_mouse(mouse_position, mouse_clicked)
        tower_description.draw(game_screen, 0, 450)
        sim_toggle.add_clock_tick(clock_tick)
        sim_toggle.update_mouse(mouse_position, mouse_clicked)
        sim_toggle.draw(game_screen, 0, 550)
        sim_message.draw(game_screen, 60, 550)
        sim_entity_viewer.add_clock_tick(clock_tick)
        sim_entity_viewer.update_mouse(mouse_position, mouse_clicked)
        sim_entity_viewer.draw(game_screen, 600, 400)
        player_stats.draw(game_screen, 600, 550)
        critter_master.set_clock_tick(clock_tick)
        critter_master.update_mouse(mouse_position, mouse_clicked)
        critter_master.draw(game_screen, game_map_ui.left_offset * 40, game_map_ui.top_offset * 40)
        cursor.update_mouse(mouse_position, mouse_clicked)
        cursor.draw(game_screen, 0, 0)

        pygame.display.flip()

        clock_tick = update_fps()
        round_continues = sim.next_frame(clock_tick)

        if not round_continues:
            round_number += 1

            if round_number < len(game_map.rounds):
                sim = Sim(game_map.board, game_map.rounds[round_number], round_number + 1)
            else:
                game_finished = True


def init_pygame():
    icon = load_sprite('tower_basic_large')
    pygame.display.set_icon(icon)
    game_screen = pygame.display.set_mode(size=(800, 600))
    pygame.mouse.set_visible(False)
    return game_screen


def update_fps() -> int:
    clock_tick = CLOCK.tick()
    fps = CLOCK.get_fps()
    pygame.display.set_caption(f"Tower Defense Game. Current FPS = {int(fps)}")
    return clock_tick

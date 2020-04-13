import pygame

from game.draw.ui.sim_entity_viewer.critter_viewer.critter_viewer import CritterViewer
from game.draw.ui.sim_entity_viewer.tower_manager.tower_manager import TowerManager
from game.draw.ui.ui_element import UIElement
from game.state import get_state

BORDER_COLOR = pygame.Color(0, 0, 0)
BACKGROUND_COLOR = pygame.Color(185, 185, 185)


class SimEntityViewer(UIElement):
    def __init__(self):
        super().__init__()
        self.tower_manager = TowerManager()
        self.critter_viewer = CritterViewer()

    def draw(self, surface, left: int, top: int) -> None:
        self.draw_border(surface, left, top)
        self.draw_background(surface, left, top)

        state = get_state()
        selected_ploppable = state.get_selected_ploppable()
        selected_critter = state.get_selected_critter()

        if selected_ploppable:
            self.tower_manager.set_tower(selected_ploppable)
            self.tower_manager.draw(surface, left, top)
        elif selected_critter:
            self.critter_viewer.set_critter(selected_critter)
            self.critter_viewer.draw(surface, left, top)

    @staticmethod
    def draw_border(surface, left: int, top: int) -> None:
        width = 200
        height = 150

        rectangle = pygame.Rect(left, top, width, height)
        pygame.draw.rect(surface, BORDER_COLOR, rectangle)

    @staticmethod
    def draw_background(surface, left: int, top: int) -> None:
        width = 198
        height = 148

        rectangle = pygame.Rect(left + 1, top + 1, width, height)
        pygame.draw.rect(surface, BACKGROUND_COLOR, rectangle)

    def update_mouse(self, mouse_position, mouse_clicked) -> None:
        state = get_state()

        selected_ploppable = state.get_selected_ploppable()
        selected_critter = state.get_selected_critter()

        if selected_ploppable:
            self.tower_manager.update_mouse(mouse_position, mouse_clicked)
        elif selected_critter:
            self.critter_viewer.update_mouse(mouse_position, mouse_clicked)

    def add_clock_tick(self, clock_tick: int) -> None:
        self.tower_manager.add_clock_tick(clock_tick)

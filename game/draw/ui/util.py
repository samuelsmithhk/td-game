import os
import pygame

DIR_NAME = os.path.dirname(os.path.realpath(__file__))
SPRITES_PATH = os.path.join(DIR_NAME, '..', '..', '..', 'resources', 'sprites')


def load_sprite(sprite_name):
    sprite_path = os.path.join(SPRITES_PATH, f"{sprite_name}.png")
    return pygame.image.load(sprite_path)

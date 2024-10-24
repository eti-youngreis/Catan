import ctypes
import os
from typing import List

import cv2
import numpy as np

from logic.config.config_utils import ConfigUtils
from logic.input import Input




class Graphic:
    tile_paths_dict = {
        '1': 'tile_ground.png',
        '2': 'tile_water.png',
        '3': 'tile_forest.png',
        '4': 'tile_field.png',
        '5': 'tile_iron_mine.png',
        '6': 'tile_blocks_mine.png'
    }

    def __init__(self, config_utils):
        self._config_utils: ConfigUtils = config_utils

    def start(self, game_input: Input):
        world_map: List = game_input.world.data
        self.display_world_map(world_map)

    def display_world_map(self, world_map):

        user32 = ctypes.windll.user32
        screen_height = user32.GetSystemMetrics(1)

        window_height = int(screen_height * 0.5)

        tile_height = window_height // self._config_utils.get_tile_width()
        tile_width = window_height // self._config_utils.get_tile_length()
        tiles_path = 'graphic/TILES'
        rows = len(world_map)
        cols = len(world_map[0]) if rows > 0 else 0

        world_height = rows * tile_width
        world_width = cols * tile_height

        world_image = np.zeros((world_height, world_width, 3), dtype=np.uint8)

        for row_idx, row in enumerate(world_map):
            for col_idx, tile_num in enumerate(row):
                tile_image_path = os.path.join(tiles_path, self.tile_paths_dict[world_map[row_idx][col_idx]])
                tile_image = cv2.imread(tile_image_path)
                if tile_image is None:
                    print(f'Warning: Tile image {tile_image_path} not found')
                    continue
                tile_image = cv2.resize(tile_image, (tile_width, tile_height))
                world_image[row_idx * tile_height: (row_idx + 1) * tile_height,
                col_idx * tile_width: (col_idx + 1) * tile_width] = tile_image

        window_name = 'World Map'

        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.imshow(window_name, world_image)
        cv2.resizeWindow(window_name, window_height, window_height)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

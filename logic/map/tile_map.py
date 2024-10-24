from logic.map.map import Map


class TilesMap(Map):

    def elements_in_row(self, world):
        return len(world)

    def elements_in_col(self, world):
        return len(world[0])

    def value_in_row_col(self, world, row, col):
        return world[row][col]

    def selected_category(self, x: int, y: int) -> str:
        (tile_width, tile_length) = (self.config_utils.get_tile_width(), self.config_utils.get_tile_length())
        (x, y) = (x // tile_width, y // tile_length)
        tile_value = self.get_cell(x, y)
        return self.config_utils.get_tile_key_by_value(tile_value)

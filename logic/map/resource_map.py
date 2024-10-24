from typing import List

from logic.map.map import Map


class ResourcesMap(Map):
    def elements_in_row(self, world):
        return len(world)

    def elements_in_col(self, world):
        return len(world[0])

    def value_in_row_col(self, world: List[List[int]], row: int, col: int):
        """
        Returns a dictionary representing the type and count of a resource at a specific location in the world.

        Parameters: world (List[List[int]]): A 2D list representing the world, where each element is an integer
        representing a tile value. row (int): The row index of the tile in the world. col (int): The column index of
        the tile in the world.

        Returns: dict[str | None, int | None]: A dictionary with a single key-value pair, where the key is the
        type of resource (as a string) and the value is the count of that resource (as an integer). Both the key and
        the value can be None. For example: {'Wood': 10} or {None: None}
        """
        tile_value = world[row][col]
        return self.config_utils.get_resource_key_value_by_tile_value(tile_value)

    def rain(self, duration):
        self.map = [
            [
                {key: round(value + (0.0005 * duration if key == self.config_utils.WOOD else 0.001 * duration),
                            4) if key in [
                    self.config_utils.WOOD, self.config_utils.WOOL] else value}
                for cell in row
                for key, value in cell.items()
            ]
            for row in self.map
        ]

    def resource(self, arguments):
        count, resource, x, y = arguments
        tile_width, tile_length = self.config_utils.get_tile_width(), self.config_utils.get_tile_length()
        x, y = x // tile_width, y // tile_length
        resource_type = resource
        resource_count = count
        self.map[x][y] = {resource_type: resource_count}

    def available_resource(self, x_coordinate, y_coordinate):
        tile_width, tile_length = self.config_utils.get_tile_width(), self.config_utils.get_tile_length()
        x_coordinate, y_coordinate = x_coordinate // tile_width, y_coordinate // tile_length
        return self.get_cell(x_coordinate, y_coordinate)

    def selected_resource(self, x_coordinate, y_coordinate):
        cell = self.available_resource(x_coordinate, y_coordinate)
        resource_array = self.config_utils.get_empty_resources_array()
        resource = next(iter(cell))
        resource_array[resource] = cell[resource]
        return [int(resource) for resource in resource_array.values()]

    def work(self, x_coordinate, y_coordinate):
        tile_width, tile_length = self.config_utils.get_tile_width(), self.config_utils.get_tile_length()
        x_coordinate, y_coordinate = x_coordinate // tile_width, y_coordinate // tile_length
        cell = self.get_cell(x_coordinate, y_coordinate)
        resource = next(iter(cell))
        if resource:
            cell[resource] -= 1

    def make_empty(self, x, y):
        cell = self.get_cell(x, y)
        for key in cell.keys():
            cell[key] = 0

    def take_resources(self, x: int, y: int, resource_to_take: int):
        cell = self.get_cell(x, y)
        resource_type = next(iter(cell))
        cell[resource_type] -= resource_to_take

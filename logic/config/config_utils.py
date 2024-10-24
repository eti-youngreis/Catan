import traceback
from typing import List, Optional

from logic.utils import get_key_by_value, load_config



class ConfigUtils:
    WATER = 'Water'
    GROUND = 'Ground'
    FIELD = 'Field'
    FOREST = 'Forest'
    IRONMINE = 'IronMine'
    BLOCKSMINE = 'BlocksMine'

    WOOL = 'Wool'
    WOOD = 'Wood'
    BLOCKS = 'Blocks'
    IRON = 'Iron'
    PEOPLE = 'People'

    resource_for_tile = {
        GROUND: None,
        FIELD: WOOL,
        FOREST: WOOD,
        WATER: None,
        IRONMINE: IRON,
        BLOCKSMINE: BLOCKS
    }

    resource_index = {
        WOOD: 0,
        WOOL: 1,
        IRON: 2,
        BLOCKS: 3,
        PEOPLE: 4
    }

    def __init__(self, config_path):
        self._config = load_config(config_path)

    def get_object_size(self, object_type: str) -> List[int]:
        return self._config['Sizes'][object_type]

    def get_tile_width(self):
        return self._config['Sizes']['Tile'][1]

    def get_tile_length(self):
        return self._config['Sizes']['Tile'][0]

    def get_capacity(self, object_type_name: str) -> List[int]:
        return self._config['Capacities'][object_type_name]

    def get_resources_types(self):
        return self._config['ResourceTypes']

    def get_tile_key_by_value(self, tile_value: int) -> str:
        return get_key_by_value(self._config['Tiles'], tile_value)

    def get_resource_key_value_by_tile(self, tile_key: str):
        resource_type: Optional[str] = self.get_resource_key_by_tile_key(tile_key)
        resource_count: Optional[int] = self.get_starting_resource(tile_key) if resource_type else None
        return {resource_type: resource_count}

    @staticmethod
    def get_resource_key_by_tile_key(tile_key: str):
        return ConfigUtils.resource_for_tile[tile_key]

    def get_resource_key_by_tile(self, tile_value: int):
        tile_key = self.get_tile_key_by_value(tile_value)
        return self.get_resource_key_by_tile_key(tile_key)

    def get_starting_resources(self):
        return self._config['StartingResources']

    def get_starting_resource(self, tile_key: str) -> int:
        return self.get_starting_resources()[tile_key]

    def get_empty_resources_array(self):
        """
        Creates a dictionary with all resource types initialized to zero, excluding 'People'.

        Returns:
            dict[str, int]: A dictionary where each key is a type of resource (as a string) and each value is 0.
            For example: {'Wood': 0, 'Wool': 0, 'Iron': 0, 'Blocks': 0}
        """
        resources = {resource_type: 0 for resource_type in self.get_resources_types() if resource_type != 'People'}
        return resources

    def get_resource_key_value_by_tile_value(self, tile_value: int):
        tile_key: str = self.get_tile_key_by_value(tile_value)
        return self.get_resource_key_value_by_tile(tile_key)

    def get_resource_index(self, resource_name: str) -> int:
        try:
            return self.resource_index[resource_name]
        except KeyError:
            print(traceback.format_exc())

    def get_costs(self, object_type: str):
        return self._config['Costs'][object_type]

from typing import List, Type

from logic.world_object.transportation.transportation import Transportation
from logic.world_object.world_object import WorldObject


class Helicopter(Transportation):
    def get_costs(self):
        return self.config_utils.get_costs(WorldObject.HELICOPTER)

    def get_obstructing_objects(self) -> List[Type]:
        return [Helicopter]

    def get_capacity(self):
        return self.config_utils.get_capacity(WorldObject.HELICOPTER)

from abc import ABC

from logic.world_object.infrastructure.infrastructure import Infrastructure
from logic.world_object.world_object import WorldObject


class Settlement(Infrastructure, ABC):
    def __init__(self, config_utils):
        super().__init__(config_utils)
        self.objects_count = {WorldObject.PEOPLE: 0, WorldObject.CAR: 0, WorldObject.TRUCK: 0,
                              WorldObject.HELICOPTER: 0}

    def increase(self, object_type: str, count: int = 1):
        # TODO Check if there is a limit on the number of vehicles in a city/village
        capacities = self.config_utils.get_capacity(type(self).__name__)
        capacity_index = self.config_utils.get_resource_index(object_type)
        if capacity_index:
            self.objects_count[object_type] = min(count + self.objects_count[object_type], capacities[capacity_index])
        else:
            self.objects_count[object_type] = count + self.objects_count[object_type]

    def selected_object(self, object_type: str) -> int:
        return self.objects_count[object_type]

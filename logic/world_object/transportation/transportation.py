from abc import ABC, abstractmethod
from typing import List

from logic.world_object.world_object import WorldObject


class Transportation(WorldObject, ABC):

    def __init__(self, config_utils):
        super().__init__(config_utils)
        self._objects_count = {WorldObject.PEOPLE: 0}
        self._resources = self.config_utils.get_empty_resources_array()

    def selected_object(self, object_type: str) -> int:
        """

        :return: The number of objects of the requested type inside the vehicle
        """
        return self._objects_count[object_type]

    def get_size(self) -> List[int]:
        """
        :return: Width and length of the vehicle
        """
        return self.config_utils.get_object_size(type(self).__name__)

    @abstractmethod
    def get_capacity(self) -> List[int]:
        pass

    @abstractmethod
    def get_costs(self):
        pass

    def take_resource(self, resource_to_take):
        resource_type: str = next(iter(resource_to_take))
        resource_count: int = resource_to_take[resource_type]
        self._resources[resource_type] -= resource_count

from abc import ABC, abstractmethod
from typing import List, Type

from logic.world_object.world_object import WorldObject


class Infrastructure(WorldObject, ABC):

    def __init__(self, config_utils):
        super().__init__(config_utils)
        self.is_complete: bool = False

    def get_obstructing_objects(self) -> List[Type]:
        return [WorldObject.INFRASTRUCTURE]

    @abstractmethod
    def get_costs(self):
        pass

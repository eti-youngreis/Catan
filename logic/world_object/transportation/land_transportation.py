from abc import ABC
from typing import List, Type

from logic.world_object.people import People
from logic.world_object.transportation.transportation import Transportation


class LandTransportation(Transportation, ABC):
    def get_obstructing_objects(self) -> List[Type]:
        return [People, LandTransportation]

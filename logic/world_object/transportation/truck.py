from typing import List

from logic.world_object.transportation.land_transportation import LandTransportation
from logic.world_object.world_object import WorldObject


class Truck(LandTransportation):

    def get_costs(self):
        return self.config_utils.get_costs(WorldObject.TRUCK)

    def get_capacity(self) -> List[int]:
        return self.config_utils.get_capacity(WorldObject.TRUCK)

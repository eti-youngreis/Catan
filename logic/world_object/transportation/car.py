from logic.world_object.transportation.land_transportation import LandTransportation
from logic.world_object.world_object import WorldObject


class Car(LandTransportation):
    def get_costs(self):
        return self.config_utils.get_costs(WorldObject.CAR)

    def get_capacity(self):
        return self.config_utils.get_capacity(WorldObject.CAR)

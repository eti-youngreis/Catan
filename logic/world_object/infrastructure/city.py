from logic.world_object.infrastructure.settlement import Settlement
from logic.world_object.world_object import WorldObject


class City(Settlement):

    def get_costs(self):
        return self.config_utils.get_costs(WorldObject.CITY)

    def __init__(self, config_utils):
        Settlement.__init__(self, config_utils)

    def get_size(self):
        return self.config_utils.get_object_size(WorldObject.CITY)

from logic.world_object.infrastructure.infrastructure import Infrastructure
from logic.world_object.world_object import WorldObject


class Road(Infrastructure):
    def get_costs(self):
        return self.config_utils.get_costs(WorldObject.ROAD)

    def get_size(self):
        return self.config_utils.get_object_size(WorldObject.ROAD)

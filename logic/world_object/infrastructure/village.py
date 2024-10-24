from logic.world_object.world_object import WorldObject
from logic.world_object.infrastructure.settlement import Settlement


class Village(Settlement):
    def get_costs(self):
        return self.config_utils.get_costs(WorldObject.VILLAGE)

    def __init__(self, config_utils):
        super().__init__(config_utils)

    def get_size(self):
        return self.config_utils.get_object_size(WorldObject.VILLAGE)

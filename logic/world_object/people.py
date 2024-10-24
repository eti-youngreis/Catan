from logic.world_object.world_object import WorldObject


class People(WorldObject):

    def get_size(self):
        return self.config_utils.get_object_size(WorldObject.PEOPLE)

    def get_obstructing_objects(self):
        return []

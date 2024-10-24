from typing import Tuple
from logic.world import World
from logic.world_object.world_object import WorldObject


def convert_and_swap_indices(x, y) -> Tuple[int, int]:
    """
    Convert to int
    Convert 1-based indices to 0-based indices and swap them.
    """
    return int(y) - 1, int(x) - 1


class ActionHandler:

    def __init__(self, world: World):
        self._world: World = world
        self.last_selected_coordinates: tuple[int, int] = (0, 0)

    def resource(self, arguments, is_start_command):
        (count, resource, x, y) = arguments
        (count, x, y) = [int(arg) for arg in (count, x, y)]
        x, y = convert_and_swap_indices(x, y)
        self._world.resource([count, resource, x, y])

    def select(self, arguments, is_start_command):
        x, y = convert_and_swap_indices(arguments[0], arguments[1])
        self.last_selected_coordinates = (x, y)

    def people(self, arguments, is_start_command):
        (count, x, y) = [int(arg) for arg in arguments]
        x, y = convert_and_swap_indices(x, y)
        self._world.people(count, x, y)

    def work(self, arguments, is_start_command):
        x, y = convert_and_swap_indices(arguments[0], arguments[1])
        self._world.work(x, y)

    def rain(self, arguments, is_start_command):
        duration = int(arguments[0])
        self._world.rain(duration)

    def wait(self, arguments, is_start_command):
        self._world.wait(arguments)

    def build(self, arguments, is_start_command):
        obj_to_build = arguments[0]
        x, y = convert_and_swap_indices(arguments[1], arguments[2])
        self._world.build(obj_to_build, x, y, is_start_command)

    def make_empty(self, arguments, is_start_command):
        x, y = convert_and_swap_indices(arguments[0], arguments[1])
        self._world.make_empty(x, y)

    def deposit(self, arguments, is_start_command):
        dest_x, dest_y = convert_and_swap_indices(arguments[0], arguments[1])
        src_x, src_y = self.last_selected_coordinates

    def take_resources(self, arguments, is_start_command):
        x_dest, y_dest = convert_and_swap_indices(arguments[0], arguments[1])
        x_src, y_src = self.last_selected_coordinates
        self._world.take_resources(x_src, y_src, x_dest, y_dest)

    def manufacture(self, arguments, is_start_command):
        vehicle_type = arguments[0]
        x, y = convert_and_swap_indices(arguments[1], arguments[2])
        self._world.manufacture(vehicle_type, x, y, is_start_command)

    def selected_resource(self):
        (x, y) = self.last_selected_coordinates
        return self._world.selected_resource(x, y)

    def selected_category(self):
        x, y = self.last_selected_coordinates
        return self._world.selected_category(x, y)

    def selected_coordinates(self):
        return self.last_selected_coordinates

    def city_count(self):
        return self._world.object_count(WorldObject.CITY)

    def village_count(self):
        return self._world.object_count(WorldObject.VILLAGE)

    def road_count(self):
        return self._world.object_count(WorldObject.ROAD)

    def car_count(self):
        return self._world.object_count(WorldObject.CAR)

    def truck_count(self):
        return self._world.object_count(WorldObject.TRUCK)

    def helicopter_count(self):
        return self._world.object_count(WorldObject.HELICOPTER)

    def selected_complete(self):
        x, y = self.last_selected_coordinates
        return self._world.selected_complete(x, y)

    def selected_people(self):
        x, y = self.last_selected_coordinates
        return self._world.selected_object(x, y, WorldObject.PEOPLE)

    def selected_car(self):
        x, y = self.last_selected_coordinates
        return self._world.selected_object(x, y, WorldObject.CAR)

    def selected_truck(self):
        x, y = self.last_selected_coordinates
        return self._world.selected_object(x, y, WorldObject.TRUCK)

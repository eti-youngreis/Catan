from typing import List

from logic.world_object.infrastructure.city import City
from logic.config.config_utils import ConfigUtils
from logic.map.object_map import ObjectsMap
from logic.map.resource_map import ResourcesMap
from logic.map.tile_map import TilesMap
from logic.world_object.transportation.helicopter import Helicopter
from logic.world_object.infrastructure.infrastructure import Infrastructure
from logic.world_object.transportation.car import Car

from logic.world_object.transportation.transportation import Transportation
from logic.world_object.infrastructure.road import Road

from logic.world_object.transportation.truck import Truck
from logic.world_object.infrastructure.village import Village
from logic.world_object.world_object import WorldObject


class World:
    def __init__(self, config_utils):
        self._config_utils: ConfigUtils = config_utils
        self._tiles_map = TilesMap(config_utils)
        self._objects_map = ObjectsMap(config_utils)
        self._resources_map = ResourcesMap(config_utils)
        self._objects_counters: dict[str, int] = {
            WorldObject.CITY: 0,
            WorldObject.VILLAGE: 0,
            WorldObject.ROAD: 0,
            WorldObject.CAR: 0,
            WorldObject.TRUCK: 0,
            WorldObject.HELICOPTER: 0
        }

    def init_maps(self, world: List):
        self._resources_map.init_map(world)
        self._objects_map.init_map(world)
        self._tiles_map.init_map(world)

    def resource(self, arguments):
        self._resources_map.resource(arguments)

    def selected_resource(self, x, y):
        return self._resources_map.selected_resource(x, y)

    def people(self, count, x, y):
        self._objects_map.people(count, x, y)

    def work(self, x, y):
        self._resources_map.work(x, y)

    def selected_category(self, x: int, y: int) -> str:
        return self._objects_map.selected_category(x, y) or self._tiles_map.selected_category(
            x, y)

    def rain(self, arguments):
        self._resources_map.rain(arguments)

    def wait(self, arguments):
        pass

    def build(self, obj_to_build: str, x: int, y: int, is_start_command: bool):
        infrastructure_class_dict = {WorldObject.CITY: City, WorldObject.VILLAGE: Village, WorldObject.ROAD: Road}
        obj_class = infrastructure_class_dict[obj_to_build]
        new_object: Infrastructure = obj_class(self._config_utils)
        if not is_start_command:
            tile_type = self._tiles_map.selected_category(x, y)
            if (tile_type != self._config_utils.GROUND or
                    not self._objects_map.is_land_available(x, y, new_object) or
                    not isinstance(new_object, Road) and
                    not self._objects_map.is_there_road(x, y, new_object)):
                return False
        self._objects_counters[obj_to_build] += 1
        self._objects_map.build(new_object, x, y)
        return True

    def manufacture(self, vehicle_type: str, x: int, y: int, is_start_command: bool) -> bool:
        transportation_class_dict = {WorldObject.CAR: Car, WorldObject.TRUCK: Truck, WorldObject.HELICOPTER: Helicopter}
        new_vehicle: Transportation = transportation_class_dict[vehicle_type](self._config_utils)
        if not is_start_command:
            if not self._objects_map.is_land_available(x, y, new_vehicle):
                return False
            resources = self._resources_map.selected_resource(x, y)
            costs = self._objects_map.costs(new_vehicle)
            if any(cost > resource for cost, resource in zip(costs, resources)):
                return False
        self._objects_counters[vehicle_type] += 1
        self._objects_map.manufacture(new_vehicle, x, y)
        return True

    def object_count(self, object_type: str) -> int:
        return self._objects_counters[object_type]

    def selected_complete(self, x: int, y: int) -> bool:
        return self._objects_map.selected_complete(x, y)

    def village_count(self):
        return self._objects_counters[WorldObject.VILLAGE]

    def road_count(self):
        return self._objects_counters[WorldObject.ROAD]

    def make_empty(self, x, y):
        self._resources_map.make_empty(x, y)

    def selected_object(self, x, y, obj_type):
        return self._objects_map.selected_object(x, y, obj_type)

    def take_resources(self, x_vehicle: int, y_vehicle: int, x_dest: int, y_dest: int) -> None:
        current_content = self._resources_map.available_resource(x_vehicle, y_vehicle)
        resource_capacity: List[int] = self._objects_map.get_vehicle_capacity(x_vehicle, y_vehicle)
        available_resource: dict[str, int] = self._resources_map.available_resource(x_dest, y_dest)
        resource_type: str = next(iter(available_resource))
        if resource_type not in current_content:
            current_content = {resource_type: 0}
        resource_index: int = self._config_utils.get_resource_index(resource_type)
        resource_to_take = {
            resource_type: min(resource_capacity[resource_index] - current_content[resource_type],
                               available_resource[resource_type])}
        self._resources_map.take_resources(x_dest, y_dest, resource_to_take[resource_type])
        # self._objects_map.take_resources(x_vehicle, y_vehicle, resource_to_take)

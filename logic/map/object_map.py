import traceback

from logic.world_object.transportation.car import Car
from logic.world_object.transportation.helicopter import Helicopter
from logic.world_object.transportation.truck import Truck
from logic.world_object.transportation.transportation import Transportation
from logic.world_object.infrastructure.road import Road
from logic.world_object.infrastructure.settlement import Settlement
from logic.world_object.infrastructure.village import Village
from logic.world_object.infrastructure.city import City
from logic.world_object.infrastructure.infrastructure import Infrastructure
from logic.utils import get_key_by_value
from logic.map.map import Map
from logic.world_object.people import People

from logic.world_object.world_object import WorldObject


class ObjectsMap(Map):
    objects_dict = {
        WorldObject.CITY: City,
        WorldObject.VILLAGE: Village,
        WorldObject.ROAD: Road,
        WorldObject.CAR: Car,
        WorldObject.TRUCK: Truck,
        WorldObject.HELICOPTER: Helicopter
    }
    priority = [WorldObject.CITY, WorldObject.VILLAGE, WorldObject.HELICOPTER,
                WorldObject.TRUCK,
                WorldObject.CAR,
                WorldObject.PEOPLE, WorldObject.ROAD]

    def elements_in_col(self, world):
        tile_length = self.config_utils.get_tile_length()
        return tile_length * len(world[0])

    def elements_in_row(self, world):
        tile_width = self.config_utils.get_tile_width()
        return tile_width * len(world)

    def value_in_row_col(self, world, row, col):
        return {WorldObject.PEOPLE: None, WorldObject.CAR: None, WorldObject.TRUCK: None,
                WorldObject.HELICOPTER: None,
                WorldObject.VILLAGE: None, WorldObject.CITY: None, WorldObject.ROAD: None}

    def people(self, count, x, y):
        cell_objects = self.get_cell(x, y)
        for obj_type_name in self.priority:
            if cell_objects[obj_type_name] and obj_type_name != WorldObject.PEOPLE:
                cell_objects[obj_type_name].increase(WorldObject.PEOPLE, count)
                return
        cell_objects[WorldObject.PEOPLE] = People(self.config_utils)

    def build(self, obj_to_build: Infrastructure, x: int, y: int):
        (object_width, object_length) = [size for size in obj_to_build.get_size()]
        for i in range(x, x + object_length):
            for j in range(y, y + object_width):
                self.map[i][j][type(obj_to_build).__name__] = obj_to_build

    def manufacture(self, vehicle_to_manufacture: Transportation, x: int, y: int) -> None:
        cell_objects = self.get_cell(x, y)
        vehicle_type: str = get_key_by_value(self.objects_dict, type(vehicle_to_manufacture))
        for obj_type in self.priority:
            if cell_objects[obj_type]:
                if isinstance(cell_objects[obj_type], Settlement):
                    cell_objects[obj_type].increase(vehicle_type)
        cell_objects[vehicle_type] = vehicle_to_manufacture

    def is_land_available(self, x: int, y: int, obj_to_build: WorldObject) -> bool:
        obstructing_objects = obj_to_build.get_obstructing_objects()
        (object_width, object_length) = [size for size in obj_to_build.get_size()]
        for i in range(x, x + object_width):
            for j in range(y, y + object_length):
                if any([obj for obj in self.map[i][j] if type(obj) in obstructing_objects]):
                    return False
        return True

    def is_there_road(self, x, y, obj_to_build: Infrastructure):
        object_width, object_length = obj_to_build.get_size()
        for i in range(x, x + object_width):
            for j in [y - 1, y + 1]:
                if 0 <= j < len(self.map[0]) and self.map[i][j].get(WorldObject.ROAD, False):
                    return True
        for i in range(y, y + object_length):
            for j in [x - 1, x + 1]:
                if 0 <= j < len(self.map) and self.map[j][i].get(WorldObject.ROAD, False):
                    return True
        return False

    def _select_obj(self, x: int, y: int):
        cell_objects = self.get_cell(x,
                                     y)
        try:
            return [cell_objects[world_object] for world_object in self.priority if cell_objects[world_object]][
                0]
        except IndexError:
            return None

    def selected_category(self, x: int, y: int):
        selected_object = self._select_obj(x, y)
        if selected_object:
            return type(selected_object).__name__
        return None

    def selected_complete(self, x: int, y: int) -> bool:
        selected_obj = self._select_obj(x, y)
        if isinstance(selected_obj, Infrastructure):
            return selected_obj.is_complete

    def selected_object(self, x, y, obj_type):
        selected_obj = self._select_obj(x, y)
        try:
            return selected_obj.selected_object(obj_type)
        except AttributeError:
            print(traceback.format_exc())

    def take_resources(self, x_vehicle: int, y_vehicle: int, resource_to_take):
        selected_vehicle = self._select_obj(x_vehicle, y_vehicle)
        if isinstance(selected_vehicle, Transportation):
            selected_vehicle.take_resource(resource_to_take)

    def get_vehicle_capacity(self, x_vehicle: int, y_vehicle: int):
        selected_vehicle = self._select_obj(x_vehicle, y_vehicle)
        try:
            return selected_vehicle.get_capacity()
        except TypeError:
            return None

    @staticmethod
    def costs(new_vehicle):
        return new_vehicle.get_costs()

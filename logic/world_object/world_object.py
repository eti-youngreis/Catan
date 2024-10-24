from abc import abstractmethod, ABC
from typing import List, Type

from logic.config.config_utils import ConfigUtils


class WorldObject(ABC):
    TRANSPORTATION = 'Transportation'
    INFRASTRUCTURE = 'Infrastructure'

    PEOPLE = 'People'
    CAR = 'Car'
    TRUCK = 'Truck'
    HELICOPTER = 'Helicopter'
    ROAD = 'Road'
    VILLAGE = 'Village'
    CITY = 'City'

    def __init__(self, config_utils):
        self.config_utils: ConfigUtils = config_utils

    @abstractmethod
    def get_size(self):
        pass

    @abstractmethod
    def get_obstructing_objects(self) -> List[Type]:
        pass

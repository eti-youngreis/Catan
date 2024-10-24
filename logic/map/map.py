from abc import ABC, abstractmethod

from logic.config.config_utils import ConfigUtils
from utils import print_error


class Map(ABC):
    def __init__(self, config_utils: ConfigUtils):
        self.config_utils: ConfigUtils = config_utils
        self.map = None

    @abstractmethod
    def elements_in_col(self, world):
        pass

    @abstractmethod
    def elements_in_row(self, world):
        pass

    @abstractmethod
    def value_in_row_col(self, world, row, col):
        pass

    def get_cell(self, x, y):
        return self.map[x][y]

    def init_map(self, world):
        try:
            elements_in_col = self.elements_in_col(world)
            elements_in_row = self.elements_in_row(world)
            self.map = [[self.value_in_row_col(world, row, col) for col in range(elements_in_col)] for row in
                        range(elements_in_row)]
        except Exception as e:
            print_error(type(self).__name__, self.init_map.__name__, e)

import traceback
from typing import Optional


from graphic.graphic_main import Graphic
from input import Input
from logic.command.action_handler import ActionHandler
from logic.config.config_utils import ConfigUtils
from utils import camel_to_snake
from world import World


class Game:
    def __init__(self):
        self._input: Optional[Input] = None
        self._world: Optional[World] = None
        self._action_handler: Optional[ActionHandler] = None

    def _start(self):
        try:
            for command in self._input.start:
                getattr(ActionHandler, camel_to_snake(command.name))(self._action_handler,
                                                                     command.arguments, True)
        except AttributeError:
            print(traceback.format_exc())

    def _steps(self):
        try:
            for command in self._input.steps:
                getattr(ActionHandler, camel_to_snake(command.name))(self._action_handler,
                                                                     command.arguments, False)
        except AttributeError:
            print(traceback.format_exc())

    def _asserts(self):
        try:
            asserts_output = [
                [_assert, getattr(ActionHandler, camel_to_snake(_assert))(self._action_handler)]
                for
                _assert in
                self._input.asserts]
            return asserts_output
        except AttributeError:
            print(traceback.format_exc())

    def start_game(self):
        try:
            self._input = Input()  # get input
            self._input.parse_and_store()  # input handling
        except Exception as e:
            print("Error in input handling", e)
        else:
            config_utils = ConfigUtils('logic/config/configuration.json')
            graphic = Graphic(config_utils)
            graphic.start(self._input)  # call the graphic side
            self._world = World(config_utils)
            self._action_handler = ActionHandler(self._world)
            self._world.init_maps(self._input.world.data)
            self._start()
            self._steps()
            print(self._asserts())

from typing import List

from logic.command.command import Command



class Input:
    def __init__(self):
        self.world: Command = Command(Command.WORLD)
        self.start: List[Command] = list()
        self.steps: List[Command] = list()
        self.asserts: List[str] = list()
        self.at_line: int = 0

    @staticmethod
    def _next_line() -> str:
        line: str = input()
        return line

    def parse_and_store(self):
        try:
            line: str = self._next_line()
            command_list: List[Command] = self.start
            parsing_world: bool = False
            asserts_reached: bool = False
            while line:
                line = line.strip()
                if line.startswith('+'):
                    # command block reached (e.g.: World, Infrastructure, etc...)
                    name = line[1:]
                    parsing_world = False
                    if name == Command.WORLD:
                        parsing_world = True
                    elif name == Command.START:
                        command_list = self.start
                    elif name == Command.INPUT:
                        command_list = self.steps
                    elif name == Command.ASSERTS:
                        asserts_reached = True
                    else:
                        raise KeyError("Unknown Input Command found: " + name)
                else:
                    if asserts_reached:
                        self.asserts.append(line)
                    elif parsing_world:
                        self.world.data.append(line.split())
                    else:
                        command = Input.parse_command(line)
                        command_list.append(command)
                        # self.steps.append(command)
                # read next input line
                line = self._next_line()
        except EOFError:
            pass

    @staticmethod
    def parse_command(line: str) -> Command:
        strings = line.split()
        command = Command(strings[0])
        command.arguments.extend(strings[1:])
        return command

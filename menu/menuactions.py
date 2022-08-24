from abc import ABC, abstractmethod
from enum import Enum, auto

class MenuAction(ABC):

    class Action(Enum):
        UP = auto()
        DOWN = auto()
        LEFT = auto()
        RIGHT = auto()
        SELECT = auto()
        HOME = auto()
        QUIT = auto()
        NONE = auto()

    @abstractmethod
    def get_action(self) -> Action:
        pass

    @abstractmethod
    def map_input_to_action(self, value) -> Action:
        pass

class KeyboardMenuAction(MenuAction):

    # a=home
    # s=<nothing>
    # i=up,m=down,j=<nothing>,l=select
    # q=quit

    def get_action(self) -> MenuAction.Action:
        charVal = input('enter menu cmd ')
        return self.map_input_to_action(charVal)

    def map_input_to_action(self, value) -> MenuAction.Action:
        match value:
            case 'i':
                return MenuAction.Action.UP
            case 'm':
                return MenuAction.Action.DOWN
            case 'l' | 's':
                return MenuAction.Action.SELECT
            case 'a':
                return MenuAction.Action.HOME
            case 'q':
                return MenuAction.Action.QUIT
            case _:
                return MenuAction.Action.NONE
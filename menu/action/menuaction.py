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
    def get_actions(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def map_input_to_action(self, value) -> Action:
        pass

from abc import ABC, abstractmethod

from menu.menus import MenuNode

class Display(ABC):

    @abstractmethod
    def display_menu(self, menunode: MenuNode):
        pass

    @abstractmethod
    def display_output(self, output: str):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass
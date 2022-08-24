from abc import ABC, abstractmethod
from .menus import MenuNode

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

class TerminalDisplay(Display):

    def display_menu(self, menunode: MenuNode, cursorPos: int):
        selectionOptions = menunode.selection_options
        if selectionOptions is None or len(selectionOptions) == 0:
            raise Exception("Must have selection options to display")

        for pos, selectionOption in enumerate(selectionOptions):
            if pos==cursorPos:
                print("> "+str(pos)+": "+selectionOption.display_name)
            else:
                print("  "+str(pos)+": "+selectionOption.display_name)

    def display_output(self, menunode: MenuNode, output: str):
        print(output)

    def clear(self):
        pass

#class BoundedDisplay(Display):

#class BoundedTerminalDisplay(BoundedDisplay):

#class LCDDisplay(BoundedDisplay):

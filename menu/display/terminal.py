import platform, os

from menu.display.display import Display
from menu.menus import MenuNode

class TerminalDisplay(Display):

    # for unit test mocking purposes
    def _output_data(self, output: str):
        print(output)

    def display_menu(self, menunode: MenuNode, cursorPos: int):
        selectionOptions = menunode.selection_options
        if not selectionOptions:
            raise Exception("Must have selection options to display")

        for pos, selectionOption in enumerate(selectionOptions):
            if pos==cursorPos:
                self._output_data("> "+str(pos)+": "+selectionOption.display_name)
            else:
                self._output_data("  "+str(pos)+": "+selectionOption.display_name)

    def display_output(self, menunode: MenuNode, output: str):
        self._output_data(output)

    def clear(self):
        osSystem = platform.system()
        if osSystem == 'Windows':
            os.system('cls')
        elif osSystem == 'Linux':
            os.system('clear')
        else:
            raise Exception("Unknown os for display clear")
        
    def cleanup(self):
        self.clear()


from abc import ABC, abstractmethod
from doctest import OutputChecker
from .menus import MenuNode
from .menus import SelectionOption
from typing import List
import platform, os

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

class TerminalDisplay(Display):

    # for unit test mocking purposes
    def _output_data(self, output: str):
        print(output)

    def display_menu(self, menunode: MenuNode, cursorPos: int):
        selectionOptions = menunode.selection_options
        if selectionOptions is None or len(selectionOptions) == 0:
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

# Not meant for instantiation
class BoundedCharacterDisplay(Display):
    def __init__(self, numRows: int, numColumns: int, characterEncoding: str):
        self._numRows = numRows
        if (numRows == 0):
            raise Exception("Number of rows must be greater than zero")
        self._numColumns = numColumns
        if (numColumns == 0):
            raise Exception("Number of columns must be greater than zero")
        self._characterEncoding = characterEncoding
        self.set_window(0)

    def set_window(self, cursor: int):
        if cursor == 0:
            self._windowTop = 0
            self._windowBottom = self._numRows-1
        elif cursor < self._windowTop:
            self._windowTop -= 1
            self._windowBottom -= 1
        elif cursor > self._windowBottom:
            self._windowTop += 1
            self._windowBottom += 1

    def prepare_selection_menu_display_buffer(self, selectionOptions: List[SelectionOption], windowTop: int, windowBottom: int, cursorPos: int) -> List[bytearray]:

        windowOptions = [(position, selectionOption) for position, selectionOption in enumerate(selectionOptions)]

        rowByteArrays = []

        for selOption in windowOptions[self._windowTop:self._windowBottom+1]:
            selectionNum = selOption[0]
            option = selOption[1]
            prepend = ' '
            if selectionNum==cursorPos:
                prepend = '>'
            displayString = prepend+str(selectionNum+1)+": "+option.display_name
            clippedDisplayString = displayString[0:self._numColumns]
            rowByteArrays.append(bytearray(clippedDisplayString, self._characterEncoding))

        return rowByteArrays

    def prepare_output_display_buffer(self, output: str, numRows, numColumns) -> List[bytearray]:

        rowByteArrays = []
        splitNum = numColumns
        rows = [output[i:i+splitNum] for i in range(0, len(output), splitNum)]
        numToOutput = min(len(rows), numRows)
        for rowNum in range(numToOutput):
            rowByteArrays.append(bytearray(rows[rowNum], self._characterEncoding))

        return rowByteArrays


class BoundedCharacterTerminalDisplay(BoundedCharacterDisplay):
    def __init__(self, rows: int, columns: int, characterEncoding: str):
        super().__init__(rows, columns, characterEncoding)

    def display_menu(self, menunode: MenuNode, cursorPos: int):

        selectionOptions = menunode.selection_options
        if selectionOptions is None or len(selectionOptions) == 0:
            raise Exception("Must have selection options to display")

        self.set_window(cursorPos)

        displayBuffer = self.prepare_selection_menu_display_buffer(selectionOptions, self._windowTop, self._windowBottom, cursorPos)
        for row in displayBuffer:
            print(row.decode(self._characterEncoding))

    def display_output(self, menunode: MenuNode, output: str):
        if output is None or len(output) == 0:
            return

        displayBuffer = self.prepare_output_display_buffer(output, self._numRows, self._numColumns)
        for row in displayBuffer:
            print(row.decode(self._characterEncoding))

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

class Sparkfun4x20LCDDisplay(BoundedCharacterDisplay):
    def __init__(self, rows: int, columns: int, characterEncoding: str):
        super().__init__(rows, columns, characterEncoding)

    def display_menu(self, menunode: MenuNode, cursorPos: int):

        selectionOptions = menunode.selection_options
        if selectionOptions is None or len(selectionOptions) == 0:
            raise Exception("Must have selection options to display")

        self.set_window(cursorPos)

        displayBuffer = self.prepare_selection_menu_display_buffer(selectionOptions, self._windowTop, self._windowBottom, cursorPos)
        for row in displayBuffer:

            print(row.decode(self._characterEncoding))
            #TODO: send row to lcd display
            #can we send the whole thing as one giant string?

    def display_output(self, menunode: MenuNode, output: str):
        if output is None or len(output) == 0:
            return

        displayBuffer = self.prepare_output_display_buffer(output, self._numRows, self._numColumns)
        for row in displayBuffer:

            print(row.decode(self._characterEncoding))
            #TODO: send row to lcd display
            #can we send the whole thing as one giant string?

    def clear(self):
        pass
        # TODO: send command for clearing sparkfun lcd

    def cleanup(self):
        # TODO: maybe we can write a "goodbye!" to the lcd or something else besides clearing it?
        self._clear()
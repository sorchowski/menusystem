from typing import List
import os, platform, logging

from menu.menus import SelectionOption
from menu.display.display import Display
from menu.menus import MenuNode

# Not meant for instantiation
class BoundedCharacterDisplay(Display):
    def __init__(self, numRows: int, numColumns: int, characterEncoding: str):
        self._numRows = numRows
        if (numRows == 0):
            logging.error("Number of rows must be greater than zero")
            raise Exception("Number of rows must be greater than zero")
        self._numColumns = numColumns
        if (numColumns == 0):
            logging.error("Number of columns must be greater than zero")
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

        for selOption in windowOptions[windowTop:windowBottom+1]:
            selectionNum = selOption[0]
            option = selOption[1]
            prepend = ' '
            if selectionNum==cursorPos:
                prepend = '>'
            displayString = prepend+str(selectionNum+1)+": "+option.display_name
            clippedDisplayString = displayString[0:self._numColumns]
            paddedAndClippedDisplayString = clippedDisplayString.ljust(self._numColumns)
            rowByteArrays.append(bytearray(paddedAndClippedDisplayString, self._characterEncoding))

        return rowByteArrays

    def prepare_output_display_buffer(self, output: bytearray, numRows, numColumns) -> List[bytearray]:

        rowByteArrays = []
        splitNum = numColumns
        rows = [output[i:i+splitNum] for i in range(0, len(output), splitNum)]
        numToOutput = min(len(rows), numRows)
        for rowNum in range(numToOutput):
            rowByteArrays.append(rows[rowNum])

        return rowByteArrays

class BoundedCharacterTerminalDisplay(BoundedCharacterDisplay):
    def __init__(self, rows: int, columns: int, characterEncoding: str):
        super().__init__(rows, columns, characterEncoding)

    def display_menu(self, menunode: MenuNode, cursorPos: int):

        selectionOptions = menunode.selection_options
        if not selectionOptions:
            logging.error("Must have selection options to display menu")
            raise Exception("Must have selection options to display")

        self.set_window(cursorPos)

        displayBuffer = self.prepare_selection_menu_display_buffer(selectionOptions, self._windowTop, self._windowBottom, cursorPos)
        for row in displayBuffer:
            print(row.decode(self._characterEncoding))

    def display_output(self, menunode: MenuNode, output: str):
        if not output:
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


from menus import MenuNode
from menu.display.bounded import BoundedCharacterDisplay
from qwiic_serlcd import QwiicSerlcd

#    sudo pip install sparkfun-qwiic-i2c
#    sudo pip install sparkfun-qwiic-serlcd

class Sparkfun4x20LCDDisplay(BoundedCharacterDisplay):
    def __init__(self, rows: int, columns: int, characterEncoding: str):
        super().__init__(rows, columns, characterEncoding)

        self._lcd = QwiicSerlcd()
        if self._lcd.connected == False:
            raise Exception("Error starting LCD")

        self._lcd.setBacklight(0, 0, 0) # black is off
	    self._lcd.setContrast(5)        # set contrast. Lower to 0 for higher contrast.
        self._lcd.clearScreen()         # clear the screen - this moves the cursor to the home position as well
        self._lcd.leftToRight()
	    self._lcd.noCursor()            # I think this just removes the blinking cursor

    def display_menu(self, menunode: MenuNode, cursorPos: int):

        selectionOptions = menunode.selection_options
        if selectionOptions is None or len(selectionOptions) == 0:
            raise Exception("Must have selection options to display")

        self.set_window(cursorPos)

        displayBuffer = self.prepare_selection_menu_display_buffer(selectionOptions, self._windowTop, self._windowBottom, cursorPos)
        for row in displayBuffer:

            rowData = row.decode(self._characterEncoding)

            print(rowData)
            #myLCD.setCursor(column, row) Is this necessary?
            self._lcd.print(rowData)
            #can we send the whole thing as one giant string?

    def display_output(self, menunode: MenuNode, output: str):
        if output is None or len(output) == 0:
            return

        displayBuffer = self.prepare_output_display_buffer(output, self._numRows, self._numColumns)
        for row in displayBuffer:

            rowData = row.decode(self._characterEncoding)

            print(rowData)
            #myLCD.setCursor(column, row) Is this necessary?
            self._lcd.print(rowData)
            #can we send the whole thing as one giant string?

    def clear(self):
        self._lcd.clearScreen()         # clear the screen - this moves the cursor to the home position as well

    def cleanup(self):
        # TODO: maybe we can write a "goodbye!" to the lcd or something else besides clearing it?
        self._clear()
        #self._lcd.noDisplay()  Would we also need a call to self._lcd.display() during this object's init?
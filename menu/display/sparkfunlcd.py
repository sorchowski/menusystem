import time
from typing import List

from menu.menus import MenuNode
from menu.display.bounded import BoundedCharacterDisplay
from qwiic_serlcd import QwiicSerlcd

#    sudo pip install sparkfun-qwiic-i2c
#    sudo pip install sparkfun-qwiic-serlcd

class Sparkfun4x20LCDDisplay(BoundedCharacterDisplay):

    def __init__(self, rows: int, columns: int, characterEncoding: str):
        super().__init__(rows, columns, characterEncoding)

        self._numRetries = 3

        self._init_lcd()

        self._lcd.setBacklight(0, 0, 0) # black is off
        self._lcd.setContrast(5)        # set contrast. Lower to 0 for higher contrast.
        self._lcd.clearScreen()         # clear the screen - this moves the cursor to the home position as well
        self._lcd.leftToRight()
        self._lcd.noCursor()            # I think this just removes the blinking cursor

    def _init_lcd(self):
        self._lcd = QwiicSerlcd()
        if self._lcd.connected == False:
            raise Exception("Error starting LCD")

    def display_menu(self, menunode: MenuNode, cursorPos: int):

        self.clear()

        selectionOptions = menunode.selection_options
        if not selectionOptions:
            raise Exception("Must have selection options to display")

        self.set_window(cursorPos)

        displayBuffer = self.prepare_selection_menu_display_buffer(selectionOptions, self._windowTop, self._windowBottom, cursorPos)
        self._send_data_to_lcd(displayBuffer)

    def display_output(self, menunode: MenuNode, output: str):

        self.clear()

        if not output:
            return

        displayBuffer = self.prepare_output_display_buffer(output, self._numRows, self._numColumns)
        self._send_data_to_lcd(displayBuffer)

    def _send_data_to_lcd(self, displayBuffer: List):

        # This is to mitigate i2c connection issues with the lcd device
        # Every 4-6 button presses and menu updates, the rpi would lose
        # connectivity with the lcd. If we get a connection exception
        # restart the lcd and resend the menu commands
        for n in range(self._numRetries):
            try:
                for rowNum, row in enumerate(displayBuffer):

                    rowData = row.decode(self._characterEncoding)

                    self._lcd.setCursor(0, rowNum)
                    self._lcd.print(rowData)

                return

            except:
                time.sleep(0.2)
                self._init_lcd()
                self.clear()


    def clear(self):
        self._lcd.clearScreen()         # clear the screen - this moves the cursor to the home position as well

    def cleanup(self):
        # TODO: maybe we can write a "goodbye!" to the lcd or something else besides clearing it?
        self.clear()
        #self._lcd.noDisplay()  Would we also need a call to self._lcd.display() during this object's init?


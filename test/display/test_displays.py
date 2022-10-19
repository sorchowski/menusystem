import unittest
from unittest.mock import MagicMock, call, patch

from menu.menus import MenuNode, MenuNodeType, SelectionOption, MenuDestination
from menu.display.terminal import TerminalDisplay
from menu.display.bounded import BoundedCharacterTerminalDisplay
from menu.display.sparkfunlcd import Sparkfun4x20LCDDisplay

class TestTerminalDisplay(unittest.TestCase):

    def setUp(self):
        self._terminalDisplay = TerminalDisplay()

    def test_display_menu_exception(self):
        emptyMenuNode = MenuNode(id=None, menuNodeType=None, selectionOptions=None, confirm=True, executorNodeId=None, isRoot=False)
        with self.assertRaises(Exception) as ecm:
            self._terminalDisplay.display_menu(emptyMenuNode, None)
        
        actualException = ecm.exception
        self.assertEqual(str(actualException), "Must have selection options to display")

    def test_display_menu(self):
        displayName1 = "Option1"
        displayName2 = "Option2"
        selOption1 = SelectionOption(id="1234", displayName=displayName1)
        selOption2 = SelectionOption(id="4321", displayName=displayName2)
        selectionOptions = [selOption1, selOption2]
        menuNodeWithSelections = MenuNode(id=None, menuNodeType=MenuNodeType.SELECTION, selectionOptions=selectionOptions, confirm=False, executorNodeId=None, isRoot=False)

        self._terminalDisplay._output_data = MagicMock()

        self._terminalDisplay.display_menu(menuNodeWithSelections, 1)

        calls = [call('  0: Option1'), call('> 1: Option2')]
        self._terminalDisplay._output_data.assert_has_calls(calls)


class TestBoundedCharacterTerminalDisplay(unittest.TestCase):

    def setUp(self):
        self._boundedDisplay = BoundedCharacterTerminalDisplay(rows=4, columns=20, characterEncoding='ascii')

    def test_init_exception_rows(self):
        with self.assertRaises(Exception) as ecm:
            BoundedCharacterTerminalDisplay(rows=0, columns=20, characterEncoding='ascii')

        actualException = ecm.exception
        self.assertEqual(str(actualException), 'Number of rows must be greater than zero')

    def test_init_exception_columns(self):
        with self.assertRaises(Exception) as ecm:
            BoundedCharacterTerminalDisplay(rows=4, columns=0, characterEncoding='ascii')

        actualException = ecm.exception
        self.assertEqual(str(actualException), 'Number of columns must be greater than zero')

    def test_prepare_selection_menu_display_buffer(self):
        selectionOptions = [SelectionOption("id1", "Option 1"), SelectionOption("id2", "Option 2"), SelectionOption("id3", "Option 3"), SelectionOption("id4", "Option 4"), SelectionOption("id5", "Option 5")]

        rowByteArrays = self._boundedDisplay.prepare_selection_menu_display_buffer(selectionOptions, windowTop=0, windowBottom=3, cursorPos=0)

        self.assertEqual(4, len(rowByteArrays))
        self.assertEqual(rowByteArrays[0].decode(), '>1: Option 1        ')
        self.assertEqual(rowByteArrays[1].decode(), ' 2: Option 2        ')
        self.assertEqual(rowByteArrays[2].decode(), ' 3: Option 3        ')
        self.assertEqual(rowByteArrays[3].decode(), ' 4: Option 4        ')

    def test_prepare_output_display_buffer(self):
        
        output = bytearray("01234567890123456789012345678901234567890", 'ascii')
        numRows = 4
        numColumns = 20

        rowByteArrays = self._boundedDisplay.prepare_output_display_buffer(output, numRows, numColumns)

        self.assertEqual(3, len(rowByteArrays))
        self.assertEqual(rowByteArrays[0].decode(), '01234567890123456789')
        self.assertEqual(rowByteArrays[1].decode(), '01234567890123456789')
        self.assertEqual(rowByteArrays[2].decode(), '0')

    def test_display_menu_exception(self):
 
        menuNode = MenuNode(id='', menuNodeType=None, selectionOptions=None, confirm=False, executorNodeId=None, isRoot=False)

        with self.assertRaises(Exception) as ecm:        
            self._boundedDisplay.display_menu(menuNode, 0)

        actualException = ecm.exception
        self.assertEqual(str(actualException), "Must have selection options to display")

    def test_display_output_not_called(self):

        menuNode = MenuNode(id='', menuNodeType=None, selectionOptions=None, confirm=False, executorNodeId=None, isRoot=False)
        self._boundedDisplay._output_data = MagicMock()

        self._boundedDisplay.display_output(menuNode, None)
        self._boundedDisplay._output_data.assert_not_called()

    def test_display_menu(self):

        selectionOptions = [SelectionOption("id1", "Option 1"), SelectionOption("id2", "Option 2"), SelectionOption("id3", "Option 3"), SelectionOption("id4", "Option 4"), SelectionOption("id5", "Option 5")]
        menuNode = MenuNode(id='', menuNodeType=None, selectionOptions=selectionOptions, confirm=False, executorNodeId=None, isRoot=False)

        self._boundedDisplay._output_data = MagicMock()
        self._boundedDisplay.display_menu(menuNode, 1)

        calls = [call(' 1: Option 1        '), call('>2: Option 2        '), call(' 3: Option 3        '), call(' 4: Option 4        ')]
        self._boundedDisplay._output_data.assert_has_calls(calls)

    def test_display_output(self):

        output = bytearray("01234567890123456789012345678901234567890", 'ascii')

        self._boundedDisplay._output_data = MagicMock()
        calls = [call('01234567890123456789'), call('01234567890123456789'), call('0')]

        self._boundedDisplay.display_output(None, output) 
        self._boundedDisplay._output_data.assert_has_calls(calls)

class TestSparkfun4x20LCDDisplay(unittest.TestCase):

    @patch('menu.display.sparkfunlcd.QwiicSerlcd')
    def test_display_menu(self, mockLcd):

        display = Sparkfun4x20LCDDisplay(4, 20, 'ascii')
        self.assertEqual(mockLcd.mock_calls, [call(), call().connected.__eq__(False), call().setBacklight(0, 0, 0), call().setContrast(5), call().clearScreen(), call().leftToRight(), call().noCursor()])

        option1 = SelectionOption(id='id1', displayName="option1", )
        option2 = SelectionOption(id='id2', displayName="option2", )
        selectionOptions = [option1, option2]
        menuNode = MenuNode(id='', menuNodeType=None, selectionOptions=selectionOptions, confirm=False, executorNodeId=None, isRoot=False)
        display.display_menu(menuNode, 0)

        self.assertTrue(all(x in mockLcd.mock_calls for x in [call().setCursor(0, 0), call().setCursor(0, 1)]))
        self.assertTrue(all(x in mockLcd.mock_calls for x in [call().print('>1: option1         '), call().print(' 2: option2         ')]))

    @patch('menu.display.sparkfunlcd.QwiicSerlcd')
    def test_display_menu_no_selection_options(self, mockLcd):

        display = Sparkfun4x20LCDDisplay(4, 20, 'ascii')
        self.assertEqual(mockLcd.mock_calls, [call(), call().connected.__eq__(False), call().setBacklight(0, 0, 0), call().setContrast(5), call().clearScreen(), call().leftToRight(), call().noCursor()])

        menuNode = MenuNode(id='', menuNodeType=None, selectionOptions=None, confirm=False, executorNodeId=None, isRoot=False)
        with self.assertRaises(Exception) as ecm:
            display.display_menu(menuNode, 0)

        actualException = ecm.exception
        self.assertEqual(str(actualException), 'Must have selection options to display')

    @patch('menu.display.sparkfunlcd.QwiicSerlcd')
    def test_display_output_no_data(self, mockLcd):

        display = Sparkfun4x20LCDDisplay(4, 20, 'ascii')
        self.assertEqual(mockLcd.mock_calls, [call(), call().connected.__eq__(False), call().setBacklight(0, 0, 0), call().setContrast(5), call().clearScreen(), call().leftToRight(), call().noCursor()])

        display.display_output(None, None)
        self.assertFalse(mockLcd.print.called)

    @patch('menu.display.sparkfunlcd.QwiicSerlcd')
    def test_display_output(self, mockLcd):

        display = Sparkfun4x20LCDDisplay(4, 20, 'ascii')
        self.assertEqual(mockLcd.mock_calls, [call(), call().connected.__eq__(False), call().setBacklight(0, 0, 0), call().setContrast(5), call().clearScreen(), call().leftToRight(), call().noCursor()])

        display.display_output(None, bytearray("Hello World", 'ascii'))

        self.assertTrue(mockLcd.print.called_with('Hello World'))


if __name__ == '__main__':
    unittest.main()

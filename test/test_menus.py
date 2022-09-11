import unittest
from unittest.mock import patch
from parameterized import parameterized

from menu.menus import SelectionOption
from menu.menus import MenuDestination, ExecutorNode, ExecutorNodeType
from menu.menus import Menus, MenuNode, MenuNodeType

class TestSelectionOption(unittest.TestCase):

    def test_as_selection_option(self):
        testId = '12345'
        testDisplayName = 'test display name'
        inputDict = {}
        inputDict['menuNodeId'] = testId
        inputDict['displayName'] = testDisplayName

        selectionOption = SelectionOption.as_selection_option(inputDict)
        self.assertEqual(selectionOption.id, testId)
        self.assertEqual(selectionOption.display_name, testDisplayName)

class TestExecutorNode(unittest.TestCase):

    def test_as_executor_node(self):
        testType = 'method'
        testDestinationOverride = 'lastSelectOptionMenu'
        testId = '12345'
        testName = 'test executor node'
        inputDict = {}
        inputDict['type'] = testType
        inputDict['destinationOverride'] = testDestinationOverride
        inputDict['_id_'] = testId
        inputDict['name'] = testName

        executorNode = ExecutorNode.as_executor_node(inputDict)
        self.assertEqual(executorNode.id, testId)
        self.assertEqual(executorNode.name, testName)
        self.assertEqual(executorNode.executor_type, ExecutorNodeType(testType))
        self.assertEqual(executorNode.destination, MenuDestination(testDestinationOverride))

class TestMenuNode(unittest.TestCase):

    def test_as_menu_node_no_id(self):
        inputDict = {}
        inputDict['random'] = 'random test value'
        asMenuNodeResult = MenuNode.as_menu_node(inputDict)
        self.assertEqual(asMenuNodeResult, inputDict)

    def test_as_menu_node(self):
        testSOId = '12345'
        testSODisplayName = 'so display name'
        testSODict = {}
        testSODict['menuNodeId'] = testSOId
        testSODict['displayName'] = testSODisplayName

        testId = 'ROOT'
        testExecutorNodeId = 'testENId'
        testConfirmValue = True
        testType = 'selection'
        inputDict = {}
        inputDict['_id_'] = testId
        inputDict['selectionOptions'] = [testSODict]
        inputDict['executorNodeId'] = testExecutorNodeId
        inputDict['confirm'] = testConfirmValue
        inputDict['type'] = testType

        menuNode = MenuNode.as_menu_node(inputDict)
        self.assertEqual(menuNode.id, testId)
        self.assertEqual(menuNode.executor_id, testExecutorNodeId)
        self.assertEqual(menuNode.type, MenuNodeType.SELECTION)
        self.assertTrue(menuNode.selection_options is not None)
        self.assertEqual(len(menuNode.selection_options), 1) 
        self.assertTrue(menuNode.is_root)
        self.assertTrue(menuNode.is_confirm)
        self.assertEqual(menuNode.type, MenuNodeType('selection'))

class TestMenu(unittest.TestCase):

    def test_valid_menu_init(self):
        menu = Menus("test/test_input_menunode_files/menunodes_valid_init.json")
        self.assertIsNotNone(menu)

    def test_validate_one_root_node_exception(self):
        with self.assertRaises(Exception) as ecm:
            menu = Menus("test/test_input_menunode_files/menunodes_multiple_root.json")

        actualException = ecm.exception
        self.assertEqual(str(actualException), "Duplicates found")

    def test_validate_selection_options_exception(self):
        with self.assertRaises(Exception) as ecm:
            menu = Menus("test/test_input_menunode_files/menunodes_invalid_selection_id.json")

        actualException = ecm.exception
        self.assertEqual(str(actualException), "Selection Option must have valid menu node id BADID")

    def test_validate_executor_menu_nodes_exception(self):
        with self.assertRaises(Exception) as ecm:
            menu = Menus("test/test_input_menunode_files/menunodes_missing_executor_node_id.json")

        actualException = ecm.exception
        self.assertEqual(str(actualException), "Execution type menu nodes must have an executor node id")

    def test_get_menu_node(self):
        testId = "YUAD5J"
        menus = Menus("test/test_input_menunode_files/menunodes_valid_init.json")
        menuNode = menus.get_menu_node(testId)
        self.assertEqual(menuNode.type, MenuNodeType.EXECUTION)
        self.assertEqual(menuNode.id, testId)
        self.assertEqual(menuNode.executor_id, "ER5KI5")

    def test_get_root_menu_node(self):
        menus = Menus("test/test_input_menunode_files/menunodes_valid_init.json")
        menuNode = menus.get_root_menu_node()
        self.assertTrue(menuNode.is_root)
        self.assertEqual(menuNode.id, 'ROOT')

class TestNavigator(unittest.TestCase):

    def test_home(self):
        pass

    # TODO: all other methods


class TestExecutor(unittest.TestCase):

    def test_register_method(self):
        pass

    def test_execute_method(self):
        pass

    def test_execute_script(self):
        pass
import json
from typing import List, Callable, Dict
from enum import Enum, unique
import subprocess
from subprocess import CalledProcessError
from pathlib import Path

# https://shortunique.id/

def check_for_duplicates(dlist):
    if len(dlist) != len(set(dlist)):
        raise Exception("Duplicates found")

@unique
class MenuNodeSpecialId(Enum):
    ROOT = 'ROOT'
    YES = 'YES'
    NO = 'NO'
    CONFIRMATION = 'CONFIRMATION'
    OUTPUT = 'OUTPUT'

@unique
class MenuDestination(Enum):
    HOME = 'home'
    LAST_SELECT_OPTION_MENU = 'lastSelectOptionMenu'
    CONFIRMATION = 'confirmation'
    POST_EXECUTE_OUTPUT = 'postExecuteOutput'

@unique
class ExecutorNodeType(Enum):
    METHOD = 'method'
    SCRIPT = 'script'

@unique
class MenuNodeType(Enum):
    SELECTION = 'selection'
    EXECUTION = 'execution'
    OUTPUT = 'output'

class SelectionOption(object):
    def __init__(self, id: str, displayName: str):
        self._menuNodeId = id
        self._displayName = displayName

    @property
    def id(self) -> str:
        return self._menuNodeId

    @property
    def display_name(self) -> str:
        return self._displayName

    @staticmethod
    def as_selection_option(dct: Dict):
        return SelectionOption(id=dct['menuNodeId'],displayName=dct['displayName'])


class ExecutorNode(object):
    def __init__(self, id: str, executorNodeType: ExecutorNodeType, name: str, destination: MenuDestination):
        self._executorNodeId = id
        self._executorType = executorNodeType
        self._name = name
        self._destinationOverride = destination # default is to always go home after executing a node

    @property
    def id(self) -> str:
        return self._executorNodeId

    @property
    def executor_type(self) -> ExecutorNodeType:
        return self._executorType

    @property
    def name(self) -> str:
        return self._name

    @property
    def destination(self) -> MenuDestination:
        return self._destinationOverride

    @staticmethod
    def as_executor_node(dct: Dict):
        executorNodeType = ExecutorNodeType(dct['type'])
        destination = MenuDestination(dct['destinationOverride']) if 'destinationOverride' in dct else None
        return ExecutorNode(id=dct['_id_'],executorNodeType=executorNodeType,name=dct['name'],destination=destination)


class MenuNode(object):
    def __init__(self, id: str, menuNodeType: MenuNodeType, selectionOptions: List[SelectionOption], confirm: bool, executorNodeId: str, isRoot: bool):
        self._menuNodeId = id
        self._menuNodeType = menuNodeType
        self._selectionOptions = selectionOptions
        self._executorNodeId = executorNodeId
        self._isRoot = isRoot
        self._isConfirm = confirm

    @property
    def id(self) -> str:
        return self._menuNodeId

    @property
    def type(self) -> MenuNodeType:
        return self._menuNodeType

    @property
    def selection_options(self) -> List[SelectionOption]:
        return self._selectionOptions

    @property
    def executor_id(self) -> str:
        return self._executorNodeId

    @property
    def is_root(self) -> bool:
        return self._isRoot

    @property
    def is_confirm(self) -> bool:
        return self._isConfirm

    @staticmethod
    def as_menu_node(dct: Dict):
        if '_id_' in dct:
            selOptions = [SelectionOption.as_selection_option(selOption) for selOption in dct['selectionOptions']] if 'selectionOptions' in dct else None
            eId = dct['executorNodeId'] if 'executorNodeId' in dct else None
            confirm = dct['confirm'] if 'confirm' in dct else None
            isRoot = True if dct['_id_'] == 'ROOT' else False
            return MenuNode(id=dct['_id_'],menuNodeType=MenuNodeType(dct['type']),selectionOptions=selOptions,confirm=confirm, executorNodeId=eId, isRoot=isRoot)

        return dct


class Menus(object):
    def __init__(self, menu_nodes_filename: str):

        _menunodes_list = self.load_menu_nodes(menu_nodes_filename)

        # validate no duplicate menu node ids
        # also validates one and only one node is the root since the root node is identified by the special id 'ROOT'
        check_for_duplicates([menunode._menuNodeId for menunode in _menunodes_list])

        self._menunodes = {menunode.id : menunode for menunode in _menunodes_list}

        # validate selection options point to valid menu nodes
        self.validate_selection_options(_menunodes_list)

        # validate executor type menu nodes point to valid executors
        self.validate_executor_menu_nodes(_menunodes_list)

        # set root node id
        self._rootNodeId = None
        for menunode in _menunodes_list:
            if menunode.is_root:
                self._rootNodeId = menunode.id

        # root node must always have selection options
        rootNodeSelectionOptions = self.get_root_menu_node().selection_options
        if rootNodeSelectionOptions is None or len(rootNodeSelectionOptions)==0:
            raise Exception("Root menu node must have selection options")

    def get_menu_node(self, menuNodeId: str) -> MenuNode:
        return self._menunodes[menuNodeId]

    def get_root_menu_node(self) -> MenuNode:
        return self._menunodes[self._rootNodeId]

    def load_menu_nodes(self, menu_nodes_filename: str) -> List[MenuNode]:
        with open(menu_nodes_filename, "r") as menunodes_file:
            menunode_data = menunodes_file.read()
            return json.loads(menunode_data, object_hook = MenuNode.as_menu_node)

    def validate_selection_options(self, menunodes: List[MenuNode]):
        for menunode in menunodes:
            if menunode.selection_options is not None:
                for selectionOption in menunode.selection_options:
                    if selectionOption.id not in self._menunodes.keys():
                        raise Exception("Selection Option must have valid menu node id "+selectionOption.id)

    def validate_executor_menu_nodes(self, menunodes: List[MenuNode]):
        for menunode in menunodes:
            if menunode.type == MenuNodeType.EXECUTION:
                executorNodeId = menunode.executor_id
                if executorNodeId is None:
                    raise Exception("Execution type menu nodes must have an executor node id")


class Navigator(object):
    def __init__(self, menus: Menus):
        self._rootMenuNode = menus.get_root_menu_node()
        self._lastSelectOptionMenuNode = self._rootMenuNode
        self._currentMenuNode = self._rootMenuNode
        self._cursorPosition = None
        self._menus = menus

        self.home()

    @property
    def current_menu_node(self) -> MenuNode:
        return self._currentMenuNode

    @property
    def cursor_position(self) -> int:
        return self._cursorPosition

    def home(self):
        self._currentMenuNode=self._rootMenuNode
        self.set_cursor()

    def set_cursor(self):
        self._cursorPosition=None
        self._selectionOptions = self._currentMenuNode.selection_options
        if self._selectionOptions is not None and len(self._selectionOptions)>0:
            self._cursorPosition=0

    def scroll_up(self):
        if self._cursorPosition is not None and self._cursorPosition>0:
            self._cursorPosition-=1

    def scroll_down(self):
        if self._selectionOptions is not None:
            numOptions = len(self._selectionOptions)
            if self._cursorPosition is not None and self._cursorPosition<(numOptions-1):
                self._cursorPosition+=1

    def navigate_to_selected_option(self):
        if self._currentMenuNode.id != MenuNodeSpecialId.CONFIRMATION.value:
            self._lastSelectOptionMenuNode = self._currentMenuNode
        targetMenuId = self._selectionOptions[self._cursorPosition].id
        self._currentMenuNode=self._menus.get_menu_node(targetMenuId)
        self.set_cursor()

    def navigate_to_confirmation_menu(self):
        self._currentMenuNode=self._menus.get_menu_node(MenuNodeSpecialId.CONFIRMATION.value)
        self.set_cursor()

    def navigate_to_last_selection_menu(self):
        self._currentMenuNode = self._lastSelectOptionMenuNode
        self.set_cursor()

    def navigate_to_post_execute_output(self):
        self._currentMenuNode = self._menus.get_menu_node(MenuNodeSpecialId.OUTPUT.value)
        self._cursorPosition = None
        self._selectionOptions = None

class Executor(object):

    class ExecutionResult(object):
        def __init__(self, output: str, returnCode: int, postExecuteMenuDestination: MenuDestination):
            self._output = output
            self._returnCode = returnCode
            self._postExecuteMenuDestination = postExecuteMenuDestination

        @property
        def output(self) -> str:
            return self._output

        @property
        def return_code(self) -> int:
            return self._returnCode

        @property
        def destination(self) -> MenuDestination:
            return self._postExecuteMenuDestination

    def __init__(self, executors_filename: str, scriptsLocation: Path):
        self._methods = {} # mapping of method names to methods
        self._executors_list = self.load_executors(executors_filename)
        self._scriptsLocation = scriptsLocation

        # validate no duplicate executor ids
        check_for_duplicates([executor._executorNodeId for executor in self._executors_list])

        self._executors = {executor.id : executor for executor in self._executors_list}

    def load_executors(self, executors_filename: str) -> List[ExecutorNode]:
        with open(executors_filename, "r") as executornodes_file:
            executornode_data = executornodes_file.read()
            return json.loads(executornode_data, object_hook = ExecutorNode.as_executor_node)

    def register_method(self, method: Callable):
        methodName = method.__name__
        print("SEO: registered methodName: "+str(methodName))
        self._methods[methodName] = method

    def execute(self, executorNodeId: str, **kwargs) -> ExecutionResult:

        executorNode = self._executors[executorNodeId]

        if executorNode.executor_type == ExecutorNodeType.SCRIPT:
            return self._execute_script(executorNode, **kwargs)
        elif executorNode.executor_type == ExecutorNodeType.METHOD:
            return self._execute_method(executorNode, **kwargs)
        else:
            raise Exception("Unsupported execution type")

    def _execute_script(self, executorNode: ExecutorNode, **kwargs) -> ExecutionResult:
        postExecuteMenuDestination = executorNode.destination if executorNode.destination is not None else MenuDestination.HOME
        scriptName = executorNode.name
        scriptToExecute = str((self._scriptsLocation / scriptName).resolve())
        print("executing script: "+scriptToExecute)
        try:
            output = subprocess.check_output([scriptToExecute])
            return Executor.ExecutionResult(output, 0, postExecuteMenuDestination)
        except (CalledProcessError, OSError) as e:
            return Executor.ExecutionResult("Error executing script", 1, MenuDestination.POST_EXECUTE_OUTPUT)

    def _execute_method(self, executorNode: ExecutorNode, **kwargs) -> ExecutionResult:
        postExecuteMenuDestination = executorNode.destination if executorNode.destination is not None else MenuDestination.HOME
        methodName = executorNode.name
        if methodName not in self._methods:
            raise Exception("Method name not registered in executor!")
        method = self._methods[methodName]
        try:
            executionResult = method(**kwargs)
            return Executor.ExecutionResult("Executed method "+methodName, 0, postExecuteMenuDestination) if executionResult is None else executionResult
        except:
            return Executor.ExecutionResult("Error executing method "+methodName, 1, MenuDestination.POST_EXECUTE_OUTPUT)



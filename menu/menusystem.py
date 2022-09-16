from pathlib import Path
from typing import Callable
from queue import Queue

from .displays import Display
from .action.menuaction import MenuAction
from .menus import Menus, Navigator, MenuNodeType, Executor, MenuDestination

class MenuSystem(object):

    def __init__(self,
                 menuNodesFilename: str,\
                 executorNodesFilename: str,\
                 scriptsPath: Path,\
                 display: Display,\
                 actionQueue: Queue,
                 menuAction: MenuAction):

        self._menus = Menus(menuNodesFilename)
        self._navigator = Navigator(self._menus)
        self._display = display
        self._actionQueue = actionQueue
        self._menuAction = menuAction

        self._executor = Executor(executorNodesFilename, scriptsPath)
        self._executor.register_method(self.handle_confirmation_no)
        self._executor.register_method(self.handle_confirmation_yes)

        self._savedExecutorNodeId = None
        self._executionResult = None
        self._action = None


    def register_execution_method(self, method: Callable):
        self._executor.register_method(method)

    @staticmethod
    def handle_confirmation_no(**kwargs) -> Executor.ExecutionResult:
        return None

    @staticmethod
    def handle_confirmation_yes(**kwargs) -> Executor.ExecutionResult:
        try:
            executorNodeId = kwargs['savedExecutorNodeId']
            executor = kwargs['executor']
            print("SEO: savedExecutorNodeId: "+executorNodeId)
            return executor.execute(executorNodeId, **kwargs)
        except KeyError as ex:
            raise Exception("missing required kwargs value: "+ex.args[0])

    def display(self):
        current_node = self._navigator.current_menu_node

        match current_node.type:

            case MenuNodeType.SELECTION:
                cursor_position = self._navigator.cursor_position
                self._display.display_menu(current_node, cursor_position)

            case MenuNodeType.OUTPUT:
                # TODO: do anything with executionResult.returnCode if error?
                output=self._executionResult.output
                self._display.display_output(current_node, output)

    def handle_execution_node(self, executionNode):

        self._executionResult = None

        if executionNode.is_confirm:

            self._savedExecutorNodeId = executionNode.executor_id
            self._navigator.navigate_to_confirmation_menu()

        else:

            self._executionResult = self._executor.execute(executionNode.executor_id, savedExecutorNodeId=self._savedExecutorNodeId, executor=self._executor)
            self._savedExecutorNodeId = None
            destinationMenuNode = self._executionResult.destination

            if destinationMenuNode == MenuDestination.LAST_SELECT_OPTION_MENU:
                self._navigator.navigate_to_last_selection_menu()
            elif destinationMenuNode == MenuDestination.POST_EXECUTE_OUTPUT:
                self._navigator.navigate_to_post_execute_output()
            else:
                self._navigator.home()

    def run(self):

        self._action = MenuAction.Action.NONE
        self.display()

        self._menuAction.start()

        while (self._action != MenuAction.Action.QUIT):

            self._action = self._actionQueue.get(block=True, timeout=None)

            if (self._action != MenuAction.Action.QUIT):
                match self._action:
                    case MenuAction.Action.UP:
                        self._navigator.scroll_up()
                    case MenuAction.Action.DOWN:
                        self._navigator.scroll_down()
                    case MenuAction.Action.SELECT:
                        self._navigator.navigate_to_selected_option()
                    case MenuAction.Action.HOME:
                        self._navigator.home()

                current_node = self._navigator.current_menu_node

                if current_node.type == MenuNodeType.EXECUTION:
                    self.handle_execution_node(current_node)

                self.display()

            self._actionQueue.task_done()
    
        self._menuAction.stop()

    def stop(self):
        # TODO: this doesn't handle the case where the main loop in 'run' is blocked waiting for a actionQueue return
        self._action = MenuAction.Action.QUIT


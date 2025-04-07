import argparse

from src.gui_debugger import GUIDebugger
from src.tui_debugger import TUIDebugger
from src.lldb_interface import LLDBInterface

class Debugger():
    def __init__(self) -> None:
        self.args = self.parse_args()

    def run_debugger(self) -> int:
        if self.args["mode"] == "gui":
            del self.args["mode"]
            gui_debugger = GUIDebugger(self.args)
            return gui_debugger.run()
        elif self.args["mode"] == "tui":
            del self.args["mode"]
            tui_debugger = TUIDebugger(self.args)
            return tui_debugger.run()
        else:
            del self.args["mode"]
            return self.run_default_debugger()

    def parse_args(self) -> list[str]:
        arg_parser = argparse.ArgumentParser()
        
        mode_group = arg_parser.add_mutually_exclusive_group()
        mode_group.add_argument("--gui", action="store_true", help="Use GUI mode")
        mode_group.add_argument("--tui", action="store_true", help="Use TUI mode")

        arg_parser.add_argument("filename", type=str, help="The name of the executable to debug")
        arg_parser.add_argument("executable_args", nargs="*", help="Commandline arguments for the executable to debug")

        raw_args = arg_parser.parse_args()

        args = {}

        if raw_args.tui == True: args["mode"] = "tui"
        elif raw_args.gui == True: args["mode"] = "gui"
        else: args["mode"] = "default"

        args["filename"] = raw_args.filename
        args["exec_args"] = raw_args.executable_args

        return args
    
    def run_default_debugger(self) -> int:
        lldb_interface = LLDBInterface(self.args["filename"], self.args["exec_args"])

        lldb_interface.lldb_init()
        cur_command = None

        while True:
            cur_command = input("(pylldb) ")
            exit = self.validate_exit(cur_command, lldb_interface)

            if exit == 0:
                lldb_interface.close()
                break
            elif exit == 1:
                continue

            command_res = lldb_interface.lldb_run_command(cur_command)
            print(self.process_command_res(command_res))

        print("Exiting...")

        return 0
    
    def validate_exit(self, command: str, lldb_interface: LLDBInterface) -> int:
        if command.lower() != "exit":
            return 2
        
        if lldb_interface.is_running:
            exit_confirmation = input("A process is still running. DO you really want to exit? (Y/n) ")
            if exit_confirmation.lower() == "Y":
                return 0
        
        return 1
    
    def process_command_res(self, command_res: str) -> str:
        pass
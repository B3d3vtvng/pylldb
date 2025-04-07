from src.debugger import Debugger

def main():
    debugger = Debugger()
    debugger_exit_code = debugger.run_debugger()
    return debugger_exit_code

exit_code = main()
exit(exit_code)
class DBError():
    def __init__(self, err_command, err_msg) -> None:
        self.err_command = err_command
        self.err_msg = err_msg

    def __repr__(self) -> str:
        return f"Encountered an error durch execution of command '{self.err_command}': {self.err_msg}"
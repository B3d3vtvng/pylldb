import subprocess
import select
from src.error import DBError

class LLDBInterface():
    def __init__(self, filename: str, args: list[str]) -> None:
        self.filename = filename
        self.args = args
        self.is_running = False
        self.lldb_process = None
        self.error = None

    def lldb_init(self) -> int:
        try:
            self.lldb_process = subprocess.Popen(
                ["lldb"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
        except FileNotFoundError:
            print("Missing required dependency: lldb")
            return 1
        
        self.lldb_run_command("target create " + self.filename)
        if self.error:
            self.error = DBError("target create " + self.filename, "Could not find target")
            return
        
        if len(self.args) != 0:
            self.lldb_run_command("process launch -- " + ' '.join(self.args))

        return

    def lldb_run_command(self, command: str) -> str:
        self.lldb_process.stdin.write(command+"\n")
        self.lldb_process.stdin.flush()
        lldb_output = self.get_lldb_output()
        return lldb_output
        

    def get_lldb_output(self) -> str:
        output = ""
        while True:
            rlist, _, _ = select.select([self.lldb_process.stdout], [], [], 1.0)
            if len(rlist) == 0:
                return output
        
            for stream in rlist:
                output += stream.readline()
        

    def close(self) -> None:
        pass
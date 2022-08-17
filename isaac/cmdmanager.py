import cmd
from gc import callbacks
import sys
import termios
import re


def generatehyphens(s):
    ret = ''
    for _ in range(len(s)):
        ret += '_'
    return ret


def cursorPos():
    if(sys.platform == "win32"):
        OldStdinMode = ctypes.wintypes.DWORD()
        OldStdoutMode = ctypes.wintypes.DWORD()
        kernel32 = ctypes.windll.kernel32
        kernel32.GetConsoleMode(
            kernel32.GetStdHandle(-10), ctypes.byref(OldStdinMode))
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 0)
        kernel32.GetConsoleMode(
            kernel32.GetStdHandle(-11), ctypes.byref(OldStdoutMode))
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    else:
        OldStdinMode = termios.tcgetattr(sys.stdin)
        _ = termios.tcgetattr(sys.stdin)
        _[3] = _[3] & ~(termios.ECHO | termios.ICANON)
        termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, _)
    try:
        _ = ""
        sys.stdout.write("\x1b[6n")
        sys.stdout.flush()
        while not (_ := _ + sys.stdin.read(1)).endswith('R'):
            True
        res = re.match(r".*\[(?P<y>\d*);(?P<x>\d*)R", _)
    finally:
        if(sys.platform == "win32"):
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), OldStdinMode)
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), OldStdoutMode)
        else:
            termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, OldStdinMode)
    if(res):
        return (res.group("x"), res.group("y"))
    return (-1, -1)


class CmdManager(cmd.Cmd):

    def __init__(self, prefix="# :- ", callback=str):
        super().__init__()
        self.prefix = prefix
        self.callback = callback
        self.prompt =  f'{self.prefix}'

    def default(self, line):
        self.callback(line)
        # self.stdout.write(f'{self.callback(line)}\n')

    def emptyline(self):
        self.stdout.write("\033[K")

    def update_prefix(self,prefix):
        self.prefix = prefix
        self.prompt = prefix

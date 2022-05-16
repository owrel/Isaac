import cmd, sys
import termios
import re
import logging
import threading
import time



def generatehyphens(s):
    ret = ''
    for i in range(len(s)):
        ret += '_' 
    return ret



def cursorPos():
    if(sys.platform == "win32"):
        OldStdinMode = ctypes.wintypes.DWORD()
        OldStdoutMode = ctypes.wintypes.DWORD()
        kernel32 = ctypes.windll.kernel32
        kernel32.GetConsoleMode(kernel32.GetStdHandle(-10), ctypes.byref(OldStdinMode))
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 0)
        kernel32.GetConsoleMode(kernel32.GetStdHandle(-11), ctypes.byref(OldStdoutMode))
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
    informationline = 'Information line, to put useless information, or not we\'ll see'
    beforeprompt = '#- '
    prompt = f'\n\n{informationline}\033[F{generatehyphens(informationline)}\033[F{beforeprompt}'
    def default(self, line):
        self.callfunction(line)
        self.stdout.write("\033[K\n\033[K")

    def emptyline(self):
         self.stdout.write("\033[K")

    def update_information(self, line):     
        x,y= cursorPos()
        x = eval(x)
        y = eval(y)
        self.stdout.write('\033[K')
        prompt = f'\n\033[K{line}\033[F\033[K{generatehyphens(line)}\033[F{self.beforeprompt}'
        self.prompt = prompt
        self.stdout.write(prompt + f'\033[{y};{x}H')
    
    def set_callfunction(self,callfunction):
        self.callfunction = callfunction


    def print(self,string):
        self.stdout.write('\033[K' + str(string)+'\n\033[K')

    def postcmd(self, stop, line):


        return stop


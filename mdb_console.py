import os

def clear():
    print(chr(27) + "c", "")

def get_size():
    size = os.get_terminal_size()
    return (size.columns, size.lines)
import os

buffer = []
width = 0
height = 0

def clear():
    print(chr(27) + "c", end="")

def get_size():
    size = os.get_terminal_size()
    return (size.columns, size.lines)

def recreate_buffer():
    global buffer
    global width
    global height

    size = get_size()
    width = size[0]
    height = size[1]
    buffer = [[" " for y in range(height)] for x in range(width)]

def display():
    width = get_size()[0]
    height = get_size()[1]

    for y in range(height):
        for x in range(width):
            print(buffer[x][y], end="", flush=False)
import os

buffer = []
width = 0
height = 0
user_input = None
render = None # Callback to render

def setup(render_callback):
    global render
    render = render_callback

def clear():
    print(chr(27) + "c", end="")

def get_size():
    size = os.get_terminal_size()
    return (size.columns, size.lines - 1) # Remove one so we can have a line for input

def recreate_buffer():
    global buffer
    global width
    global height

    size = get_size()
    width = size[0]
    height = size[1]
    buffer = [[" " for y in range(height)] for x in range(width)]

def display():
    global user_input

    # Clear the screen and render the buffer
    clear()
    recreate_buffer()
    render()

    # Draw the buffer
    for y in range(height):
        for x in range(width):
            print(buffer[x][y], end="", flush=False)

        # Newline
        # Even though the buffer will overflow to the next line normally,
        # the console can be resized which will affect how it overflows
        print("", flush=False)
    
    # Flush the buffer and print a cursor so the user can give input
    print(" > ", end="", flush=True)
    user_input = input()
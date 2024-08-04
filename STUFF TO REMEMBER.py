import time
import os

# Makes it work for windows 10, apparently it enables ANSI sequences
if os.name == 'nt':
    os.system('cls')

# Clear console
print("SUSSY")
time.sleep(1)
print(chr(27) + 'c', end="")
time.sleep(1)
print("AMOGUS")

# Get console size
print(os.get_terminal_size())

# TODO: on terminal resize, update the UI
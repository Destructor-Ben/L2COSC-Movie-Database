import mdb_console as console

def render():
    if (console.user_input == "exit"):
        return False

    for x in range(console.width):
        console.buffer[x][0] = "-"
        console.buffer[x][-1] = "-"

    for y in range(console.height):
        console.buffer[0][y] = "|"
        console.buffer[-1][y] = "|"

    console.buffer[0][0] = "+"
    console.buffer[-1][0] = "+"
    console.buffer[0][-1] = "+"
    console.buffer[-1][-1] = "+"

    console.bg_colours[0][0] = (255, 0, 0)
    console.fg_colours[1][0] = (0, 255, 0)

    return True

console.setup(render)
console.run()

import mdb_console as console
import time

console.clear()
print(console.get_size())

time.sleep(1)

console.clear()
console.recreate_buffer()
# Rendering goes here
console.buffer[0][0] = "a"
console.display()

time.sleep(2)

console.clear()
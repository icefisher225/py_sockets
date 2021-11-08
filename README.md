# py_sockets
A library to build off later, to make socket programming faster in python


## Dependencies
Builtins: socket, time, os, sys, subprocess, threading

Packages: strictly, caoe


## Sample code
```python
from client_socketlib import ClientSocket

ip = "10.0.1.200"
port = 12345

socket = ClientSocket(ip, port)
# socket = ClientSocket("10.0.1.200", 12345)

error = socket.connect()

if error[0] == 1:
    '''
    Checks if there was an error in making the connection, returns if so.
    '''
    print(error[1])
    return 0
time.sleep(.1)

socket.send("Hello, World!")

time.sleep(2)

print(socket.recv())
```

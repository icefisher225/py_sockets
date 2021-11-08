# py_sockets
A library to build off later. Hopefully it makes socket-level python programming faster.


## Dependencies
Builtins: socket, time, os, sys, subprocess, threading

Packages: strictly, caoe

## Sample Code

### Server:

```python

import multiprocessing as mp
from server_socketlib import ServerSocket, ServerCommSocket, get_connection

def run(commsock, q):
    commsock.send(f"host attached = {commsock.ip}")
    print(commsock.recv())
    return 0


def main():
    ip = "localhost"
    port = 12345
    queue = mp.Queue()
    server_socket = ServerSocket(ip, port, queue)

    process_list = list()

    while True:
        communication_socket = get_connection(server_socket)
        if communication_socket.error != None:
            print(f"error: {communication_socket.msg}")
            break #or continue, if you want to ignore errors
        else:
            clientprocess = mp.Process(target = run, args(commsock, q, ))
            clientprocess.start()
            process_list.append(clientprocess)

    for process in process_list:
        wait(process)
    return 0

if __name__ == __"main__":
    main()
```

### Client:

```python
from client_socketlib import ClientSocket

ip = "10.0.1.200"
port = 12345

socket = ClientSocket(ip, port)
# socket = ClientSocket("10.0.1.200", 12345)

if socket.connect()[1] == 1:
    # Checks if there was an error in making the connection, returns if so.
    print(error[1])
    return 0

time.sleep(.1)

socket.send("Hello, World!")

time.sleep(2)

print(socket.recv())
```

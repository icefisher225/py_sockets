# py_sockets
A library to build off later. Hopefully it makes socket-level python programming faster.


## Dependencies
Builtins: socket

Packages: strictly (possibly to be removed in future update), caoe (thread orphanage prevention)

Helpful modules for using this library: multiprocessing, time, threading

## Sample Code

### Server:

```python

import multiprocessing as mp
from server_socketlib import ServerSocket, ServerCommSocket, ExitCode, get_connection

def run(commsock, queue):
    commsock.send(f"host attached = {commsock.ip}")
    check = (data := commsock.recv()).split(" ")[0]
    if check == "exit" or check == "quit":
        queue.put(ExitCode())
    print(data)
    return 0


def main():
    ip = "localhost"
    port = 12345
    queue = mp.Queue()
    # This is used for interprocess communication, as needed.
    server_socket = ServerSocket(ip, port, queue)

    process_list = list()

    while True:
        communication_socket = get_connection(server_socket)
        if communication_socket.error != None:
            # If the client sends in "ExitCode"
            print(f"error: {communication_socket.msg}")
            break #If this is removed, the serversocket can never be told to exit from the client and will need to be exited directly.
        else:
            clientprocess = mp.Process(target = run, args(commsock, queue, ))
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

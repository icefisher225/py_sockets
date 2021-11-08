# py_sockets
This is a library to make error-handled socket programming faster and easier.<br><br>Written for Python 3.9.x.


## Dependencies
#### Builtins:
  * socket


#### Packages:
  * strictly (possibly to be removed in future update)
  * caoe (thread orphanage prevention)

```bash
python3 -m pip install strictly
python3 -m pip install caoe
```

#### Helpful modules for using this library:
  * multiprocessing (server-side only)
  * time
  * threading



## Sample Code

### Server:

```python
import multiprocessing as mp #used to allow multiple concurrent client connections.
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
    process_list = list()
    comqueue = mp.Queue()
    # This is used for communication back to main loop ONLY

    server_socket = ServerSocket(ip, port, comqueue)    

    while True:
        communication_socket = get_connection(server_socket, num=15, timeout=60)
        if communication_socket.error == None:
            clientprocess = mp.Process(target = run, args(commsock, comqueue, ))
            clientprocess.start()
            process_list.append(clientprocess)
        else:
            print(f"error: {communication_socket.msg}")
            break
            #If this is removed, the serversocket can never be told to
            # exit from the client and will need to be exited locally.

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

if socket.connect() == 1:
    print(socket.error())
    return 1

socket.send("Hello, World!")

time.sleep(2)

print(socket.recv())
```

import time
from strictly import *

importfailure = False

try:
    from client_socketlib import ClientSocket
except ModuleNotFoundError as e:
    raise e
    importfailure=True


def main():
    assert importfailure == False, "Import failed. Exiting..."

    ip = "localhost"
    port = 12345
    sock = ClientSocket(ip, port)
    err = sock.connect()
    print(err)
    if err[0] == 1:
        print(err[1])
        return 0
    time.sleep(.1)
    # print(sock.recv())
    sock.send("UwU world~~")

    # Needs threading, one to run event loop, another to send,
    # a third to recieve



if __name__ == "__main__":
    main()

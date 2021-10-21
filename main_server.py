import time
import math
import multiprocessing as mp
import queue

import caoe
caoe.install()

importfailure = False

try:
    from server_socketlib import ServerSocket, ServerCommSocket, get_connection
except ModuleNotFoundError as e:
    raise e
    importfailure=True



def run(commsock):
    commsock.send(1)
    print(commsock.recv())



def main():
    if importfailure == True:
        print("Import failure")
        return 1
    ip = "localhost"
    port = 12345
    q = mp.Queue()
    sock = ServerSocket(ip, port, q)
    while True:
        commsock = get_connection(sock)
        if commsock.error != 0:
            print(f"{commsock.msg}")
            return 1
        else:
            proc = mp.Process(target=run, args=(commsock, None, ))



if __name__ == "__main__":
    main()

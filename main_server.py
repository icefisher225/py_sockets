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



def run(commsock, q):
    # commsock.send(f"host = {commsock.ip}")
    print("entered run function")
    print(commsock.recv())
    return 0

    # This needs to run three threads, one to event loop (?),
    # one to send data, and a third to recieve.



def main():
    if importfailure == True:
        print("Import failure")
        return 1
    ip = "localhost"
    port = 12345
    q = mp.Queue()
    procs = list()
    sock = ServerSocket(ip, port, q)
    while True:
        commsock = get_connection(sock)
        if commsock.error != None:
            print(f"error: {commsock.msg}")
            return 1
        else:
            proc = mp.Process(target=run, args=(commsock, q, ))
            proc.start()
            procs.append(proc)

    for proc in procs:
        wait(proc)
    return 0

if __name__ == "__main__":
    main()

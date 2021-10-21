import time
import os
import sys
import subprocess
import threading
from strictly import *

importfailure = False

try:
    from client_socketlib import ClientSocket
except ModuleNotFoundError as e:
    raise e
    importfailure=True




def main():
    if importfailure == True:
        print("Import failure")
        return 1

    ip = "localhost"
    port = 12345
    sock = ClientSocket(ip, port)



if __name__ = "__main__":
    main()

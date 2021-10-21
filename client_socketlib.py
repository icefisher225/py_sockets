import socket
import time
import os
import sys
import subprocess
import threading
from strictly import *
import caoe

caoe.install()

class Socketer:
    def __init__(self, sock=None):
        if sock is None:
            self._sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self._sock=sock

    def __enter__(self):
        # take no action on context enter
        return self

    def __exit__(self, *_):
        self._sock.shutdown(socket.SHUT_RDWR)
        self._sock.close()
        self._sock = None


class ClientSocket(Socketer):
    def __init__(self, clientsock=None, ip="0.0.0.0", port=9999, error=None, msg=None):
        super().__init__()
        self.clientsock =  self._sock if (clientsock is None) else clientsock
        self.ip = ip
        self.port = port
        self.error = error
        self.msg = msg

    @property
    def sock(self):
        return self._sock

    @strictly
    def connect(self) -> tuple:
        try:
            self.clientsock.connect(ip, port)
        except Exception as e:
            return (1, e)
        return (0, )

    @strictly
    def send(self, srcmsg:str) -> None:
        msg = orig_msg = _str_to_msgbytes(srcmsg)

        tot=len(msg)
        cur=0 # current amout of message that has been sent (bytes)
        while len(msg):
            self.clientsock.send(msg[0:CHUNK])
            msg=msg[CHUNK:]
        print("Message Sent")


@strictly
def _str_to_msgbytes(src: str) -> bytes:
    body = bytes(src, 'utf-8')
    bodylen = org_bodylen = len(body)

    # split the bodylen into four bytes and put it on the front of body
    fmtd_len = bytes()
    for _ in range(4):
        fmtd_len = bytes([(bodylen & 0xff)]) + fmtd_len
        bodylen = bodylen >> 8
    else:
        if bodylen != 0:
            raise ValueError(f"message too long to send, cannot send data longer than {0xffffffff}, got {orig_bodylen}")

    return fmtd_len+b'\n'+body


@strictly
def message_len(sock) -> int:
    msg_len = 0
    for _ in range(4): msg_len = (msg_len << 8) + sock.recv(1)[0]
    sock.recv(1) #this throws away the delimiter
    return msg_len

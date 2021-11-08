import socket
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
    def __init__(self, ip="0.0.0.0", port=9999, **kwargs):
        super().__init__()
        self.clientsock = kwargs.get("clientsock") if ("clientsock" in kwargs) else self._sock
        self.ip = ip
        self.port = port
        self.error = kwargs.get("error") if ("error" in kwargs) else None
        self.msg = kwargs.get("msg") if ("msg" in kwargs) else None

    @property
    def sock(self):
        return self._sock

    @strictly
    def connect(self) -> tuple:
        try:
            self.clientsock.connect((self.ip, self.port))
        except Exception as e:
            return (1, e)
        return (0, )

    @strictly
    def send(self, srcmsg:str) -> None:
        CHUNK = 2048
        msg = orig_msg = _str_to_msgbytes(srcmsg)

        tot=len(msg)
        cur=0 # current amout of message that has been sent (bytes)
        while len(msg):
            self.clientsock.send(msg[0:CHUNK])
            msg=msg[CHUNK:]
        print(f"{srcmsg} -> {orig_msg} sent")


    @strictly
    def recv(self) -> str:
        while True:
            try:
                msglen = _message_len(self._sock)
            except:
                raise Exception(f"Incorrect data recived, exiting")
                return 1
            cur = 0
            data = bytes()
            while cur<msglen:
                data += self._sock.recv(2048)
                cur = len(data)
            data.decode()
            return data


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
    print(body)
    return fmtd_len+b'\n'+body


@strictly
def message_len(sock) -> int:
    msg_len = 0
    for _ in range(4): msg_len = (msg_len << 8) + sock.recv(1)[0]
    sock.recv(1) #this throws away the delimiter
    return msg_len

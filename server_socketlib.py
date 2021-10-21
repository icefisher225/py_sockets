from strictly import *
import socket
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


class ServerSocket(Socketer):
    def __init__(self, ip, port, q):
        self.ip = ip
        self.port = port
        self.q = q
        self.listening = False
        super().__init__()
        self._sock.settimeout(60)


    @property
    def servsock(self):
        return self._sock

    @strictly
    def _set_timeout(self, time) -> None:
        self._sock.settimeout(time)


    @property
    def get_lsn(self):
        """
        :return: value of self.listening
        """
        return self.listening

    @property
    def set_lsn(self):
        """
        :return: True if listening, False if not
        """
        if self.listening == True:
            return True
        self.listening = True
        return False


class ServerCommSocket():
    def __init__(self, clientsock, ip="0.0.0.0", error=None, msg=None):
        self._sock = clientsock
        self.ip = ip
        self.error = error
        self.msg = msg

    def __enter__(self):
        # take no action on context enter
        return self

    def __exit__(self, *_):
        self._sock.shutdown(socket.SHUT_RDWR)
        self._sock.close()
        self._sock = None

    @strictly
    def send(self, srcmsg:str) -> None:
        msg = orig_msg = _str_to_msgbytes(srcmsg)

        tot=len(msg)
        cur=0 # current amout of message that has been sent (bytes)
        while len(msg):
            self._sock.send(msg[0:CHUNK])
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
def _message_len(sock) -> int:
    msg_len = 0
    for _ in range(4): msg_len = (msg_len << 8) + sock.recv(1)[0]
    sock.recv(1) #this throws away the delimiter
    return msg_len

@strictly
def _accept(serversock) -> ServerCommSocket:
    '''
    private function
    '''
    try:
        (clientsock, addr) = serversock._sock.accept()
    except Exception as e:
        return _error_sock(f"Exception caught: {e}")
    return ServerCommSocket(clientsock, address)

@strictly
def _bind(serversock) -> None:
    serversock._sock.bind((serversock.ip, serversock.port))

@strictly
def _listen(serversock, num) -> None:
    serversock._sock.listen(num)

@strictly
def _error_sock(msg=None) -> ServerCommSocket:
    return ServerCommSocket(None, None, 1, msg)

@strictly
def get_connection(serversock, num = 10) -> ServerCommSocket:
    '''
    Call this function with args passed to get client connection from ServerSocket
    :serversock: serversocket
    :num: (optional) number of client connections to buffer.
          for one connection only, set to 0.
          default is 10.
          Only used on first call of this function
    :return: ClientSocket object bound to first requested connection
             ClientSocket object with error state (clientsocket.error set to 1)
    '''
    if serversock.listening == False:
        _bind(serversock)
        _listen(serversock, num)
        serversock.listening = True
    serversock._set_timeout(10) # If more than 10 seconds of waiting for new connection, throws error
    try:
        res = _accept(serversock)
    except socket.timeout:
        return _error_sock(f"Socket Timeout Error")
    return res

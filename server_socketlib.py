from strictly import *
import socket
import caoe
import queue

caoe.install()


class ExitCode:
    #this is partially a stub
    def __init__(self):
        self._code = 1

    @property
    def ecode(self):
        return self._code



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
        self._sock.settimeout(1)


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
            return
        self.listening = True


class ServerCommSocket():
    def __init__(self, clientsock, ip="0.0.0.0", port=9999, **kwargs):
        self._sock = clientsock
        self.ip = ip
        self.port = port
        self.error = kwargs.get("error") if ("error" in kwargs) else None
        self.msg = kwargs.get("msg") if ("msg" in kwargs) else None
        self._sock.set_inheritable(True)

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
    def recv(self) -> str:
        while True:
            try:
                msglen = _message_len(self._sock)
            except:
                raise Exception("Incorrect data recived, exiting")
                return 1
            cur = 0
            data = bytes()
            while cur<msglen:
                data += self._sock.recv(2048)
                cur = len(data)
            data.decode()
            return data.decode()

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
    if clientsock.get_inheritable() == False:
        clientsock.set_inheritable(True)
    return ServerCommSocket(clientsock, addr[0], addr[1])

@strictly
def _bind(serversock) -> None:
    serversock._sock.bind((serversock.ip, serversock.port))

@strictly
def _listen(serversock, num) -> None:
    serversock._sock.listen(num)

@strictly
def _error_sock(msge=None) -> ServerCommSocket:
    return ServerCommSocket(None, error=1, msg=msge)

@strictly
def get_connection(serversock, **kwargs) -> ServerCommSocket:
    '''
    Call this function with args passed to get client connection from ServerSocket
    :serversock: ServerSocket
    :num=<int>: (optional) number of client connections to buffer.
        For one connection only, set to 0.
        Default: 10.
        Only used on first call of this function.
    :timeout=<int>: (optional) time (seconds) to wait before shutting down
        server-side socket if no connections are made.
        Default: 120 seconds
        Pass -1 for infinite time (running as a service).
    :return: ClientSocket object bound to first requested connection
        ClientSocket object with error state (clientsocket.error set to 1)
    '''
    num = kwargs.get("num") if ("num" in kwargs) else 10
    if serversock.get_lsn == False:
        _bind(serversock)
        print(f"Serversocket bound")
        _listen(serversock, num)
        print(f"Serversocket listening for {num} connections")
        serversock.set_lsn
        print(f"socket is listening: {serversock.get_lsn}")

    serversock._set_timeout(1)
    count = kwargs.get("timeout") if ("timeout" in kwargs) else 120

    iter = 0
    while True:
        try:
            conn = _accept(serversock)
            print("accepted connection")
            return conn
        except socket.timeout: #this happens once a second, on timeout
            try:
                code = serversock.q.get()
                if type(code) == ExitCode: #only hits if queue is not empty
                    return _error_sock(f"Exitcode sent from client")
                else:
                    raise queue.Empty() # used to hit exception, this is temporary
            except queue.Empty:
                if count == -1:
                    continue #loop with infinite timeout
                elif iter > count:
                    return _error_sock(f"Socket Timeout Error")
                else:
                    iter += 1
                    continue #loop with integer timeout

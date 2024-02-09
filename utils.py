from random import randrange
from hashlib import sha256
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import socket
from typing import Tuple

HEADER_SIZE = 10

class DiffieHellman:

    def __init__(self, header_size = 10):
        self.HEADER_SIZE = header_size
        self.p = 179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624225795083
        self.g = randrange(2, self.p)
        self.secret = randrange(2, self.p - 1)

    def shareParams(self)-> bytes:
        g = long_to_bytes(self.g)
        h1 = f'{hex(len(g))[2:]:>0{self.HEADER_SIZE}}'.encode()
        p = long_to_bytes(self.p)
        h2 = f'{hex(len(p))[2:]:>0{self.HEADER_SIZE}}'.encode()
        params = h1 + g + h2 + p
        return params

    def recvParams(self, pk: bytes)-> None:
        h1 = int(pk[:self.HEADER_SIZE].decode(), 16)
        pk = pk[self.HEADER_SIZE:]
        self.g = bytes_to_long(pk[:h1])
        pk = pk[h1:]
        h2 = int(pk[:self.HEADER_SIZE].decode(), 16)
        pk = pk[self.HEADER_SIZE:]
        self.p = bytes_to_long(pk[:h2])

    def sharePubKey(self)-> bytes:
        pubkey = long_to_bytes(pow(self.g, self.secret, self.p))
        h = f'{hex(len(pubkey))[2:]:>0{self.HEADER_SIZE}}'.encode()
        pk = h + pubkey
        return pk

    def recvPubKey(self, pk: bytes)-> None:
        h = int(pk[:self.HEADER_SIZE].decode(), 16)
        pk = pk[self.HEADER_SIZE:]
        self.key = bytes_to_long(pk[:h])
        self.key = pow(self.key, self.secret, self.p)

    def getAESKey(self)-> Tuple[bytes, bytes]:
        key = long_to_bytes(self.key)
        key = sha256(key).digest()
        return AES.new(
            key[:AES.block_size],
            AES.MODE_CBC,
            key[-AES.block_size:]
        )

def server_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)
    return s

def send_data(c :socket.socket, data: bytes):
    header = f'{hex(len(data))[2:]:>0{HEADER_SIZE}}'.encode()
    data = header + data
    c.send(data)

def recv_data(c: socket.socket):
    header = c.recv(HEADER_SIZE)
    if len(header) == 0:
        raise socket.error
    data = c.recv(int(header.decode(), 16))
    return data

def communicate(c: socket.socket, aes, data: bytes=None):
    if isinstance(data, type(None)):
        data = recv_data(c)
        data = unpad(aes.decrypt(data), AES.block_size)
        print("Encrypted Message : ",data)
        return data
    else:
        data = aes.encrypt(pad(data, AES.block_size))
        print("Encrypted Message : ",data)
        send_data(c, data)

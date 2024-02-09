from utils import *
from time import sleep
import serial 
import os 
import time

# serial_port= serial.Serial(port='COM6',baudrate=9600,timeout=2)
serial_port= serial.Serial(port='COM6',baudrate=9600,timeout=2)
serial_port.close()
serial_port.open()

def on_new_connect(c):
    dh = DiffieHellman()
    send_data(c, dh.shareParams())
    print('\nShared DH parameters')
    dh.recvPubKey(recv_data(c))
    print('Received DH public key')
    send_data(c, dh.sharePubKey())
    print('Shared DH public key\n')
    return dh.getAESKey()

def communicate(c, aes, data: bytes=None):
    if isinstance(data, type(None)):
        data = recv_data(c)
        data = unpad(aes.decrypt(data), AES.block_size)
        return data
    else:
        data = aes.encrypt(pad(data, AES.block_size))
        send_data(c, data)

def main():
    print('Server Connected')
    server_sock = server_socket('localhost', 3000)
    client_sock, _ = server_sock.accept()
    aes = on_new_connect(client_sock)
    
    while True:
        
        msg= serial_port.readline().decode('ascii')
        communicate(client_sock, aes, msg.encode())
        # print(msg.encode())
        print(f'Sent: {msg}')
        sleep(1) 

    client_sock.close()
    server_sock.close()

if __name__ == '__main__':
    main()

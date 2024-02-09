from utils import *
import random
import decimal


def man_in_the_middle(s, c):
    server_dh = DiffieHellman()
    client_dh = DiffieHellman()
    server_dh.recvParams(recv_data(s))
    print('\nReceived DH parameters from server')
    client_dh.recvParams(server_dh.shareParams())
    send_data(c, client_dh.shareParams())
    print('Shared DH parameter to client')
    client_dh.recvPubKey(recv_data(c))
    print('Received DH public key from client')
    send_data(s, server_dh.sharePubKey())
    print('Shared DH public key to server')
    server_dh.recvPubKey(recv_data(s))
    print('Received DH public key from server')
    send_data(c, client_dh.sharePubKey())
    print('Shared DH public key to client\n')
    return server_dh.getAESKey(), client_dh.getAESKey()

def modify(msg: str):
    if open('flags.txt', 'r').read().strip() == '1':
        msg = str(float(decimal.Decimal(random.randrange(0,1000))/100))
    return msg

def main():
  
    listen_sock = server_socket('localhost', 4000)
    client_sock, _ = listen_sock.accept()
    s = socket.socket()
    s.connect(('localhost', 3000))

    server_aes, client_aes = man_in_the_middle(s, client_sock)

    try:
        while True:

            msg = communicate(s, server_aes).decode()
            print(f'Received from server: {msg}')
            msg = modify(msg)
            communicate(client_sock, client_aes, msg.encode())
            print(f'Sent to client: {msg}')          
    except socket.error:
        pass
    except Exception as e:
        print(str(e))

    client_sock.close()
    s.close()

if __name__ == '__main__':
    main()

from utils import *

def on_new_connect(s):
    dh = DiffieHellman()
    dh.recvParams(recv_data(s))
    print('\nReceived DH parameters')
    send_data(s, dh.sharePubKey())
    print('Shared DH public key')
    dh.recvPubKey(recv_data(s))
    print('Received DH key\n')
    return dh.getAESKey()

def main():

    s = socket.socket()
    s.connect(('localhost', 4000))
    aes = on_new_connect(s)   

    try:
        while True:
            msg = communicate(s, aes)
            # print(msg)
            msg = communicate(s, aes).decode()
            print(f'Received: {msg}')

    except socket.error:
        pass
    except Exception as e:
        print(str(e))

    s.close()

if __name__ == '__main__':
    main()

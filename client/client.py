import socket
import time

def main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #s.bind(("127.0.0.1", 10400))

    s.connect(("127.0.0.1", 35891))


    while True:
        data = input(">")
        s.send(data.encode())
        dataFromClient = s.recv(4096)

        print(dataFromClient.decode())






main()
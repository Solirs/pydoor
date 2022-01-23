import socket
import time

def main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(("127.0.0.1", 10555))

    s.connect(("127.0.0.1", 35891))


    while True:
        data = input(">")
        s.send(data.encode())






main()
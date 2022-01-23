import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("127.0.0.1", 35891))

data = "Hey"

s.send(data.encode())
import socket
import time
import sys

localHost = "127.0.0.1"
PORT = 1887
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((localHost, PORT))


serverQuestion =  client.recv(1024)#have name?
print(serverQuestion.decode())
myName = input("".join(("Name:")))
client.sendall(bytes(myName,'UTF-8'))

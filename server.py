import socket
import threading
import random
import sys

LOCALHOST = "127.0.0.1"
PORT = 1887
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("[ SERVER ] Let's go")
print("[ SERVER ] Waiting for client's requests ...")


class ClientIdentity:
    def __init__(self,sockCl,nameCl,preferenceCl):
        self.sockCl = sockCl
        self.name = nameCl.upper()
        self.preference = preferenceCl
        self.score = []

class Thread(threading.Thread):
    def __init__(self,clientAdr,sockCl):
        threading.Thread.__init__(self)
        self.sockCl = sockCl
        print ("[ SERVER ] New connection created : ", clientAdr)

    def run(self):
        #ask name
        self.sockCl.send(bytes("[ SERVER ] Hi, What's your name ?",'UTF-8'))
        recvName = self.sockCl.recv(2048)
        clientNichName = recvName.decode()
        print ("[ CLIENT ] My name is ",clientNichName)


while True:  
    server.listen(1)
    acceptClient = server.accept()
    socketCl = acceptClient[0]
    clientAdr = acceptClient[1]
    thread = Thread(clientAdr, socketCl)
    thread.start()

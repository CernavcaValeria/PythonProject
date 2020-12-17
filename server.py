import socket
import threading
import random
import sys
import clientIdentityClass

LOCALHOST = "127.0.0.1"
PORT = 1887
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("[ SERVER ] Let's go")
print("[ SERVER ] Waiting for client's requests ...")

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
        preference = 'none'
        clientIdentity = clientIdentityClass.ClientIdentity(self.sockCl,clientNichName,preference)
        
        #ask preference
        self.sockCl.send(bytes("[ SERVER ] Do you want to play with a friend? y/n",'UTF-8'))
        recvPreference = self.sockCl.recv(2048)
        recvPrefere = recvPreference.decode()
        if recvPrefere=='y':
            print ("[",clientNichName,"] I want to play with a friend! ")
            clientIdentity.preference = 'multiPlayer'
        elif recvPrefere=='n':
            print ("[",clientNichName.upper(),"] I want to play with server! ")
            clientIdentity.preference = 'onePlayer'

while True:  
    server.listen(1)
    acceptClient = server.accept()
    socketCl = acceptClient[0]
    clientAdr = acceptClient[1]
    thread = Thread(clientAdr, socketCl)
    thread.start()

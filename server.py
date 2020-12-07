import socket
import threading
import random

LOCALHOST = "127.0.0.1"
PORT = 1886
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("[ SERVER ] Start")
print("[ SERVER ] Waiting for clients requests ...")


def declareWinner(Players,p1Attmps,p2Attmps):
    player1Score = int(50-(2*p1Attmps))
    player2Score = int(50-(2*p2Attmps))
    if player1Score<player2Score:
        msg1 = "".join(('[ SERVER ] Your opponent ', Players[1].name ,' won with ', str(player2Score) , ' points VS you ', str(player1Score),' points'))
        msg2 = "".join(('[ SERVER ] You won with ', str(player2Score),' points VS ', Players[0].name , ' with ', str(player1Score) ,' points'))
        Players[0].sockCl.send(bytes(msg1,'UTF-8'))
        Players[1].sockCl.send(bytes(msg2,'UTF-8'))
    elif player1Score>player2Score:
        msg1 = "".join(('[ SERVER ] Your opponent ', Players[0].name ,' won with ', str(player1Score) , ' p VS you ', str(player2Score),' points'))
        msg2 = "".join(('[ SERVER ] You won with ', str(player1Score),' points VS ', Players[1].name , ' with ', str(player2Score) ,' points'))
        Players[0].sockCl.send(bytes(msg2,'UTF-8'))
        Players[1].sockCl.send(bytes(msg1,'UTF-8'))
    elif player1Score==player2Score:
        msg1 = "".join(('[ SERVER ] Equality ! Score : ',str(player1Score),' points'))
        msg2 = "".join(('[ SERVER ] Equality ! Score : ',str(player2Score),' points'))
        Players[0].sockCl.send(bytes(msg1,'UTF-8'))
        Players[1].sockCl.send(bytes(msg2,'UTF-8'))
    print("[ SERVER ] The results were transmitted successfully !")


sessionMultiPLayers = 1
sessionTwoPlayers = []
numberOfPlayers = 0

def gameServerTwoClients():
    global numberOfPlayers
    numberOfPlayers = numberOfPlayers + 1
    currentNrOfPlayer = len(sessionTwoPlayers)
    indexPlayer1 =  numberOfPlayers-1

    if currentNrOfPlayer%2==1:
        print("[ SERVER ] Waiting opponent player for",sessionTwoPlayers[indexPlayer1].name )
        sessionTwoPlayers[indexPlayer1].sockCl.send(bytes("1",'UTF-8'))

    elif currentNrOfPlayer%2==0:
        indexPlayer1 = numberOfPlayers-2
        indexPlayer2 = numberOfPlayers-1
        sessionTwoPlayers[indexPlayer1].sockCl.send(bytes("[ SERVER ] Start Game ...",'UTF-8'))
        sessionTwoPlayers[indexPlayer2].sockCl.send(bytes("[ SERVER ] Start Game ...",'UTF-8'))

        print("\n~ Start GAME between :",sessionTwoPlayers[0].name , "and", sessionTwoPlayers[1].name," ~")
        readyP1 = sessionTwoPlayers[indexPlayer1].sockCl.recv(2048)
        readyP2 = sessionTwoPlayers[indexPlayer2].sockCl.recv(2048)
        print(readyP1.decode())


        #Player1 give the Number- Player2 Guess the number
        sessionTwoPlayers[indexPlayer1].sockCl.send(bytes("[ SERVER ] Give me an number between [0,50 ]: __",'UTF-8'))
        numberForPlayer2 = sessionTwoPlayers[indexPlayer1].sockCl.recv(2048)
        numberForPL2 = int(numberForPlayer2.decode())
        print("[",sessionTwoPlayers[indexPlayer1].name,"] I give the number : " ,numberForPL2 )

        sessionTwoPlayers[indexPlayer2].sockCl.send(bytes("[ SERVER ] Guess the number : __",'UTF-8'))
        Player2Guess = sessionTwoPlayers[indexPlayer2].sockCl.recv(2048)
        numberP2HaveToGuess = int(Player2Guess.decode())
        print("[",sessionTwoPlayers[indexPlayer2].name,"] I guess : " ,numberP2HaveToGuess )

        player2Attepmts = 0
        while True:
            player2Attepmts = player2Attepmts + 1
            if numberP2HaveToGuess<numberForPL2:
                sessionTwoPlayers[indexPlayer2].sockCl.send(bytes("[ SERVER ] Wrong! The number is bigger. Try Again",'UTF-8'))
            
            if numberP2HaveToGuess>numberForPL2:
                sessionTwoPlayers[indexPlayer2].sockCl.send(bytes("[ SERVER ] Wrong! The number is smaller. Try Again",'UTF-8'))
            
            if numberP2HaveToGuess==numberForPL2:
                sessionTwoPlayers[indexPlayer2].sockCl.send(bytes("ok",'UTF-8'))
                sessionTwoPlayers[indexPlayer1].sockCl.send(bytes(str(player2Attepmts),'UTF-8'))                
                print("[ SERVER ] PLayer",sessionTwoPlayers[1].name,"guessd the number in",str(player2Attepmts),"attempts")
                break

            player2think = sessionTwoPlayers[indexPlayer2].sockCl.recv(2048)
            num = int(player2think.decode())
            print("[",sessionTwoPlayers[indexPlayer2].name,"] I guess : " ,num)
            numberP2HaveToGuess = num



        #Player2 give the Number- Player1 Guess the number
        ready1P1 = sessionTwoPlayers[indexPlayer1].sockCl.recv(2048)
        ready1P2 = sessionTwoPlayers[indexPlayer2].sockCl.recv(2048)
        print(ready1P1.decode())

        sessionTwoPlayers[indexPlayer2].sockCl.send(bytes("[ SERVER ] Give me an number between [0,50] : __",'UTF-8'))
        numberForPlayer1 = sessionTwoPlayers[indexPlayer2].sockCl.recv(2048)
        numberForPL1 = int(numberForPlayer1.decode())
        print("[",sessionTwoPlayers[indexPlayer2].name,"] I give the number : " ,numberForPL1 )

        sessionTwoPlayers[indexPlayer1].sockCl.send(bytes("[ SERVER ] Guess the number : __",'UTF-8'))
        Player1Guess = sessionTwoPlayers[indexPlayer1].sockCl.recv(2048)
        numberP1HaveToGuess = int(Player1Guess.decode())
        print("[",sessionTwoPlayers[indexPlayer1].name,"] I guess : " ,numberP1HaveToGuess )
        
        player1Attepmts = 0
        while True:
            player1Attepmts = player1Attepmts + 1
            if numberP1HaveToGuess<numberForPL1:
                sessionTwoPlayers[indexPlayer1].sockCl.send(bytes("[ SERVER ] Wrong! The number is bigger. Try Again",'UTF-8'))
            
            if numberP1HaveToGuess>numberForPL1:
                sessionTwoPlayers[indexPlayer1].sockCl.send(bytes("[ SERVER ] Wrong! The number is smaller. Try Again",'UTF-8'))
            
            if numberP1HaveToGuess==numberForPL1:
                sessionTwoPlayers[indexPlayer2].sockCl.send(bytes(str(player1Attepmts),'UTF-8'))                
                sessionTwoPlayers[indexPlayer1].sockCl.send(bytes("ok",'UTF-8'))
                print("[ SERVER ] PLayer",sessionTwoPlayers[indexPlayer1].name,"guessed the number in",str(player1Attepmts),"attempts")
                break

            player1think = sessionTwoPlayers[indexPlayer1].sockCl.recv(2048)
            num1 = int(player1think.decode())
            print("[",sessionTwoPlayers[indexPlayer1].name,"] I guess : " ,num1)
            numberP1HaveToGuess = num1 

        #Players waiting for results
        waitingPl1 = sessionTwoPlayers[indexPlayer1].sockCl.recv(2048)
        waitingPl2 = sessionTwoPlayers[indexPlayer2].sockCl.recv(2048)
        print(waitingPl1.decode())

        newList = []
        newList.append(sessionTwoPlayers[indexPlayer1])
        newList.append(sessionTwoPlayers[indexPlayer2])
        declareWinner(newList,player1Attepmts,player2Attepmts)
        


def gameServerOneClient(clientIdentity):

    number = random.randint(1,50)
    print("[ SERVER ]", clientIdentity.name,"has to guess the number",number)
    clientIdentity.sockCl.send(bytes("[ SERVER ] Guess the number : __",'UTF-8'))
    plGuess = clientIdentity.sockCl.recv(2048)
    playerGuess = int(plGuess.decode())
    print("[",clientIdentity.name,"] I guess : " ,playerGuess)

    attempts = 0
    while True:
        attempts = attempts + 1
        if playerGuess<number:
            clientIdentity.sockCl.send(bytes("[ SERVER ] Wrong! The number is bigger. Try Again",'UTF-8'))
            
        if playerGuess>number:
            clientIdentity.sockCl.send(bytes("[ SERVER ] Wrong! The number is smaller. Try Again",'UTF-8'))
            
        if playerGuess==number:
            clientIdentity.sockCl.send(bytes("ok",'UTF-8'))             
            print("[ SERVER ] PLayer",clientIdentity.name,"guessd the number in",str(attempts),"attempts")
            break

        playerThink = clientIdentity.sockCl.recv(2048)
        num = int(playerThink.decode())
        print("[",clientIdentity.name,"] I guess : " ,num)
        playerGuess = num

    playerByeMsg = clientIdentity.sockCl.recv(2048)
    print("[",clientIdentity.name,"]",playerByeMsg.decode())


class ClientIdentity:
    def __init__(self,sockCl,nameCl,preferenceCl):
        self.sockCl = sockCl
        self.name = nameCl.upper()
        self.preference = preferenceCl 
    
    def printAboutInfo(self):
        print("Clinet name : ",self.name)
        print("preference Client:",self.preference)


class Thread(threading.Thread):

    def __init__(self,clientAdr,sockCl):
        threading.Thread.__init__(self)
        self.sockCl = sockCl
        print ("[ SERVER ] New connection created : ", clientAdr)

    def run(self):
        #ask name
        print ("[ SERVER ] Connection with : ", clientAdr)
        self.sockCl.send(bytes("[ SERVER ] Hi, What's your name ?",'UTF-8'))
        recvPreference = self.sockCl.recv(2048)
        clientNichName = recvPreference.decode()
        print ("[ CLIENT ] My name is ",clientNichName)
        preference = 'none'
        clientIdentity = ClientIdentity(self.sockCl,clientNichName,preference)
        
        #ask preference
        self.sockCl.send(bytes("[ SERVER ] Do you want to play with a friend? y/n",'UTF-8'))
        recvPreference = self.sockCl.recv(2048)
        recvPrefere = recvPreference.decode()
        if recvPrefere=='y':
            print ("[",clientNichName,"] I want to play with a friend! ")
            clientIdentity.preference = 'multiPlayer'
        elif recvPrefere=='n':
            print ("[",clientNichName,"] I want to play with server! ")
            clientIdentity.preference = 'onePlayer'

        print ("[",clientNichName,"] Ready to play!")

        if clientIdentity.preference == 'onePlayer':
            gameServerOneClient(clientIdentity)
        elif clientIdentity.preference == 'multiPlayer':
            sessionTwoPlayers.append(clientIdentity)
            gameServerTwoClients()
            

numberPlayers = 0
while True:  
    server.listen(1)
    accept = server.accept()
    socketCl = accept[0]
    clientAdr = accept[1]
    numberPlayers = numberPlayers + 1
    newThread = Thread(clientAdr, socketCl) 
    print("[ SERVER ] Number Players ",numberPlayers)
    newThread.start()
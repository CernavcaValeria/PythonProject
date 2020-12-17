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



def gameServerOneClient(clientIdentity):
    
    number = random.randint(0,50)
    print("[ SERVER ]", clientIdentity.name,"has to guess the number",number)
    clientIdentity.sockCl.send(bytes("[ SERVER ] Guess the number : __",'UTF-8'))
    plGuess = clientIdentity.sockCl.recv(2048)
    playerGuess = int(plGuess.decode())
    print("[",clientIdentity.name,"] I guess : " ,playerGuess)

    clientQuit = False
    attempts = 0
    while True:
        attempts = attempts + 1
        if playerGuess<number:
            clientIdentity.sockCl.send(bytes("[ SERVER ] Wrong! The number is bigger. Try Again",'UTF-8'))
            
        if playerGuess>number:
            clientIdentity.sockCl.send(bytes("[ SERVER ] Wrong! The number is smaller. Try Again",'UTF-8'))
            
        if playerGuess==number:
            clientIdentity.score.append(attempts)
            bestScore = min(clientIdentity.score)
            msg = "ok"+str(bestScore)
            clientIdentity.sockCl.send(bytes(msg,'UTF-8'))             
            print("[ SERVER ] PLayer",clientIdentity.name,"guessd the number in",str(attempts),"attempts")
            break

        playerThink = clientIdentity.sockCl.recv(2048)
        num = playerThink.decode()
        if num.isdigit():
            print("[",clientIdentity.name,"] I guess : " ,int(num))
            playerGuess = int(num)
        else:
            clientQuit = True
            print("[",clientIdentity.name,"] I have to go. Bye!\n")
            break

    if clientQuit == False:
        clientIdentity.score.append(attempts)
        playerByeMsg = clientIdentity.sockCl.recv(2048)
        onePlayer = []
        onePlayer.append(clientIdentity)
        playAgain(onePlayer)


def declareWinner(Players,p1Attmps,p2Attmps):
    
    player1Score = int(50-(2*(p1Attmps-1)))
    player2Score = int(50-(2*(p2Attmps-1)))
    player1BestSc = min(Players[0].score)
    player2BestSc = min(Players[1].score)

    if player1Score<player2Score:
        msg1 = "".join(('[ SERVER ] You lose! Score: ',str(player1Score),' points (',str(p1Attmps) ,' attempts)\n[ SERVER ] Your best result: ',str(player1BestSc),' attempts'))
        msg2 = "".join(('[ SERVER ] You won! Score: ', str(player2Score),' points (',str(p2Attmps) ,' attempts)\n[ SERVER ] Your best result: ',str(player2BestSc),' attempts'))
        Players[0].sockCl.send(bytes(msg1,'UTF-8'))
        Players[1].sockCl.send(bytes(msg2,'UTF-8'))
    elif player1Score>player2Score:
        msg1 = "".join(('[ SERVER ] You won! Score: ', str(player1Score),' points (',str(p1Attmps) ,' attempts)\n[ SERVER ] Your best result: ',str(player1BestSc),' attempts'))
        msg2 = "".join(('[ SERVER ] You lose! Score: ',str(player2Score),' points (',str(p2Attmps) ,' attempts)\n[ SERVER ] Your best result: ',str(player2BestSc),' attempts'))
        Players[0].sockCl.send(bytes(msg1,'UTF-8'))
        Players[1].sockCl.send(bytes(msg2,'UTF-8'))
    elif player1Score==player2Score:
        msg1 = "".join(('[ SERVER ] Equality ! Score : ',str(player1Score),' points (',str(p1Attmps) ,' attempts)\n[ SERVER ] Your best result: ',str(player1BestSc),' attempts'))
        msg2 = "".join(('[ SERVER ] Equality ! Score : ',str(player2Score),' points (',str(p2Attmps) ,' attempts)\n[ SERVER ] Your best result: ',str(player2BestSc),' attempts'))
        Players[0].sockCl.send(bytes(msg1,'UTF-8'))
        Players[1].sockCl.send(bytes(msg2,'UTF-8'))
    print("[ SERVER ] The results were transmitted successfully !")
    playAgain(Players)


def playAgain(Players):
    
    if len(Players)==2:
        recvIfWantContinuePl1 = Players[0].sockCl.recv(2048)
        recvIfWantContinuePl2 = Players[1].sockCl.recv(2048)
        wantContinuePl1 = recvIfWantContinuePl1.decode()
        wantContinuePl2 = recvIfWantContinuePl2.decode()

        Players[0].sockCl.send(bytes('[ SERVER ] I have successfully received your wish to continue or not!','UTF-8'))
        Players[1].sockCl.send(bytes('[ SERVER ] I have successfully received your wish to continue or not!','UTF-8'))

        if wantContinuePl1=='n' and wantContinuePl2=='n':    
            print ("[",Players[0].name,"] I have to go. Bye ! ")
            print ("[",Players[1].name,"] I have to go. Bye ! ")

        elif wantContinuePl1=='y' and wantContinuePl2=='y':
            continueGameP1 = Players[0].sockCl.recv(2048)
            continueGameP2 = Players[1].sockCl.recv(2048)
            print("[",Players[0].name,"]",continueGameP1.decode())
            print("[",Players[1].name,"]",continueGameP2.decode())
            sessionTwoPlayers.append(Players[0])
            sessionTwoPlayers.append(Players[1])
            Players[0].sockCl.send(bytes('n','UTF-8'))
            Players[1].sockCl.send(bytes('n','UTF-8'))
            readyPl1 = Players[0].sockCl.recv(2048)
            readyPl2 = Players[1].sockCl.recv(2048)
            print("[",Players[0].name,"]",readyPl1.decode())
            print("[",Players[1].name,"]",readyPl1.decode())
            gameServerTwoClients()

        elif wantContinuePl1=='y' and wantContinuePl2=='n':  
            continueGame = Players[0].sockCl.recv(2048)
            print("[",Players[0].name,"]",continueGame.decode())
            Players[0].sockCl.send(bytes('y','UTF-8'))
            isReady = Players[0].sockCl.recv(2048)
            print("[",Players[0].name,"]",isReady.decode())
            gameServerOneClient(Players[0])

        elif wantContinuePl1=='n' and wantContinuePl2=='y':
            continueGame = Players[1].sockCl.recv(2048)
            print("[",Players[1].name,"]",continueGame.decode())
            Players[1].sockCl.send(bytes('y','UTF-8'))
            isReady = Players[1].sockCl.recv(2048)
            print("[",Players[1].name,"]",isReady.decode())
            gameServerOneClient(Players[1])
    
    elif len(Players)==1:
        recvIfWantContinue = Players[0].sockCl.recv(2048)
        wantContinue = recvIfWantContinue.decode()
        Players[0].sockCl.send(bytes('[ SERVER ] I have successfully received your wish to continue or not!','UTF-8'))

        if wantContinue=='n':    
            print ("[",Players[0].name,"] I have to go. Bye ! ")
            
        elif wantContinue=='y':
            clientMsg = Players[0].sockCl.recv(2048)
            print ("[",Players[0].name,"]",clientMsg.decode())
            Players[0].sockCl.send(bytes('y','UTF-8'))
            isClReady = Players[0].sockCl.recv(2048)
            print ("[",Players[0].name,"]",isClReady.decode())
            gameServerOneClient(Players[0])


sessionTwoPlayers = []
def gameServerTwoClients():

    if len(sessionTwoPlayers)%2==1:
        print("[ SERVER ] Waiting opponent player for",sessionTwoPlayers[0].name )
        sessionTwoPlayers[0].sockCl.send(bytes("1",'UTF-8'))

    elif len(sessionTwoPlayers)%2==0:
        sessionTwoPlayers[0].sockCl.send(bytes("[ SERVER ] Start Game ...",'UTF-8'))
        sessionTwoPlayers[1].sockCl.send(bytes("[ SERVER ] Start Game ...",'UTF-8'))

        print("\n~ Start GAME between :",sessionTwoPlayers[0].name , "and", sessionTwoPlayers[1].name," ~")
        readyP1 = sessionTwoPlayers[0].sockCl.recv(2048)
        readyP2 = sessionTwoPlayers[1].sockCl.recv(2048)
        print(readyP1.decode())


        # player1 give the number | player2 guess the number
        sessionTwoPlayers[0].sockCl.send(bytes("[ SERVER ] Give me an number between [0,50 ]: __",'UTF-8'))
        numberForPlayer2 = sessionTwoPlayers[0].sockCl.recv(2048)
        numberForPL2 = int(numberForPlayer2.decode())
        print("[",sessionTwoPlayers[0].name,"] I give the number : " ,numberForPL2 )

        sessionTwoPlayers[1].sockCl.send(bytes("[ SERVER ] Guess the number : __",'UTF-8'))
        Player2Guess = sessionTwoPlayers[1].sockCl.recv(2048)
        player2ThinkTheNumber = int(Player2Guess.decode())
        print("[",sessionTwoPlayers[1].name,"] I guess : " ,player2ThinkTheNumber )

        clientQuit = False
        player2Attepmts = 0
        while True:
            player2Attepmts = player2Attepmts + 1
            if player2ThinkTheNumber<numberForPL2:
                sessionTwoPlayers[1].sockCl.send(bytes("[ SERVER ] Wrong! The number is bigger. Try Again",'UTF-8'))
            
            if player2ThinkTheNumber>numberForPL2:
                sessionTwoPlayers[1].sockCl.send(bytes("[ SERVER ] Wrong! The number is smaller. Try Again",'UTF-8'))
            
            if player2ThinkTheNumber==numberForPL2:
                sessionTwoPlayers[1].sockCl.send(bytes("ok",'UTF-8'))
                sessionTwoPlayers[0].sockCl.send(bytes(str(player2Attepmts),'UTF-8'))                
                print("[ SERVER ] PLayer",sessionTwoPlayers[1].name,"guessd the number in",str(player2Attepmts),"attempts")
                break

            player2think = sessionTwoPlayers[1].sockCl.recv(2048)
            num = player2think.decode()
            if num.isdigit():
                print("[",sessionTwoPlayers[1].name,"] I guess : " ,int(num))
                player2ThinkTheNumber = int(num)
            else:
                print("[",sessionTwoPlayers[1].name,"] I have to go. Bye!\n")
                clientQuit = True
                break

        if clientQuit==True:
            sessionTwoPlayers[0].sockCl.send(bytes('exit','UTF-8'))
            singleClient = sessionTwoPlayers[0] 
            sessionTwoPlayers.pop(0)
            sessionTwoPlayers.pop(0)
            gameServerOneClient(singleClient)
        else:

            sessionTwoPlayers[1].score.append(player2Attepmts)


            # player2 give the number | player1 guess the number
            ready1P1 = sessionTwoPlayers[0].sockCl.recv(2048)
            ready1P2 = sessionTwoPlayers[1].sockCl.recv(2048)
            print(ready1P1.decode())

            sessionTwoPlayers[1].sockCl.send(bytes("[ SERVER ] Give me an number between [0,50] : __",'UTF-8'))
            numberForPlayer1 = sessionTwoPlayers[1].sockCl.recv(2048)
            numberForPL1 = int(numberForPlayer1.decode())
            print("[",sessionTwoPlayers[1].name,"] I give the number : ",numberForPL1 )

            sessionTwoPlayers[0].sockCl.send(bytes("[ SERVER ] Guess the number : __",'UTF-8'))
            Player1Guess = sessionTwoPlayers[0].sockCl.recv(2048)
            player1ThinkTheNumber = int(Player1Guess.decode())
            print("[",sessionTwoPlayers[0].name,"] I guess : ",player1ThinkTheNumber )
            
            player1Attepmts = 0
            while True:
                player1Attepmts = player1Attepmts + 1
                if player1ThinkTheNumber<numberForPL1:
                    sessionTwoPlayers[0].sockCl.send(bytes("[ SERVER ] Wrong! The number is bigger. Try Again",'UTF-8'))
                
                if player1ThinkTheNumber>numberForPL1:
                    sessionTwoPlayers[0].sockCl.send(bytes("[ SERVER ] Wrong! The number is smaller. Try Again",'UTF-8'))
    
                if player1ThinkTheNumber==numberForPL1:
                    sessionTwoPlayers[1].sockCl.send(bytes(str(player1Attepmts),'UTF-8'))                
                    sessionTwoPlayers[0].sockCl.send(bytes("ok",'UTF-8'))
                    print("[ SERVER ] PLayer",sessionTwoPlayers[0].name,"guessed the number in",str(player1Attepmts),"attempts")
                    break

                player1think = sessionTwoPlayers[0].sockCl.recv(2048)
                num1 = player1think.decode()
                if num1.isdigit():
                    print("[",sessionTwoPlayers[0].name,"] I guess : " ,int(num1))
                    player1ThinkTheNumber = int(num1)
                else:
                    print("[",sessionTwoPlayers[0].name,"] I have to go. Bye!\n")
                    clientQuit = True
                    break

            if clientQuit==True:
                sessionTwoPlayers[1].sockCl.send(bytes('exit','UTF-8'))
                singleClient = sessionTwoPlayers[1] 
                sessionTwoPlayers.pop(0)
                sessionTwoPlayers.pop(0)
                gameServerOneClient(singleClient)
            else:
                sessionTwoPlayers[0].score.append(player1Attepmts)

                #Players waiting for results
                waitingPl1 = sessionTwoPlayers[0].sockCl.recv(2048)
                waitingPl2 = sessionTwoPlayers[1].sockCl.recv(2048)
                print(waitingPl1.decode())

                newList = []
                newList.append(sessionTwoPlayers[0])
                newList.append(sessionTwoPlayers[1])
                sessionTwoPlayers.pop(0)
                sessionTwoPlayers.pop(0)
                declareWinner(newList,player1Attepmts,player2Attepmts)


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

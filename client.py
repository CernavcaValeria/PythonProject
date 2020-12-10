import socket
import time

localHost = "127.0.0.1"
PORT = 1887
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((localHost, PORT))
listOfScorescOfSiglePlayer = []

def playAgain(myName):
    continueOrNo = input("".join(("[ SERVER ] Do you want to Continue? y/n :")))
    client.sendall(bytes(continueOrNo,'UTF-8'))
    serverRecvValidation =  client.recv(1024)
    print(serverRecvValidation.decode())
    
    if continueOrNo=='n':
        print("[ SERVER ] Bye!")
        client.close()
        
    elif continueOrNo=='y' :
        client.sendall(bytes("I want to continue",'UTF-8'))
    
        serverMsge =  client.recv(1024)
        playSingle = serverMsge.decode()
        if playSingle=='y':
            time.sleep(1)
            client.sendall(bytes("I'm ready to play with the server",'UTF-8'))
            playWithServer(myName)

        elif playSingle=='n':
            time.sleep(1)
            client.sendall(bytes("I'm ready to play with an opponent",'UTF-8'))
            playWithSomeone(myName)



def playWithServer(myName):
    serverMsg =  client.recv(1024)
    print(serverMsg.decode())
    number = input("".join(("[ ", myName.upper() ," ] ")))
    client.sendall(bytes(number,'UTF-8'))

    attempts = 0
    myBestScore = ''
    while True:
        msgS =  client.recv(1024)
        msg = msgS.decode()
        for i in range (2,len(msg)):
             myBestScore = "".join(msg[i])

        attempts = attempts + 1
        if msg[0]+msg[1]!='ok':
            print(msg)
        elif msg[0]+msg[1]=='ok':
            print("[ SERVER ] Congrats !You guessed the number !")
            break
        iThink = input("".join(("[ ", myName.upper() ," ] ")))
        client.sendall(bytes(iThink,'UTF-8'))

    print("[ SERVER ] The results are in the process of being displayed ...\n")
    time.sleep(2)
    print("[ SERVER ] Your score is",(50-2*(attempts-1)),"points (",attempts,"attempts )\n[ SERVER ] Your best result:",myBestScore,"attempts")
    client.sendall(bytes("Thank you ! Bye",'UTF-8'))
    playAgain(myName)



def whoWon():
    print("[ SERVER ] The results are in the process of being displayed ...\n")
    time.sleep(3)
    who = client.recv(1024)
    winner = who.decode()
    print(winner)



def playWithSomeone(myName):
    isReadySecondPlayer =  client.recv(1024)
    isReady = isReadySecondPlayer.decode()
    if isReady=='1':
        print("[ SERVER ] Wait for the second player ...")
        gameStart =  client.recv(1024)
        print(gameStart.decode())
    else:
        print(isReady)
    client.sendall(bytes("[ PLAYERS] We're ready for Part 1!",'UTF-8'))


    #start (part1)
    playerStatus1 =  client.recv(1024)#recv status: giver / guesser
    status1 = playerStatus1.decode()
    print(status1)

    statusPlayer = ''
    for i in range(11,15):
        statusPlayer = statusPlayer + status1[i]
 
    number = input("".join(("[ ", myName.upper() ," ] ")))
    client.sendall(bytes(number,'UTF-8'))

    attempts = 0
    if statusPlayer=='Gues':
        while True:
            msg_ =''
            msg_ =  client.recv(1024)
            msg = msg_.decode()
            attempts = attempts + 1
            if msg!='ok':
                print(msg)
            elif msg=='ok':
                print("[ SERVER ] Congrats !You guessed the number in",attempts,"attempts")
                break
            iThink = input("".join(("[ ", myName.upper() ," ] ")))
            client.sendall(bytes(iThink,'UTF-8'))

    elif statusPlayer=='Give':
        print("[ SERVER ] The opponent tries to guess ...")
        opponentGuessed =  client.recv(1024)
        opponentAttempts = opponentGuessed.decode()
        print("[ SERVER ] The opponent guessed the number in ",opponentAttempts,"attempts")


    #start(part2)
    client.sendall(bytes("[ PLAYERS] We're ready for Part 2 !",'UTF-8'))
    playerStatus2 =  client.recv(1024)#recv status1: giver / guesser
    status2 = playerStatus2.decode()
    print(status2)

    status1Player = ''
    for j in range(11,15):
        status1Player = status1Player + status2[j]
 
    number1 = input("".join(("[ ", myName.upper() ," ] ")))
    client.sendall(bytes(number1,'UTF-8'))

    attempts1 = 0
    if status1Player=='Gues':
        while True:
            attempts1 = attempts1 + 1
            msg_1 =  client.recv(1024)
            msg1 = msg_1.decode()
            if msg1!='ok':
                print(msg1)
            else:
                print("[ SERVER ] Congrats !You guessed the number in",attempts1,"attempts")
                break
            iThink1 = input("".join(("[ ", myName.upper() ," ] ")))
            client.sendall(bytes(iThink1,'UTF-8'))

    elif status1Player=='Give':
        print("[ SERVER ] The opponent tries to guess ...")
        opponentGuessed1 =  client.recv(1024)
        opponentAttempts1 = opponentGuessed1.decode()
        print("[ SERVER ] The opponent guessed the number in ",opponentAttempts1,"attempts")
    
    client.sendall(bytes("[ PLAYERS] Waiting for results ... ",'UTF-8'))
    whoWon()
    playAgain(myName)




serverQuestion =  client.recv(1024)#have name?
print(serverQuestion.decode())
myName = input("".join(("Name:")))
client.sendall(bytes(myName,'UTF-8'))

serverQuestion1 =  client.recv(1024)#play with server or friend?
print(serverQuestion1.decode())
responsePreference = input("".join(("Preference:")))
client.sendall(bytes(responsePreference,'UTF-8'))
    

if responsePreference=='y':
    playWithSomeone(myName)
elif responsePreference=='n':
    playWithServer(myName)

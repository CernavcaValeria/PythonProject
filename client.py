import socket
import time

localHost = "127.0.0.1"
PORT = 1886
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((localHost, PORT))


def playWithServer(myName):
    serverMsg =  client.recv(1024)
    print(serverMsg.decode())
    number = input("".join(("[ ", myName.upper() ," ] ")))
    client.sendall(bytes(number,'UTF-8'))

    attempts = 0
    while True:
        isCorect =  client.recv(1024)
        isCorectNr = isCorect.decode()
        attempts = attempts + 1
        if isCorectNr[0]+isCorectNr[1]!='ok':
            print(isCorectNr)
        elif isCorectNr[0]+isCorectNr[1]=='ok':
            print("[ SERVER ] Congrats !You've guessed the number in",attempts,"attempts")
            break
        iThink = input("".join(("[ ", myName.upper() ," ] ")))
        client.sendall(bytes(iThink,'UTF-8'))

    print("[ SERVER ] The results are in the process of being displayed ...\n")
    print("[ SERVER ] Your score is",(50-2*(attempts)),"points !")
    client.sendall(bytes("Thank you ! Bye",'UTF-8'))
    client.close()


def whoWon():
    print("[ SERVER ] The results are in the process of being displayed ...\n")
    time.sleep(4)
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

    client.sendall(bytes("[ PLAYERS] We're ready for Part1!",'UTF-8'))


    #start (part1)
    playerStatus1 =  client.recv(1024)#recv status: giver / guesser
    status = playerStatus1.decode()
    print(status)

    statusPlyer = ''
    for i in range(11,15):
        statusPlyer = statusPlyer + status[i]
 
    number = input("".join(("[ ", myName.upper() ," ] ")))
    client.sendall(bytes(number,'UTF-8'))

    attempts = 0
    if statusPlyer=='Gues':
        while True:
            isCorect_ =''
            isCorect_ =  client.recv(1024)
            isCorect = isCorect_.decode()
            attempts = attempts + 1
            if isCorect!='ok':
                print(isCorect)
            elif isCorect=='ok':
                print("[ SERVER ] Congrats !You've guessed the number in",attempts,"attempts")
                break
            iThink = input("".join(("[ ", myName.upper() ," ] ")))
            client.sendall(bytes(iThink,'UTF-8'))

    elif statusPlyer=='Give':
        print("[ SERVER ] The opponent tries to guess ...")
        opponentGuessed =  client.recv(1024)
        opponentTrys = opponentGuessed.decode()
        print("[ SERVER ] The opponent guessed the number in ",opponentTrys,"attempts")


    #start (part2)
    client.sendall(bytes("[ PLAYERS] We're ready for Part2 !",'UTF-8'))
    firstStepServer =  client.recv(1024)#recv status1: giver / guesser
    status1 = firstStepServer.decode()
    print(status1)

    status1Player = ''
    for j in range(11,15):
        status1Player = status1Player + status1[j]
 
    number1 = input("".join(("[ ", myName.upper() ," ] ")))
    client.sendall(bytes(number1,'UTF-8'))

    attempts1 = 0
    if status1Player=='Gues':
        while True:
            attempts1 = attempts1 + 1
            isCorect_1 =  client.recv(1024)
            isCorect1 = isCorect_1.decode()
            if isCorect1!='ok':
                print(isCorect1)
            else:
                print("[ SERVER ] Congrats !You've guessed the number in",attempts1,"attempts")
                break
            iThink1 = input("".join(("[ ", myName.upper() ," ] ")))
            client.sendall(bytes(iThink1,'UTF-8'))

    elif status1Player=='Give':
        print("[ SERVER ] The opponent tries to guess ...")
        opponentGuessed1 =  client.recv(1024)#the opponent guessed the number
        opponentTrys1 = opponentGuessed1.decode()
        print("[ SERVER ] The opponent guessed the number in ",opponentTrys1,"attempts")
    
    client.sendall(bytes("[ PLAYERS] Waiting for results ... ",'UTF-8'))
    whoWon()
    client.close()



serverQuestion =  client.recv(1024)#have name?
print(serverQuestion.decode())
myName = input("".join(("Name:")))
client.sendall(bytes(myName,'UTF-8'))

serverQuestion1 =  client.recv(1024)#play with server or friend
print(serverQuestion1.decode())
responsePreference = input("".join(("Preference:")))
client.sendall(bytes(responsePreference,'UTF-8'))
    

if responsePreference=='y':
    playWithSomeone(myName)
elif responsePreference=='n':
    playWithServer(myName)
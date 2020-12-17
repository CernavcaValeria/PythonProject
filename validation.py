def validateNumberInRange(myName):
    isOk = False
    while True:
        number = input("".join(("[ ", myName.upper() ," ] ")))
        if number.isdigit()==True:
            if  int(number) in range(0,51):
                isOk = True
            else:
                print("-----------The number is out of range (0,50). Try Again!") 
        elif number=='exit':
            isOk = True
        else:
            print("-----------Enter a number. Try Again!")
        if isOk==True:
            break
    return str(number)


def validatePrefernace():
    while True:  
        response = input("".join(("Preference:")))
        if response=='y' or response=='n':
            break
        print("-----------Wrong input. Try Again!")         
    return response


def validateResponse():
    while True:
        response = input("".join(("[ SERVER ] Do you want to Continue? y/n :")))
        if response=='y' or response=='n':
            break
        print("-----------Wrong input. Try Again!")
    return response

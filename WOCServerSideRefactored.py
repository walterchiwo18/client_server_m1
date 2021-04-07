#Server Side Refactored
#Walter Chiwo
#July 16 2020



from socket import SOCK_STREAM,AF_INET,socket
from threading import Thread


#Server Code 

SERVER = socket(AF_INET,SOCK_STREAM)
#AF_INET - IPV4
#SOCK_STREAM - TCIP - These are the things that allow
                    # for communication between computers

SERVER_HOST = ''#'192.168.5.183'# - there should
                       #            be a way of getting
                       #            machine host
                       #            but socket is like shut up dbag                        
SERVER_PORT = 33000
SERVER_ADDRESS = (SERVER_HOST,SERVER_PORT)

SERVER.bind(SERVER_ADDRESS)


#Computer Communication Code
computerAddresses = {}
computerNames = {}
messageSize = 1024 #this is how big a message can be in bytes


def machineAccess():
    """This allows different computers/machines to join the
       server"""
    while True:
        newMachine, newMachinesAddress = SERVER.accept()
        #This accept function is all it takes to receive new
        #machines like no sweat

        print("%s computer has joined the server and has this type %s" % (newMachinesAddress , type(newMachine)))


        
        newMachine.send(bytes("Welcome to the Chat!","utf-8"))
        computerAddresses[newMachine] = newMachinesAddress
        
        Thread(target = nameMachinesAndTalk, args = (newMachine,)).start()
        #Thread basically alows us to do many things at the same time
        #nameMachines will be identifing different computers at the same time

def nameMachinesAndTalk(newMachine):
    """This method will name new computers that join the server spread info"""

    newMachine.send(bytes("What is your name?","utf-8"))

    
    
    newMachineName = newMachine.recv(messageSize).decode("utf8")

    messageToRepeatName = "Welcome %s." % newMachineName

    computerNames[newMachine] = newMachineName


    broadcastToComputers(bytes(messageToRepeatName,"utf8"))
    
    
    
    while True:
        machineInput = newMachine.recv(messageSize)

        if machineInput != bytes("{quit}","utf8"):
            broadcastToComputers(machineInput,newMachineName)
        else:
            newMachine.send(bytes("BYE!!!","utf8"))
            broadcastToComputers(bytes("%s has left the chat :(" % newMachineName,"utf8"))
            del computerNames[newMachine]
            newMachine.close();
            break

   

    

def broadcastToComputers(broadCastMessage,broadCasterName = ""):
    """This should broadcast infomation to all the clients on the"""
    for eachComputer in computerNames:
        eachComputer.send(bytes(broadCasterName,"utf8")+broadCastMessage)

     
if __name__ == "__main__": #what the hell is this
    
    SERVER.listen(5)
    print("The server is just waiting for connections!!!")
    
    ACCEPT_THREAD = Thread( target = machineAccess)

    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()

    SERVER.close()
    

    
 
    
    

    







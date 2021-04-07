#Walter Chiwo
#07/22/2020
#Clientside Code

from socket import AF_INET,SOCK_STREAM,socket
from threading import Thread
import tkinter

##Establishing a Connection with the Server

CLIENT_SOCKET = socket(AF_INET,SOCK_STREAM)

CLIENT_HOST = '127.0.0.1'##socket.gethostbyname('localhost')  #How da fuq does this work?!!??!!
CLIENT_PORT = 33000

CLIENT_ADDRESS = (CLIENT_HOST,CLIENT_PORT)

CLIENT_SOCKET.connect(CLIENT_ADDRESS)

MESSAGE_SIZE = 1024



#Recieve, Send and Exit Definitions
def receiveMessages():
    """This is going to receive messages from the server/other clients"""

    while True:

        try:
            messagesFromServer = CLIENT_SOCKET.recv(MESSAGE_SIZE).decode("utf8")
            messageList.insert(tkinter.END,messagesFromServer)
            
        except OSError:
            break
        
        

def sendMessages(event = None):
    """This will send messages from this computer to server"""

    messageToSend = userMessages.get()
    userMessages.set("")

    CLIENT_SOCKET.send(bytes(messageToSend,"utf8"))

    if messageToSend == "{quit}":
        CLIENT_SOCKET.close()
        messageWindow.quit()        
    
    

    

def exitMessages(event = None):
    """This will exit messages from this computer to server"""
    userMessages.set("{quit}")
    sendMessages()


#GUI Stuff

messageWindow = tkinter.Tk()
messageWindow.title("Socket Chat")

messageFrame = tkinter.Frame(messageWindow)

userMessages = tkinter.StringVar()
userMessages.set("Type here...")

messageScroll = tkinter.Scrollbar(messageFrame)

messageList = tkinter.Listbox(messageFrame,height = 15, width = 50, yscrollcommand = messageScroll.set)

#Placing GUI Stuff on Screen

messageScroll.pack(side = tkinter.RIGHT, fill = tkinter.Y)

messageList.pack(side = tkinter.LEFT, fill = tkinter.BOTH)
messageList.pack()

messageFrame.pack()

messageEntryBox = tkinter.Entry(messageWindow,textvariable = userMessages)
messageEntryBox.bind("<Return>",sendMessages)
messageEntryBox.pack()

messageButton = tkinter.Button(messageWindow,text = "SEND",command = sendMessages)
messageButton.pack()

#is this something that might cause background problems?
messageWindow.protocol("VM_DELETE_WINDOW",exitMessages)


#How we can jumpstart this program


JUMP_CABLES = Thread(target = receiveMessages)
JUMP_CABLES.start()

tkinter.mainloop()












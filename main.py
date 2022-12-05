from tkinter import *
import tkinter as tk
import sys
import socket
import threading

#Globals
isConnected = False
clientSocket = None

#Initiate Window
window = Tk()

#Set up grid specifications
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
#This just means that all the grid boxes are the same size

#Create window to show log of text
log = Text(window)
log.pack()
log.grid(column=0, row=0, sticky = tk.W, padx = 5, pady = 5)
#Create space for user input
user = StringVar()
input = Entry(window, text = user)
input.grid(column=0, row=1, sticky=tk.W, padx = 5, pady = 5)

#Function that will send text from input to the log when enter is pressed
def Enter_pressed(event):
    input_get = input.get()
    #print(input_get)
    log.insert(INSERT, '%s\n' % input_get)

    if(input_get[-1] == ';'): #If the text entry is code, then execute it and show the result
        result = exec(input_get[:len(input_get) - 1])
        #print(result)
        #log.insert(INSERT, str(result) + '\n')


    user.set('')
    return "break"
#Bind the function above to whenever enter is pressed
input.bind("<Return>", Enter_pressed)

#Redirect stdout and stderr to the window. Accidentally made a shell oops
def redirect(inputStr):
    log.insert(INSERT, inputStr)
sys.stdout.write = redirect
#sys.stderr.write = redirect

#Tricky part. Multithreading for receiving server responses so the whole thing doesn't fall apart
def recv_from_server():
    while True:
        try:
            server_response = clientSocket.recvfrom(2048)
            if (server_response.length >= 1):
                log.insert(INSERT, server_response)
                log.insert(INSERT, '\n')
        except:
            pass

serverThread = threading.Thread(target=recv_from_server())

#Button for connecting to another client
def connectClick():
    serverPort = 9876
    serverName = "127.0.0.1" #localhost

    serverAddr = (serverName, serverPort)
    clientSocket = socket(socket.AF_INET, socket.SOCK_DGRAM)
    isConnected = True
    serverThread.start()

connect = tk.Button(window,
                    text="Connect",
                    command=connectClick())
connect.grid(column=1, row=1,sticky=tk.W, padx = 5, pady = 5)

def disconnectClick():
    if(isConnected):
        serverThread.stop()

disconnect = tk.Button(window,
                       text = "Disconnect",
                       command=disconnectClick())
disconnect.grid(column = 2, row=1, sticky=tk.W, padx = 5, pady = 5)



frame = Frame(window)

window.mainloop()


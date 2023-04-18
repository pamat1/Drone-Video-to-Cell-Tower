# Import Module
from tkinter import *
import threading
from streaming import *

peer_ip = None
chat = None
stream = None
# create root window
root = Tk()

# root window title and dimension
root.title("Drone Video to Cell Tower")
# Set geometry(widthxheight)
root.geometry('667x655')


####################### Helpers ###########################

def cut(entry):
    text = entry.get()
    entry.delete(0, END)
    return text


def clicked():
    global chat
    global peer_ip
    root.title("Connecting... please wait")
    peer_ip, sport, dport, sock = holepunch(serverOutput)
    root.title("Drone Video to Cell Tower")
    chat = P2P_Chat_Thread(peer_ip, sport, dport, sock, peerOutput, peerData)
    chat.start()


def beginStream():
    global peer_ip
    global stream
    global chat
    if (peer_ip == None):
        serverOutput.insert(INSERT, "Cannot begin stream. No peer IP found.\n")
        return
    if (streamButton['text'] == "Begin Stream"):
        serverOutput.insert(INSERT, "Beginning Stream.\n")
        streamButton.config(text="Stop Stream")
        stream = P2P_Stream_Thread(peer_ip)
        chat.startStream()
        #stream.startStream()
        #print("./rx.sh " + peer_ip + " " + str(STREAM_PORT))
        subprocess.Popen("./rx.sh " + peer_ip + " " + str(STREAM_PORT), shell=True)
    else:
        serverOutput.insert(INSERT, "Stopping Stream.\n")
        chat.stopStream()
        stream.stopStream()
        streamButton.config(text="Begin Stream")


################ Frame 1: Connecting to Server ############

server_connect_frame = Frame(root)

serverAddress = Entry(server_connect_frame, width=60)
serverConnect = Button(server_connect_frame, text="Connect to Server", command=clicked)
serverConnect.bind()

serverAddress.grid(row=0, column=0, sticky=W, pady=2, padx=2)
serverConnect.grid(row=0, column=1, sticky=W, pady=2, padx=2)

################ Frame 2: Server Output ###################

server_comm_frame = Frame(root)

serverLabel = Label(server_comm_frame, text="Server/Console Output")
serverOutput = Text(server_comm_frame, width=70, height=5)

serverLabel.grid(row=0, column=0, sticky=N, pady=2, padx=2)
serverOutput.grid(row=1, column=0, sticky=N, pady=2, padx=2)

################## Frame 3: Peer Output ####################

peer_frame = Frame(root)

p2pLabel = Label(peer_frame, text="Peer Output")
p = Frame(peer_frame)
peerOutput = Text(p, width=50)
p2 = Frame(p)
peerData = Listbox(p2, height=5)
streamButton = Button(p2, text="Begin Stream", height=5, command=beginStream)

peerInput = Entry(peer_frame, width=80)
peerInput.grid(row=0, column=0, sticky=E, pady=2, padx=2)
peerInput.bind('<Return>', lambda e: chat.sendMsg(cut(peerInput)))

p2pLabel.grid(row=0, column=0, sticky=N, pady=2, padx=2)

peerOutput.grid(row=0, column=0, sticky=W, pady=2, padx=2)
peerData.grid(row=0, column=1, pady=2)
streamButton.grid(row=1, column=1, pady=10)
p2.grid(row=0, column=1, padx=2, pady=2)
p.grid(row=1, column=0, sticky=W, pady=2, padx=2)

peerInput.grid(row=2, column=0, sticky=N, pady=2, padx=2)

# Putting Everything Together

server_connect_frame.grid(row=0, columnspan=2, column=0, pady=2)
server_comm_frame.grid(row=1, column=0, pady=2, padx=10)
peer_frame.grid(row=2, column=0, rowspan=2, pady=2, padx=10)

# Execute Tkinter
root.mainloop()
